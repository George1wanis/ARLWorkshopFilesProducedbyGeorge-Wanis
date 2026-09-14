import sys
import rclpy
from rclpy.node import Node
from turtle_interfaces.srv import ShapeCommand


class Stage2Client(Node):

    def __init__(self):
        super().__init__('stage2_client')
        self.client = self.create_client(ShapeCommand, '/shape_command')

        while not self.client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('Waiting for /shape_command service to become available...')

    def send_command(self, command: str):
        req = ShapeCommand.Request()
        req.command = command
        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    client_node = Stage2Client()

    # If arguments are passed on command line: ros2 run turtle_controller stage2_client <cmd>
    cmd_args = sys.argv[1:]
    if cmd_args:
        cmd = ' '.join(cmd_args)
        response = client_node.send_command(cmd)
        if response:
            status = 'SUCCESS' if response.success else 'FAILED'
            print(f'[{status}] Response: {response.message}')
    else:
        # Interactive loop
        print('=== Turtle Shape Controller Client ===')
        print('Available shapes: butterfly, racecar (race car), ilros (i love ros), circle')
        print('Available controls: pause, resume, reset, stop, exit')
        try:
            while rclpy.ok():
                user_input = input('Enter command > ').strip()
                if not user_input:
                    continue
                if user_input.lower() in ('exit', 'quit', 'q'):
                    break
                response = client_node.send_command(user_input)
                if response:
                    status = 'SUCCESS' if response.success else 'FAILED'
                    print(f'[{status}] Response: {response.message}')
        except (KeyboardInterrupt, EOFError):
            pass

    client_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
