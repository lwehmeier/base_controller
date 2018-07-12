#!/usr/bin/python
import math
from math import sin, cos, pi, radians, sqrt
import rospy
import tf
import numpy as np
from std_msgs.msg import Float32, Int16
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import struct
v_scale = 1000 #0.01ms = speed1, 00.1ms = speed 100
def callback(twist):
    vx = twist.linear.x
    vy = twist.linear.y
    th = twist.angular.z
    val = sqrt(vx*vx+vy*vy)
    direction = np.arccos(vx/val)
    speed_pub.publish(Int16(val*scale))
    direction_pub.publish(Int16(direction/pi*180))
    if val > 0.01 :
        go_pub.publish(Int16(1))
    else :
        go_pub.publish(Int16(0))
    angular_pub.publish(Int16(th/pi*180)) #need deg per second



rospy.init_node('odom')
global speed_pub
global direction_pub
global angular_pub
global go_pub
go_pub = rospy.Publisher("/platform/go", Int16, queue_size=3)
speed_pub = rospy.Publisher("/platform/speed", Int16, queue_size=3)
direction_pub = rospy.Publisher("/platform/direction", Int16, queue_size=3)
angular_pub = rospy.Publisher("/platform/theta", Int16, queue_size=3)
rospy.Subscriber("/cmd_vel", Twist, callback)
r = rospy.Rate(10) # 10hz
rospy.spin()
