import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

from rclpy.qos import QoSProfile, ReliabilityPolicy, LivelinessPolicy, DurabilityPolicy, HistoryPolicy, QoSDurabilityPolicy, QoSHistoryPolicy

custom_qos_profile = QoSProfile(
	reliability=ReliabilityPolicy.BEST_EFFORT,
	durability=DurabilityPolicy.VOLATILE,
	history=HistoryPolicy.KEEP_LAST,
	depth=10,
	#deadline=Duration(seconds=1),
	liveliness=LivelinessPolicy.AUTOMATIC
	)


class IceBrgidge(Node):

	def __init__(self):
		super().__init__('icethimble_bridge')
		self.publisher_ = self.create_publisher(Twist, 'finger_force', 10)
		timer_period = 0.1
		self.timer = self.create_timer(timer_period, self.pub_force_callback)
		self.rec_msg = Twist()

		self.subscription = self.create_subscription(
			Twist,
			'finger_force_dongle',
			self.read_dongle,
			custom_qos_profile)

		self.get_logger().info('IceBridge initiated')

	def pub_force_callback(self):
		msg = Twist()
		msg = self.rec_msg
		self.publisher_.publish(msg)
		#self.get_logger().info('Published: "%i"',msg.linear.x)

	def read_dongle(self, msg):
		self.rec_msg = msg
		#print(msg.linear.z)



def main(args=None):
	rclpy.init(args=args)

	bridge_ice = IceBrgidge()

	rclpy.spin(bridge_ice)

	bridge_ice.destroy_node()

	rclpy.shutdown()


if __name__ == '__main__':
	main()