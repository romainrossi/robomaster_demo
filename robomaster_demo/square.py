#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SquareNode(Node):
    def __init__(self):
        super().__init__("square")
        self.cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.get_logger().info("Square Node has been started")
        self.counter_ = 0
        self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        if ( self.counter_ >= 0 and self.counter_ <20 ):
            self.get_logger().info("Etape 1")
            msg.linear.x = 0.25
            msg.linear.y = 0.0
            msg.angular.z = 0.0
        if ( self.counter_ >= 20 and self.counter_ <40 ):
            self.get_logger().info("Etape 2")
            msg.linear.x = 0.0
            msg.linear.y = -0.25
            msg.angular.z = 0.0
        if ( self.counter_ >= 40 and self.counter_ <60 ):
            self.get_logger().info("Etape 3")
            msg.linear.x = -0.25
            msg.linear.y = 0.0
            msg.angular.z = 0.0
        if ( self.counter_ >= 60 and self.counter_ <80 ):
            self.get_logger().info("Etape 4")
            msg.linear.x = 0.0
            msg.linear.y = 0.25
            msg.angular.z = 0.0
        if ( self.counter_ >= 80 ):
            self.get_logger().info("Etape 5")
            msg.linear.x = 0.0
            msg.linear.y = 0.0
            msg.angular.z = 0.0
        self.cmd_vel_pub.publish(msg)
        self.counter_ = self.counter_ + 1

def main(args=None):
    rclpy.init(args=args) # initialisation comm ROS2

    node = SquareNode()
    rclpy.spin(node)

    rclpy.shutdown() # Shutdown node

if __name__== '__main__':
    main()
