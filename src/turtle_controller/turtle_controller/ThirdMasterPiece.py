import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


class CinematicRosArt(Node):

    def __init__(self):
        super().__init__('cinematic_ros_art')

        # ------------------------------------------------
        # Publisher & Subscriber
        # ------------------------------------------------
        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # ------------------------------------------------
        # Service Client: Set Pen
        # ------------------------------------------------
        self.pen_client = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        # ------------------------------------------------
        # Turtle Pose Tracking
        # ------------------------------------------------
        self.x = 5.544444
        self.y = 5.544444
        self.theta = 0.0

        # ------------------------------------------------
        # Canvas Settings & Thresholds
        # ------------------------------------------------
        self.scale = 0.85
        self.center_x = 5.5
        self.center_y = 5.5
        self.point_threshold = 0.05

        # ------------------------------------------------
        # Cinematic Palette (RGB)
        # ------------------------------------------------
        self.colors = {
            'neon_pink': (255, 20, 147),
            'gold': (255, 215, 0),
            'cyan': (0, 238, 255),
            'magenta': (220, 0, 180),
            'soft_yellow': (255, 255, 180),
        }

        # ------------------------------------------------
        # Pen State Async Synchronization
        # ------------------------------------------------
        self.pen_is_down = False
        self.pen_color_name = None
        self.pending_pen_state = None
        self.waiting_for_pen = False

        # ------------------------------------------------
        # Path Execution
        # ------------------------------------------------
        self.path = self.build_path()
        self.path_index = 0
        self.finished = False

        # Timer loop (50 Hz)
        self.timer = self.create_timer(0.02, self.control_loop)

    def pose_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta

    # ====================================================
    # Parametric Shape Generators (Local Coordinates)
    # ====================================================

    def generate_heart(self, cx, cy, radius, steps=50):
        """Generates a smooth heart outline using cardioid parametric equations."""
        pts = []
        for i in range(steps + 1):
            t = 2 * math.pi * i / steps
            # Heart formula
            x = radius * (16 * (math.sin(t) ** 3)) / 16.0
            y = radius * (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)) / 16.0
            pts.append((cx + x, cy + y))
        return pts

    def generate_star(self, cx, cy, outer_r, inner_r, points=5):
        """Generates a 5-pointed star outline."""
        pts = []
        total_steps = points * 2
        for i in range(total_steps + 1):
            angle = (i * math.pi / points) - (math.pi / 2)
            r = outer_r if i % 2 == 0 else inner_r
            pts.append((
                cx + r * math.cos(angle),
                cy + r * math.sin(angle)
            ))
        return pts

    def generate_flower(self, cx, cy, r_petal, petals=5, steps_per_petal=12):
        """Generates a 5-petaled flower shape."""
        pts = []
        total_steps = petals * steps_per_petal
        for i in range(total_steps + 1):
            theta = 2 * math.pi * i / total_steps
            # Rose curve formula for flower effect
            r = r_petal * (0.5 + 0.5 * math.fabs(math.sin(petals * theta / 2)))
            pts.append((
                cx + r * math.cos(theta),
                cy + r * math.sin(theta)
            ))
        return pts

    def to_world(self, local_x, local_y):
        """Maps local coordinates to Turtlesim screen bounds [0..11]."""
        return (
            self.center_x + self.scale * local_x,
            self.center_y + self.scale * local_y,
        )

    def shape_to_waypoints(self, local_points, color_name):
        """Converts local points into actionable waypoints with pen lifts/drops."""
        waypoints = []
        if not local_points:
            return waypoints

        first_x, first_y = self.to_world(*local_points[0])

        # Lift pen and fly to starting position
        waypoints.append({
            'x': first_x,
            'y': first_y,
            'pen_down': False,
            'color': color_name,
        })

        # Drop pen and draw the path
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
    # Path Assembly: "I <HEART> ROS" + Decorators
    # ====================================================

    def build_path(self):
        path = []

        # --- LETTER 'I' (Cyan) ---
        letter_i = [
            (-5.0, 3.2), (-3.8, 3.2),        # Top bar
            (-4.4, 3.2), (-4.4, 1.2),        # Main stem
            (-5.0, 1.2), (-3.8, 1.2)         # Bottom bar
        ]
        path += self.shape_to_waypoints(letter_i, 'cyan')

        # --- HEART SHAPE (Neon Pink) ---
        heart_pts = self.generate_heart(cx=-2.0, cy=2.2, radius=1.2)
        path += self.shape_to_waypoints(heart_pts, 'neon_pink')

        # --- LETTER 'R' (Gold) ---
        letter_r = [
            (0.0, 1.2), (0.0, 3.2),          # Stem up
            (1.0, 3.2), (1.3, 2.7),          # Upper loop outer curve
            (1.0, 2.2), (0.0, 2.2),          # Upper loop bottom
            (0.6, 2.2), (1.4, 1.2)           # Diagonal leg
        ]
        path += self.shape_to_waypoints(letter_r, 'gold')

        # --- LETTER 'O' (Gold) ---
        letter_o = []
        steps = 30
        for i in range(steps + 1):
            angle = 2 * math.pi * i / steps
            letter_o.append((
                2.6 + 0.7 * math.cos(angle),
                2.2 + 1.0 * math.sin(angle)
            ))
        path += self.shape_to_waypoints(letter_o, 'gold')

        # --- LETTER 'S' (Gold) ---
        letter_s = [
            (4.8, 3.0), (4.2, 3.2), (3.7, 2.8),  # Top curve
            (4.7, 2.2),                          # Middle slope
            (3.7, 1.6), (4.3, 1.2), (4.8, 1.4)   # Bottom curve
        ]
        path += self.shape_to_waypoints(letter_s, 'gold')

        # --- DECORATIVE FLOWERS (Magenta) ---
        flower1 = self.generate_flower(cx=-3.5, cy=-1.5, r_petal=0.9, petals=5)
        path += self.shape_to_waypoints(flower1, 'magenta')

        flower2 = self.generate_flower(cx=3.5, cy=-1.5, r_petal=0.9, petals=5)
        path += self.shape_to_waypoints(flower2, 'magenta')

        # --- DECORATIVE STARS (Soft Yellow) ---
        star1 = self.generate_star(cx=-1.2, cy=-2.0, outer_r=0.7, inner_r=0.3)
        path += self.shape_to_waypoints(star1, 'soft_yellow')

        star2 = self.generate_star(cx=0.0, cy=-1.0, outer_r=0.9, inner_r=0.4)
        path += self.shape_to_waypoints(star2, 'soft_yellow')

        star3 = self.generate_star(cx=1.2, cy=-2.0, outer_r=0.7, inner_r=0.3)
        path += self.shape_to_waypoints(star3, 'soft_yellow')

        return path

    # ====================================================
    # Kinematics and Control Logic
    # ====================================================

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

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
        request.width = 3 if down else 1
        request.off = 0 if down else 1

        future = self.pen_client.call_async(request)
        self.pending_pen_state = (down, color_name)
        self.waiting_for_pen = True
        future.add_done_callback(self.pen_response_callback)
        return True

    def pen_response_callback(self, future):
        self.pen_is_down, self.pen_color_name = self.pending_pen_state
        self.waiting_for_pen = False

    def control_loop(self):
        if self.finished:
            return

        if self.waiting_for_pen:
            self.publisher.publish(Twist())
            return

        if self.path_index >= len(self.path):
            self.publisher.publish(Twist())
            self.finished = True
            self.get_logger().info('✨ "I ROS" masterpiece drawing complete! ✨')
            return

        target = self.path[self.path_index]

        if self.request_pen(target['pen_down'], target['color']):
            self.publisher.publish(Twist())
            return

        dx = target['x'] - self.x
        dy = target['y'] - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.point_threshold:
            self.path_index += 1
            return

        target_angle = math.atan2(dy, dx)
        angle_error = self.normalize_angle(target_angle - self.theta)

        # Smooth kinematic scaling
        heading_factor = max(math.cos(angle_error), 0.0)
        max_linear = 2.5
        max_angular = 7.0

        msg = Twist()
        msg.linear.x = min(3.5 * distance * heading_factor, max_linear)
        msg.angular.z = max(min(7.0 * angle_error, max_angular), -max_angular)

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CinematicRosArt()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
