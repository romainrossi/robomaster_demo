#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import robomaster_msgs.msg

class TrajectoryPoint():
    def __init__(self, vx, vy, rz, duration_s):
        self.msg_ = Twist()
        self.msg_.linear.x = vx
        self.msg_.linear.y = vy
        self.msg_.angular.z = rz
        self.duration_s_ = duration_s

    def msg(self):
        return self.msg_
    def duration(self):
        return self.duration_s_
    def duration_dec(self):
        self.duration_s_ = self.duration_s_ - 1
    def expired(self):
        return self.duration_s_ == 0

class ReactNode(Node):
    def __init__(self):
        super().__init__("react")
        self.cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.cmd_arm_pub = self.create_publisher(Twist, "/cmd_arm", 10)
        self.vision_sub = self.create_subscription(robomaster_msgs.msg.Detection, "/vision", self.vision_marker_cb, 10)

        self.get_logger().info("React Node has been started")

        self.create_timer(0.1, self.timer_callback)

        self.step_ = TrajectoryPoint( 0.25,  0.00, 0.00, 20)

    def vision_marker_cb(self, msg: robomaster_msgs.msg.Detection):
        markers = msg.markers
        for m in markers:
            r = m.roi
            #self.get_logger().info("Detection : " + str(m.kind))

            if (m.kind == "1"):
                if (0.4 < r.x_offset ) and (r.x_offset < 0.6):
                    self.get_logger().info("ping")
                    self.step_ = TrajectoryPoint( 0.0,  0.3, 0.00, 50)
            if (m.kind == "2"):
                if (0.4 < r.x_offset ) and (r.x_offset < 0.6):
                    self.get_logger().info("pong")
                    self.step_ = TrajectoryPoint( 0.0,  -0.2, 0.00, 50)

    def timer_callback(self):
        if ( not self.step_.expired() ):
            msg = self.step_.msg()
            self.cmd_vel_pub.publish(msg)
            self.step_.duration_dec()

def main(args=None):
    rclpy.init(args=args) # initialisation comm ROS2

    node = ReactNode()
    rclpy.spin(node)

    rclpy.shutdown() # Shutdown node

if __name__== '__main__':
    main()
