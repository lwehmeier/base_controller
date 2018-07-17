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
MAX_X = 0.15
MAX_Y = 0.15
MAX_THETA = 0.2
update_rate = 0.5
v_scale = 100 #0.01ms = speed1, 00.1ms = speed 100
global is_go
is_go=True
global last_twist
last_twist=Twist()
global last_cmd
last_cmd = Vector3()
global stop
stop=False
def callback(twist):
    global last_twist
    last_twist=twist
def e_stop(data):
    global stop
    if data.data > 0:
        stop = True
        print("EMERGENCY STOP TRIGGERED. Stopping...")
        go_pub.publish(Int16(0))
    else:
        stop = False
def update_grisp(event):
    if stop:
        speed_pub.publish(Vector3(0,0,0))
        go_pub.publish(Int16(0))
        return
    twist = last_twist
    global is_go
    global last_cmd
    vx = twist.linear.x
    vy = twist.linear.y
    th = twist.angular.z
    new_cmd = Vector3()
    new_cmd.x = vx if vx <= MAX_X else MAX_X
    new_cmd.y = vy if vy <= MAX_Y else MAX_Y
    new_cmd.z = th if th <= MAX_THETA else MAX_THETA
        #speed_pub.publish(Int16(2+val*v_scale))
        #print(2+val*v_scale)
        #direction_pub.publish(Int16(direction/pi*180))
        #if not is_go:
        #    go_pub.publish(Int16(1))
        #    is_go=True
    #else :
        #if is_go:
        #    go_pub.publish(Int16(0))
        #    is_go=False
    #if th != 0.0:
    #    if not is_go:
    #        go_pub.publish(Int16(1))
    #        is_go=True
    #    angular_pub.publish(Int16(th/pi*180)) #need deg per second
    if new_cmd.x != 0.0 or new_cmd.z != 0.0 or new_cmd.y != 0:
        if new_cmd.x != last_cmd.x or new_cmd.y != last_cmd.y or new_cmd.z != last_cmd.z:
            print("update")
            last_cmd = new_cmd
            speed_pub.publish(new_cmd)
            #direction_pub.publish(Int16(new_cmd.y))
            #angular_pub.publish(Int16(new_cmd.z)) #need deg per second
            if not is_go:
                go_pub.publish(Int16(1))
                print("go")
                is_go = True
    else:
        if is_go and new_cmd.x == 0.0 and new_cmd.z == 0.0 and new_cmd.y == 0.0:
            go_pub.publish(Int16(0))
            print("stop")
            is_go = False


rospy.init_node('base_controller')
global speed_pub
global direction_pub
global angular_pub
global go_pub
go_pub = rospy.Publisher("/platform/go", Int16, queue_size=3)
speed_pub = rospy.Publisher("/platform/combined", Vector3, queue_size=3)
rospy.Subscriber("/cmd_vel", Twist, callback)
rospy.Subscriber("/platform/e_stop", Int16, e_stop)
r = rospy.Rate(10) # 10hz
rospy.Timer(rospy.Duration(0.8),update_grisp)
rospy.spin()
