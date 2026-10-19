import sys
import termios
import tty

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

instruction_msg = """
---------------------------------------------
Control the Turtle with Arrow Keys!
---------------------------------------------
   (↑) Up Arrow    : Move Forward
   (↓) Down Arrow  : Move Backward
   (←) Left Arrow  : Rotate Counter-Clockwise
   (→) Right Arrow : Rotate Clockwise

Press CTRL+C to exit.
---------------------------------------------
"""


class TurtleKeyboardTeleop(Node):

  def __init__(self):
    super().__init__('turtle_keyboard_teleop')
    # Publish to turtlesim's velocity topic
    self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
    self.get_logger().info(instruction_msg)

  def get_key(self):
    """Captures raw keyboard inputs from the terminal without pressing Enter."""
    settings = termios.tcgetattr(sys.stdin)
    try:
      tty.setraw(sys.stdin.fileno())
      key = sys.stdin.read(1)
      if key == '\x1b':  # Handle multi-byte arrow key escape sequences
        key += sys.stdin.read(2)
    finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

  def run(self):
    try:
      while rclpy.ok():
        key = self.get_key()
        twist = Twist()

        # Map arrow keys to Twist velocities
        if key == '\x1b[A':  # Up Arrow
          twist.linear.x = 2.0
          twist.angular.z = 0.0
          self.get_logger().info('Moving Forward')
        elif key == '\x1b[B':  # Down Arrow
          twist.linear.x = -2.0
          twist.angular.z = 0.0
          self.get_logger().info('Moving Backward')
        elif key == '\x1b[D':  # Left Arrow
          twist.linear.x = 0.0
          twist.angular.z = 2.0
          self.get_logger().info('Turning Left')
        elif key == '\x1b[C':  # Right Arrow
          twist.linear.x = 0.0
          twist.angular.z = -2.0
          self.get_logger().info('Turning Right')
        elif key == '\x03':  # Ctrl+C
          break
        else:
          continue

        self.publisher_.publish(twist)
    except Exception as e:
      self.get_logger().error(f'{e}')


def main(args=None):
  rclpy.init(args=args)
  teleop_node = TurtleKeyboardTeleop()
  teleop_node.run()
  teleop_node.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
  main()