import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


class ButterflyController(Node):

    def __init__(self):
        super().__init__('butterfly_controller')

        # ------------------------------------------------
        # Publisher: control turtle velocity
        # ------------------------------------------------

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # ------------------------------------------------
        # Subscriber: receive turtle position
        # ------------------------------------------------

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # ------------------------------------------------
        # Service client: change pen color
        # ------------------------------------------------

        self.pen_client = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        # ------------------------------------------------
        # Turtle state
        # ------------------------------------------------

        self.x = 5.544444
        self.y = 5.544444
        self.theta = 0.0

        # ------------------------------------------------
        # Butterfly parameters
        # ------------------------------------------------

        self.t = 0.0

        # Bigger butterfly
        self.scale = 1.3

        # Center of turtlesim
        self.center_x = 5.5
        self.center_y = 5.5

        # ------------------------------------------------
        # Speed parameters
        # ------------------------------------------------

        # Desired physical distance between consecutive
        # waypoints (in turtlesim units). This replaces the
        # old FIXED t_step, which caused waypoints to bunch
        # up / jump erratically in the tightly-curled part
        # of the curve (the "turbulence" you saw).
        self.desired_arc_length = 0.06

        # Distance at which we move to next point
        self.point_threshold = 0.08

        # ------------------------------------------------
        # Warm colors
        # RGB values are 0-255
        # ------------------------------------------------

        self.colors = [
            (255, 120, 0),   # Orange
            (255, 60, 0),    # Red-orange
            (255, 190, 0),   # Golden orange
            (255, 30, 30),   # Warm red
        ]

        self.current_color = -1

        # ------------------------------------------------
        # Timer
        # ------------------------------------------------

        self.timer = self.create_timer(
            0.02,
            self.control_loop
        )

        self.finished = False

        # Set initial pen
        self.change_pen_color(0)

    # ====================================================
    # Receive turtle position
    # ====================================================

    def pose_callback(self, msg):

        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta

    # ====================================================
    # Butterfly equation
    # ====================================================

    def butterfly(self, t):

        factor = (
            math.exp(math.cos(t))
            - 2 * math.cos(4 * t)
            - math.sin(t / 12) ** 5
        )

        x = math.sin(t) * factor
        y = math.cos(t) * factor

        return x, y

    # ====================================================
    # Estimate local curve speed |d(point)/dt| and return
    # a t_step that advances roughly `desired_arc_length`
    # of actual physical distance.
    #
    # This is the key fix: the old code used a FIXED t_step,
    # but the butterfly curve moves at very different speeds
    # depending on t (fast in the wide wing sweeps, slow and
    # twisty in the small looping region). A fixed t_step
    # therefore produced waypoints that were sometimes far
    # apart (fine) and sometimes bunched at sharp angles
    # (causing the turtle to zig-zag / scribble).
    # ====================================================

    def adaptive_t_step(self, t):

        probe_dt = 1e-4

        x1, y1 = self.butterfly(t)
        x2, y2 = self.butterfly(t + probe_dt)

        dx = (x2 - x1) * self.scale
        dy = (y2 - y1) * self.scale

        speed = math.hypot(dx, dy) / probe_dt

        # Avoid division by ~0 in near-stationary spots
        speed = max(speed, 1e-3)

        step = self.desired_arc_length / speed

        # Clamp so we never take absurdly large/small jumps
        return min(max(step, 0.001), 0.25)

    # ====================================================
    # Normalize angle
    # ====================================================

    def normalize_angle(self, angle):

        while angle > math.pi:
            angle -= 2 * math.pi

        while angle < -math.pi:
            angle += 2 * math.pi

        return angle

    # ====================================================
    # Change pen color
    # ====================================================

    def change_pen_color(self, color_index):

        if color_index == self.current_color:
            return

        if not self.pen_client.wait_for_service(timeout_sec=0.1):
            return

        r, g, b = self.colors[color_index]

        request = SetPen.Request()

        request.r = r
        request.g = g
        request.b = b

        # Thicker line
        request.width = 4

        # 0 = pen on
        request.off = 0

        self.pen_client.call_async(request)

        self.current_color = color_index

    # ====================================================
    # Main control loop
    # ====================================================

    def control_loop(self):

        if self.finished:
            return

        # -----------------------------------------------
        # Current butterfly point
        # -----------------------------------------------

        bx, by = self.butterfly(self.t)

        target_x = self.center_x + self.scale * bx
        target_y = self.center_y + self.scale * by

        # -----------------------------------------------
        # Distance to target
        # -----------------------------------------------

        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        # -----------------------------------------------
        # If we reached the point,
        # move to the next butterfly point using an
        # ADAPTIVE step (fixes the scribbling/turbulence)
        # -----------------------------------------------

        if distance < self.point_threshold:

            self.t += self.adaptive_t_step(self.t)

            # -------------------------------------------
            # Change color as we progress
            # -------------------------------------------

            progress = self.t / (12 * math.pi)

            color_index = int(
                progress * len(self.colors)
            )

            color_index = min(
                color_index,
                len(self.colors) - 1
            )

            self.change_pen_color(color_index)

            # -------------------------------------------
            # Butterfly finished
            # -------------------------------------------

            if self.t >= 12 * math.pi:

                stop = Twist()

                self.publisher.publish(stop)

                self.finished = True

                self.get_logger().info(
                    '🦋 Butterfly complete!'
                )

                return

        # -----------------------------------------------
        # Calculate direction
        # -----------------------------------------------

        target_angle = math.atan2(
            dy,
            dx
        )

        angle_error = self.normalize_angle(
            target_angle - self.theta
        )

        # -----------------------------------------------
        # Create velocity command
        #
        # FIX: previously the turtle drove forward at full
        # speed *while* turning, regardless of how far off
        # its heading was. That made it cut corners between
        # closely-spaced waypoints instead of pivoting onto
        # them cleanly -- the other big cause of the
        # scribbly look. Now forward speed is throttled down
        # when the heading error is large (rotate-in-place
        # first, then drive), and speeded back up once
        # roughly facing the target.
        # -----------------------------------------------

        msg = Twist()

        # 1.0 when facing the target dead-on, shrinks toward
        # 0 as the heading error approaches +/-90 degrees or
        # more, and never goes negative (no reversing).
        heading_factor = max(math.cos(angle_error), 0.0)

        # Faster base speeds than the original
        max_linear = 6.0
        max_angular = 10.0

        msg.linear.x = min(6.0 * distance * heading_factor, max_linear)
        msg.angular.z = max(
            min(10.0 * angle_error, max_angular),
            -max_angular
        )

        self.publisher.publish(msg)


# ========================================================
# Main
# ========================================================

def main(args=None):

    rclpy.init(args=args)

    node = ButterflyController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
