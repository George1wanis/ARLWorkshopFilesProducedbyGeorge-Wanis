import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


class RaceCarController(Node):

    def __init__(self):
        super().__init__('race_car_controller')

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
        # Service client: change pen color / lift pen
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
        # Drawing parameters
        # ------------------------------------------------

        # Overall size of the car
        self.scale = 1.0

        # Center of turtlesim canvas
        self.center_x = 5.5
        self.center_y = 5.5

        # Distance at which we consider a waypoint "reached".
        # Kept small and paired with a slower top speed below so
        # the turtle actually lands on each point instead of
        # blowing past it and looping back.
        self.point_threshold = 0.05

        # ------------------------------------------------
        # Palette
        # ------------------------------------------------

        self.colors = {
            'red': (220, 20, 20),
            'black': (15, 15, 15),
        }

        # ------------------------------------------------
        # Pen state tracking
        #
        # KEY FIX: call_async() only *sends* a SetPen request,
        # it does not wait for turtlesim to apply it. Driving
        # forward right after calling it meant the turtle
        # sometimes moved a tick or two (or more) with the OLD
        # pen state/color still active -- that's what was
        # drawing the stray lines connecting separate shapes
        # (e.g. spoiler <-> body, stripe <-> wheel) in the
        # earlier version. Now we track a pending request and
        # freeze motion until the service confirms it applied.
        # ------------------------------------------------

        self.pen_is_down = False
        self.pen_color_name = None
        self.pending_pen_state = None
        self.waiting_for_pen = False

        # ------------------------------------------------
        # Build the full list of waypoints that trace out
        # the car (body, spoiler, stripe, both wheels)
        # ------------------------------------------------

        self.path = self.build_path()
        self.path_index = 0

        # ------------------------------------------------
        # Timer
        # ------------------------------------------------

        self.timer = self.create_timer(
            0.02,
            self.control_loop
        )

        self.finished = False

    # ====================================================
    # Receive turtle position
    # ====================================================

    def pose_callback(self, msg):

        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta

    # ====================================================
    # Geometry helpers
    # ====================================================

    def circle_points(self, cx, cy, r, steps=60):
        """Return `steps` points evenly spaced around a circle,
        used to trace each wheel. More steps than before so each
        step is a smaller, gentler turn -> smoother wheels."""

        pts = []

        for i in range(steps):
            angle = 2 * math.pi * i / steps
            pts.append((
                cx + r * math.cos(angle),
                cy + r * math.sin(angle),
            ))

        return pts

    def to_world(self, local_x, local_y):
        """Convert a local car-space coordinate into a turtlesim
        world coordinate (scaled + centered)."""

        return (
            self.center_x + self.scale * local_x,
            self.center_y + self.scale * local_y,
        )

    # ====================================================
    # Build the ordered list of waypoints
    #
    # Each waypoint says: (x, y, pen_down, color)
    #   pen_down = False -> pen lifts and the turtle glides to
    #              this point without drawing (used to jump
    #              between separate shapes: body -> spoiler ->
    #              stripe -> wheel -> wheel)
    #   pen_down = True  -> the turtle draws a line from the
    #              previous point to this one
    # ====================================================

    def build_path(self):

        path = []

        # ------------------------------------------------
        # 1) Car body (side profile), red, closed outline
        # ------------------------------------------------

        body_local = [
            (-3.6, -0.6),   # rear bottom corner
            (-3.6, 0.2),    # rear bumper, vertical
            (-3.0, 0.5),    # rear deck
            (-2.6, 1.0),    # rear windshield base
            (-1.6, 1.5),    # roof start
            (0.2, 1.6),     # roof peak
            (1.6, 1.3),     # windshield, front top
            (2.2, 0.7),     # hood slope
            (3.6, 0.5),     # front hood
            (3.9, 0.1),     # front bumper curve
            (3.9, -0.6),    # front bottom corner
            (-3.6, -0.6),   # close the outline back at the start
        ]

        path += self.shape_to_waypoints(body_local, 'red')

        # ------------------------------------------------
        # 2) Rear spoiler, red, small wing above the trunk
        # ------------------------------------------------

        spoiler_local = [
            (-3.4, 0.5),
            (-3.4, 1.3),
            (-2.7, 1.3),
            (-2.7, 1.0),
        ]

        path += self.shape_to_waypoints(spoiler_local, 'red')

        # ------------------------------------------------
        # 3) Racing stripe down the hood, black
        # ------------------------------------------------

        stripe_local = [
            (1.6, 1.2),
            (3.7, 0.25),
        ]

        path += self.shape_to_waypoints(stripe_local, 'black')

        # ------------------------------------------------
        # 4) Wheels, black, tucked under the body
        # ------------------------------------------------

        wheel_radius = 0.9

        rear_wheel_center = (-2.3, -1.0)
        front_wheel_center = (2.3, -1.0)

        for cx, cy in (rear_wheel_center, front_wheel_center):

            circle_local = self.circle_points(cx, cy, wheel_radius)

            # close the circle by returning to its first point
            circle_local = circle_local + [circle_local[0]]

            path += self.shape_to_waypoints(circle_local, 'black')

        return path

    def shape_to_waypoints(self, local_points, color_name):
        """Turn a list of local-space points into waypoints:
        pen lifts to travel to the first point, then stays down
        while tracing the rest of the shape."""

        waypoints = []

        first_x, first_y = self.to_world(*local_points[0])

        waypoints.append({
            'x': first_x,
            'y': first_y,
            'pen_down': False,
            'color': color_name,
        })

        for local_x, local_y in local_points[1:]:

            world_x, world_y = self.to_world(local_x, local_y)

            waypoints.append({
                'x': world_x,
                'y': world_y,
                'pen_down': True,
                'color': color_name,
            })

        return waypoints

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
    # Pen control
    #
    # request_pen() only fires the service call and returns
    # True if a change was actually needed. It does NOT assume
    # the change has taken effect -- pen_is_down/pen_color_name
    # are only updated once the service confirms, inside
    # pen_response_callback(). control_loop() checks
    # self.waiting_for_pen and freezes movement until then.
    # ====================================================

    def request_pen(self, down, color_name):

        if down == self.pen_is_down and color_name == self.pen_color_name:
            return False

        if not self.pen_client.wait_for_service(timeout_sec=0.1):
            return False

        r, g, b = self.colors[color_name]

        request = SetPen.Request()

        request.r = r
        request.g = g
        request.b = b

        # Thicker line while actually drawing
        request.width = 4 if down else 1

        # 0 = pen down / drawing, 1 = pen up / no line
        request.off = 0 if down else 1

        future = self.pen_client.call_async(request)

        self.pending_pen_state = (down, color_name)
        self.waiting_for_pen = True

        future.add_done_callback(self.pen_response_callback)

        return True

    def pen_response_callback(self, future):

        self.pen_is_down, self.pen_color_name = self.pending_pen_state
        self.waiting_for_pen = False

    # ====================================================
    # Main control loop
    # ====================================================

    def control_loop(self):

        if self.finished:
            return

        # -----------------------------------------------
        # Hold still while a pen change is in flight so we
        # never draw (or skip drawing) with the wrong state
        # -----------------------------------------------

        if self.waiting_for_pen:
            self.publisher.publish(Twist())
            return

        # -----------------------------------------------
        # Whole car finished
        # -----------------------------------------------

        if self.path_index >= len(self.path):

            stop = Twist()

            self.publisher.publish(stop)

            self.finished = True

            self.get_logger().info(
                '🏎️  Race car complete!'
            )

            return

        target = self.path[self.path_index]

        # -----------------------------------------------
        # If this waypoint needs a different pen state than
        # we currently have, request it and wait -- don't
        # move until it's confirmed applied.
        # -----------------------------------------------

        if self.request_pen(target['pen_down'], target['color']):
            self.publisher.publish(Twist())
            return

        # -----------------------------------------------
        # Distance to target
        # -----------------------------------------------

        dx = target['x'] - self.x
        dy = target['y'] - self.y

        distance = math.sqrt(dx * dx + dy * dy)

        # -----------------------------------------------
        # Reached this waypoint -> advance to the next one
        # -----------------------------------------------

        if distance < self.point_threshold:
            self.path_index += 1
            return

        # -----------------------------------------------
        # Calculate direction
        # -----------------------------------------------

        target_angle = math.atan2(dy, dx)

        angle_error = self.normalize_angle(
            target_angle - self.theta
        )

        # -----------------------------------------------
        # Rotate-in-place first, then drive, so corners of
        # the car come out sharp instead of rounded off.
        # Lower top speeds than before, since waypoints on
        # the wheels/spoiler are close together and the old
        # 6.0 units/sec let the turtle overshoot them and
        # loop back to correct, which is what drew the small
        # spirals.
        # -----------------------------------------------

        heading_factor = max(math.cos(angle_error), 0.0)

        max_linear = 3.0
        max_angular = 8.0

        msg = Twist()

        msg.linear.x = min(4.0 * distance * heading_factor, max_linear)
        msg.angular.z = max(
            min(8.0 * angle_error, max_angular),
            -max_angular
        )

        self.publisher.publish(msg)


# ========================================================
# Main
# ========================================================

def main(args=None):

    rclpy.init(args=args)

    node = RaceCarController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
