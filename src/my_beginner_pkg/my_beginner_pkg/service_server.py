from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class ServiceServer(Node):

  def __init__(self):
    super().__init__('add_ints_server')
    self.srv = self.create_service(
        AddTwoInts, 'add_two_ints', self.add_two_ints_callback
    )
    self.get_logger().info('Add Two Ints Service Ready.')

  def add_two_ints_callback(self, request, response):
    response.sum = request.a + request.b
    self.get_logger().info(f'Incoming request: {request.a} + {request.b}')
    return response


def main(args=None):
  rclpy.init(args=args)
  node = ServiceServer()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()