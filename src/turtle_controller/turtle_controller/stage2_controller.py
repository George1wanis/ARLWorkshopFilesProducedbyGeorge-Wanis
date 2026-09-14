import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen, TeleportAbsolute
from std_srvs.srv import Empty
from turtle_interfaces.srv import ShapeCommand


class Stage2Controller(Node):

    def __init__(self):
        super().__init__('stage2_controller')

        # ------------------------------------------------
        # Service Server: Shape Command
        # ------------------------------------------------
        self.srv = self.create_service(
            ShapeCommand,
            '/shape_command',
            self.handle_command
        )

        # ------------------------------------------------
        # Publisher: /turtle1/cmd_vel
        # ------------------------------------------------
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # ------------------------------------------------
        # Subscriber: /turtle1/pose
        # ------------------------------------------------
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # ------------------------------------------------
        # Service Clients
        # ------------------------------------------------
        # Client to teleport turtle to middle (reset)
        self.teleport_client = self.create_client(
            TeleportAbsolute,
            '/turtle1/teleport_absolute'
        )

        # Client to change pen colors
        self.pen_client = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        # Client to clear turtlesim canvas
        self.clear_client = self.create_client(
            Empty,
            '/clear'
        )

        # ------------------------------------------------
        # Turtle State
        # ------------------------------------------------
        self.x = 5.544445
        self.y = 5.544445
        self.theta = 0.0

        # State machine: 'IDLE', 'RUNNING', 'PAUSED'
        self.state = 'IDLE'
        self.active_shape = None

        # ------------------------------------------------
        # Pen State & Palettes
        # ------------------------------------------------
        self.pen_is_down = False
        self.pen_rgb = None
        self.pen_width = 3
        self.pending_pen_state = None
        self.waiting_for_pen = False

        self.color_palette = {
            'orange': (255, 120, 0),
            'red_orange': (255, 60, 0),
            'gold_orange': (255, 190, 0),
            'warm_red': (255, 30, 30),
            'red': (220, 20, 20),
            'black': (15, 15, 15),
            'neon_pink': (255, 20, 147),
            'gold': (255, 215, 0),
            'cyan': (0, 238, 255),
            'magenta': (220, 0, 180),
            'soft_yellow': (255, 255, 180),
            'white': (255, 255, 255),
        }

        # ------------------------------------------------
        # Butterfly Curve Parameters (FirstMasterPiece)
        # ------------------------------------------------
        self.t = 0.0
        self.max_t = 12 * math.pi
        self.butterfly_scale = 1.3
        self.desired_arc_length = 0.06
        self.butterfly_threshold = 0.08
        self.butterfly_colors = [
            (255, 120, 0),   # Orange
            (255, 60, 0),    # Red-orange
            (255, 190, 0),   # Golden orange
            (255, 30, 30),   # Warm red
        ]
        self.current_butterfly_color_idx = -1

        # ------------------------------------------------
        # Waypoint Path Execution (RaceCar & ILROS)
        # ------------------------------------------------
        self.path = []
        self.path_index = 0
        self.waypoint_threshold = 0.05

        # ------------------------------------------------
        # Timer (50 Hz)
        # ------------------------------------------------
        self.timer = self.create_timer(0.02, self.control_loop)

        self.get_logger().info('🚀 Stage 2 Shape Controller service is ready on /shape_command')
        self.get_logger().info('Available shapes: "butterfly", "racecar" ("race car"), "ilros" ("i love ros"), "circle"')
        self.get_logger().info('Available controls: "pause", "resume", "reset", "stop"')

    def pose_callback(self, msg: Pose):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta

    # ====================================================
    # Service Callback
    # ====================================================
    def handle_command(self, request, response):
        raw_cmd = request.command.strip().lower()
        cmd = raw_cmd.replace('_', ' ').replace('-', ' ').strip()
        self.get_logger().info(f'Received command: "{raw_cmd}" (normalized: "{cmd}")')

        # PAUSE
        if cmd == 'pause':
            if self.state == 'RUNNING':
                self.state = 'PAUSED'
                self.cmd_vel_pub.publish(Twist())
                response.success = True
                response.message = f'Paused shape "{self.active_shape}".'
            elif self.state == 'PAUSED':
                response.success = True
                response.message = 'Turtle is already paused.'
            else:
                response.success = False
                response.message = 'No active shape is currently running to pause.'

        # RESUME / START
        elif cmd in ('resume', 'start', 'continue'):
            if self.state == 'PAUSED':
                self.state = 'RUNNING'
                response.success = True
                response.message = f'Resumed shape "{self.active_shape}".'
            elif self.state == 'RUNNING':
                response.success = True
                response.message = f'Shape "{self.active_shape}" is already running.'
            else:
                response.success = False
                response.message = 'No paused shape to resume. Choose "butterfly", "racecar", "ilros", or "circle" to start.'

        # RESET (Returns turtle to middle using teleport_absolute)
        elif cmd in ('reset', 'center'):
            self.reset_turtle()
            response.success = True
            response.message = 'Turtle teleported back to middle (5.54, 5.54) and canvas reset.'

        # STOP
        elif cmd == 'stop':
            self.state = 'IDLE'
            self.active_shape = None
            self.path = []
            self.path_index = 0
            self.t = 0.0
            self.cmd_vel_pub.publish(Twist())
            response.success = True
            response.message = 'Stopped movement and canceled shape.'

        # SHAPE 1: BUTTERFLY (FirstMasterPiece)
        elif cmd in ('butterfly', 'fly', 'shape 1', 'shape1'):
            self.start_butterfly()
            response.success = True
            response.message = 'Starting butterfly masterpiece (Stage 1 Shape 1)!'

        # SHAPE 2: RACECAR (SecondMasterPiece)
        elif cmd in ('racecar', 'race car', 'racecare', 'car', 'race', 'shape 2', 'shape2'):
            self.start_racecar()
            response.success = True
            response.message = 'Starting race car masterpiece (Stage 1 Shape 2)!'

        # SHAPE 3: I LOVE ROS (ThirdMasterPiece)
        elif cmd in ('ilros', 'i love ros', 'iloveros', 'love ros', 'i love', 'ros', 'love', 'shape 3', 'shape3'):
            self.start_ilros()
            response.success = True
            response.message = 'Starting "I LOVE ROS" cinematic masterpiece (Stage 1 Shape 3)!'

        # SIMPLE CIRCLE
        elif cmd == 'circle':
            self.state = 'RUNNING'
            self.active_shape = 'circle'
            response.success = True
            response.message = 'Starting circle shape!'

        else:
            response.success = False
            response.message = (
                f'Unknown command "{raw_cmd}". Valid options: '
                '"butterfly", "racecar" ("race car"), "ilros" ("i love ros"), '
                '"circle", "pause", "resume", "reset", "stop".'
            )

        return response

    # ====================================================
    # Shape Starters
    # ====================================================
    def start_butterfly(self):
        self.state = 'RUNNING'
        self.active_shape = 'butterfly'
        self.t = 0.0
        self.current_butterfly_color_idx = -1
        self.path = []
        self.path_index = 0
        self.set_butterfly_color(0)
        self.get_logger().info('🦋 Commenced Butterfly shape.')

    def start_racecar(self):
        self.path = self.build_racecar_path()
        self.path_index = 0
        self.active_shape = 'racecar'
        self.state = 'RUNNING'
        self.get_logger().info(f'🏎️ Commenced Race Car shape with {len(self.path)} waypoints.')

    def start_ilros(self):
        self.path = self.build_ilros_path()
        self.path_index = 0
        self.active_shape = 'ilros'
        self.state = 'RUNNING'
        self.get_logger().info(f'✨ Commenced "I LOVE ROS" shape with {len(self.path)} waypoints.')

    # ====================================================
    # Reset Turtle using TeleportAbsolute
    # ====================================================
    def reset_turtle(self):
        self.state = 'IDLE'
        self.active_shape = None
        self.path = []
        self.path_index = 0
        self.t = 0.0
        self.current_butterfly_color_idx = -1
        self.waiting_for_pen = False

        # Stop movement
        self.cmd_vel_pub.publish(Twist())

        # Call /turtle1/teleport_absolute to return turtle to center
        if self.teleport_client.service_is_ready():
            teleport_req = TeleportAbsolute.Request()
            teleport_req.x = 5.544445
            teleport_req.y = 5.544445
            teleport_req.theta = 0.0
            self.teleport_client.call_async(teleport_req)
            self.get_logger().info('Teleported turtle to center (5.54, 5.54).')
        else:
            self.get_logger().warn('/turtle1/teleport_absolute service is not ready yet!')

        # Clear canvas
        if self.clear_client.service_is_ready():
            clear_req = Empty.Request()
            self.clear_client.call_async(clear_req)
            self.get_logger().info('Cleared canvas via /clear.')

        # Reset pen
        self.request_pen(down=False, color='black', width=3)

    # ====================================================
    # Pen Management
    # ====================================================
    def request_pen(self, down: bool, color, width=None):
        if isinstance(color, str):
            rgb = self.color_palette.get(color, (255, 255, 255))
        elif isinstance(color, (tuple, list)):
            rgb = tuple(color)
        else:
            rgb = (255, 255, 255)

        if width is None:
            width = 4 if down else 1

        if (down == self.pen_is_down and rgb == self.pen_rgb and width == self.pen_width):
            return False

        if not self.pen_client.service_is_ready():
            return False

        request = SetPen.Request()
        request.r = int(rgb[0])
        request.g = int(rgb[1])
        request.b = int(rgb[2])
        request.width = int(width)
        request.off = 0 if down else 1

        future = self.pen_client.call_async(request)
        self.pending_pen_state = (down, rgb, width)
        self.waiting_for_pen = True
        future.add_done_callback(self.pen_response_callback)
        return True

    def pen_response_callback(self, future):
        if self.pending_pen_state:
            self.pen_is_down, self.pen_rgb, self.pen_width = self.pending_pen_state
        self.waiting_for_pen = False

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    # ====================================================
    # Butterfly Curve Math (FirstMasterPiece)
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

    def adaptive_t_step(self, t):
        probe_dt = 1e-4
        x1, y1 = self.butterfly(t)
        x2, y2 = self.butterfly(t + probe_dt)
        dx = (x2 - x1) * self.butterfly_scale
        dy = (y2 - y1) * self.butterfly_scale
        speed = math.hypot(dx, dy) / probe_dt
        speed = max(speed, 1e-3)
        step = self.desired_arc_length / speed
        return min(max(step, 0.001), 0.25)

    def set_butterfly_color(self, color_idx):
        if color_idx == self.current_butterfly_color_idx:
            return
        rgb = self.butterfly_colors[color_idx]
        self.request_pen(down=True, color=rgb, width=4)
        self.current_butterfly_color_idx = color_idx

    # ====================================================
    # Race Car Path Generator (SecondMasterPiece)
    # ====================================================
    def build_racecar_path(self):
        scale = 1.0
        center_x = 5.544445
        center_y = 5.544445

        def to_world(lx, ly):
            return center_x + scale * lx, center_y + scale * ly

        def shape_to_wp(local_points, color_name):
            wp = []
            first_x, first_y = to_world(*local_points[0])
            wp.append({'x': first_x, 'y': first_y, 'pen_down': False, 'color': color_name, 'width': 4})
            for lx, ly in local_points[1:]:
                wx, wy = to_world(lx, ly)
                wp.append({'x': wx, 'y': wy, 'pen_down': True, 'color': color_name, 'width': 4})
            return wp

        def circle_pts(cx, cy, r, steps=60):
            pts = []
            for i in range(steps):
                angle = 2 * math.pi * i / steps
                pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
            return pts

        path = []
        # 1. Car body
        body_local = [
            (-3.6, -0.6), (-3.6, 0.2), (-3.0, 0.5), (-2.6, 1.0),
            (-1.6, 1.5), (0.2, 1.6), (1.6, 1.3), (2.2, 0.7),
            (3.6, 0.5), (3.9, 0.1), (3.9, -0.6), (-3.6, -0.6)
        ]
        path += shape_to_wp(body_local, 'red')

        # 2. Rear spoiler
        spoiler_local = [
            (-3.4, 0.5), (-3.4, 1.3), (-2.7, 1.3), (-2.7, 1.0)
        ]
        path += shape_to_wp(spoiler_local, 'red')

        # 3. Racing stripe
        stripe_local = [
            (1.6, 1.2), (3.7, 0.25)
        ]
        path += shape_to_wp(stripe_local, 'black')

        # 4. Wheels
        wheel_radius = 0.9
        rear_wheel = (-2.3, -1.0)
        front_wheel = (2.3, -1.0)
        for cx, cy in (rear_wheel, front_wheel):
            c_pts = circle_pts(cx, cy, wheel_radius)
            c_pts.append(c_pts[0])
            path += shape_to_wp(c_pts, 'black')

        return path

    # ====================================================
    # "I LOVE ROS" Path Generator (ThirdMasterPiece)
    # ====================================================
    def build_ilros_path(self):
        scale = 0.85
        center_x = 5.544445
        center_y = 5.544445

        def to_world(lx, ly):
            return center_x + scale * lx, center_y + scale * ly

        def shape_to_wp(local_points, color_name):
            wp = []
            if not local_points:
                return wp
            first_x, first_y = to_world(*local_points[0])
            wp.append({'x': first_x, 'y': first_y, 'pen_down': False, 'color': color_name, 'width': 3})
            for lx, ly in local_points[1:]:
                wx, wy = to_world(lx, ly)
                wp.append({'x': wx, 'y': wy, 'pen_down': True, 'color': color_name, 'width': 3})
            return wp

        def generate_heart(cx, cy, radius, steps=50):
            pts = []
            for i in range(steps + 1):
                t = 2 * math.pi * i / steps
                x = radius * (16 * (math.sin(t) ** 3)) / 16.0
                y = radius * (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)) / 16.0
                pts.append((cx + x, cy + y))
            return pts

        def generate_star(cx, cy, outer_r, inner_r, points=5):
            pts = []
            total = points * 2
            for i in range(total + 1):
                angle = (i * math.pi / points) - (math.pi / 2)
                r = outer_r if i % 2 == 0 else inner_r
                pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
            return pts

        def generate_flower(cx, cy, r_petal, petals=5, steps_per_petal=12):
            pts = []
            total = petals * steps_per_petal
            for i in range(total + 1):
                theta = 2 * math.pi * i / total
                r = r_petal * (0.5 + 0.5 * math.fabs(math.sin(petals * theta / 2)))
                pts.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
            return pts

        path = []
        # LETTER 'I' (Cyan)
        letter_i = [
            (-5.0, 3.2), (-3.8, 3.2), (-4.4, 3.2), (-4.4, 1.2), (-5.0, 1.2), (-3.8, 1.2)
        ]
        path += shape_to_wp(letter_i, 'cyan')

        # HEART SHAPE (Neon Pink)
        heart_pts = generate_heart(cx=-2.0, cy=2.2, radius=1.2)
        path += shape_to_wp(heart_pts, 'neon_pink')

        # LETTER 'R' (Gold)
        letter_r = [
            (0.0, 1.2), (0.0, 3.2), (1.0, 3.2), (1.3, 2.7),
            (1.0, 2.2), (0.0, 2.2), (0.6, 2.2), (1.4, 1.2)
        ]
        path += shape_to_wp(letter_r, 'gold')

        # LETTER 'O' (Gold)
        letter_o = []
        steps = 30
        for i in range(steps + 1):
            angle = 2 * math.pi * i / steps
            letter_o.append((2.6 + 0.7 * math.cos(angle), 2.2 + 1.0 * math.sin(angle)))
        path += shape_to_wp(letter_o, 'gold')

        # LETTER 'S' (Gold)
        letter_s = [
            (4.8, 3.0), (4.2, 3.2), (3.7, 2.8), (4.7, 2.2),
            (3.7, 1.6), (4.3, 1.2), (4.8, 1.4)
        ]
        path += shape_to_wp(letter_s, 'gold')

        # DECORATIVE FLOWERS (Magenta)
        path += shape_to_wp(generate_flower(cx=-3.5, cy=-1.5, r_petal=0.9, petals=5), 'magenta')
        path += shape_to_wp(generate_flower(cx=3.5, cy=-1.5, r_petal=0.9, petals=5), 'magenta')

        # DECORATIVE STARS (Soft Yellow)
        path += shape_to_wp(generate_star(cx=-1.2, cy=-2.0, outer_r=0.7, inner_r=0.3), 'soft_yellow')
        path += shape_to_wp(generate_star(cx=0.0, cy=-1.0, outer_r=0.9, inner_r=0.4), 'soft_yellow')
        path += shape_to_wp(generate_star(cx=1.2, cy=-2.0, outer_r=0.7, inner_r=0.3), 'soft_yellow')

        return path

    # ====================================================
    # Main Control Loop
    # ====================================================
    def control_loop(self):
        if self.state != 'RUNNING':
            return

        # Simple circle
        if self.active_shape == 'circle':
            msg = Twist()
            msg.linear.x = 2.0
            msg.angular.z = 2.0
            self.cmd_vel_pub.publish(msg)
            return

        # Butterfly
        if self.active_shape == 'butterfly':
            bx, by = self.butterfly(self.t)
            target_x = 5.544445 + self.butterfly_scale * bx
            target_y = 5.544445 + self.butterfly_scale * by

            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)

            if distance < self.butterfly_threshold:
                self.t += self.adaptive_t_step(self.t)

                progress = self.t / self.max_t
                c_idx = min(int(progress * len(self.butterfly_colors)), len(self.butterfly_colors) - 1)
                self.set_butterfly_color(c_idx)

                if self.t >= self.max_t:
                    self.cmd_vel_pub.publish(Twist())
                    self.state = 'IDLE'
                    self.active_shape = None
                    self.get_logger().info('🦋 Butterfly masterpiece complete!')
                    return

            target_angle = math.atan2(dy, dx)
            angle_error = self.normalize_angle(target_angle - self.theta)
            heading_factor = max(math.cos(angle_error), 0.0)

            msg = Twist()
            msg.linear.x = min(6.0 * distance * heading_factor, 6.0)
            msg.angular.z = max(min(10.0 * angle_error, 10.0), -10.0)
            self.cmd_vel_pub.publish(msg)
            return

        # Waypoint-following shapes (RaceCar and ILROS)
        if self.active_shape in ('racecar', 'ilros'):
            if self.waiting_for_pen:
                self.cmd_vel_pub.publish(Twist())
                return

            if self.path_index >= len(self.path):
                self.cmd_vel_pub.publish(Twist())
                self.state = 'IDLE'
                shape_name = self.active_shape
                self.active_shape = None
                self.get_logger().info(f'🎉 Shape "{shape_name}" complete!')
                return

            target = self.path[self.path_index]

            if self.request_pen(target['pen_down'], target['color'], target.get('width', 3)):
                self.cmd_vel_pub.publish(Twist())
                return

            dx = target['x'] - self.x
            dy = target['y'] - self.y
            distance = math.hypot(dx, dy)

            if distance < self.waypoint_threshold:
                self.path_index += 1
                return

            target_angle = math.atan2(dy, dx)
            angle_error = self.normalize_angle(target_angle - self.theta)
            heading_factor = max(math.cos(angle_error), 0.0)

            if self.active_shape == 'racecar':
                max_linear = 3.0
                max_angular = 8.0
                k_linear = 4.0
                k_angular = 8.0
            else:  # ilros
                max_linear = 2.5
                max_angular = 7.0
                k_linear = 3.5
                k_angular = 7.0

            msg = Twist()
            msg.linear.x = min(k_linear * distance * heading_factor, max_linear)
            msg.angular.z = max(min(k_angular * angle_error, max_angular), -max_angular)
            self.cmd_vel_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Stage2Controller()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

