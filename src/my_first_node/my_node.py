import rclpy
from rclpy.node import Node


class MyNode(Node):

    def __init__(self):
        super().__init__('my_first_node')

        self.get_logger().info('Hello from my node!')


def main(args=None):

    # 1. Initialize rclpy
    rclpy.init(args=args)

    # 2. Inistantiates a "node" object from the "MyNode" class which enharites from the "Node" parent class
    node = MyNode()

    # 3. Process callbacks
    rclpy.spin(node)

    # 4. Destroy the "node" object
    node.destroy_node()

    # 5. Shutdown rclpy
    rclpy.shutdown()


if __name__ == '__main__':
    main()
