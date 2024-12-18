#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

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

class SquareNode(Node):
    def __init__(self):
        super().__init__("square")
        self.cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.get_logger().info("Square Node has been started")

        self.create_timer(0.1, self.timer_callback)

        self.trajectory_ = []
        self.trajectory_.append( TrajectoryPoint( 0.25,  0.00, 0.00, 20) )
        self.trajectory_.append( TrajectoryPoint( 0.00, -0.25, 0.00, 20) )
        self.trajectory_.append( TrajectoryPoint(-0.25,  0.00, 0.00, 20) )
        self.trajectory_.append( TrajectoryPoint( 0.00,  0.25, 0.00, 20) )
        self.trajectory_.append( TrajectoryPoint( 0.00,  0.00, 0.00, 20) )

        self.counter_ = -1

    def timer_callback(self):

        # Détection première itération
        if (self.counter_ == -1):
            self.counter_ = 0
            self.step_ = self.trajectory_[self.counter_]
            self.get_logger().info("Etape "+str(self.counter_))

        if (self.counter_ >= 0):
            msg = self.step_.msg()
            self.step_.duration_dec()
            self.cmd_vel_pub.publish(msg)
            if ( self.step_.expired() ):
                self.counter_ = self.counter_ + 1
                if ( self.counter_ < len(self.trajectory_) ):
                    self.step_ = self.trajectory_[self.counter_]
                    self.get_logger().info("Etape "+str(self.counter_))
                else:
                    self.counter_ = -100

def main(args=None):
    rclpy.init(args=args) # initialisation comm ROS2

    node = SquareNode()
    rclpy.spin(node)

    rclpy.shutdown() # Shutdown node

if __name__== '__main__':
    main()
