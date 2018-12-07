#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
PI = 3.1415926535897

posicion = Odometry()

def callback_pose(data):
    global posicion
    posicion = data
    # print "data" ,  posicion.pose.pose.orientation.z


def move():
    # Starts a new node
    rospy.init_node('robot_cuadrado', anonymous=True)
    rate = rospy.Rate(10)
    
    # velocity_publisher = rospy.Publisher('/komodo_1/cmd_vel', Twist, queue_size=10)
    velocity_publisher = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size=10)
    pose_subscriber = rospy.Subscriber(
                '/mobile_base_controller/odom', Odometry, callback_pose)
    vel_msg = Twist()
    speed = 0.1
    speed_move = 0.1#0.1
    distance=0.5
    angle = 88 # math.pi/2
    angular_speed = speed*2*PI/360*100
    relative_angle = angle*2*PI/360

    
    
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0


    for i in range(1):
        print "iteracion ",i 
        vel_msg.linear.x = 0

        while(posicion.pose.pose.position.x==0):
            continue
        #Setting the current time for distance calculus
        t0 = float(rospy.Time.now().to_sec())
        current_distance = 0
        recorrido_total= abs(posicion.pose.pose.position.x)+distance
        # print posicion.pose.pose.position.x,' ',recorrido_total
        # #Loop to move the turtle in an specified distance
        # while(abs(posicion.pose.pose.position.x) < recorrido_total):
        #     print "es menor"
        #     print posicion.pose.pose.position.x
        #     #Publish the velocity
        #     velocity_publisher.publish(vel_msg)
        #     rate.sleep()
        #     #Takes actual time to velocity calculus
        #     t1=float(rospy.Time.now().to_sec())
        #     #Calculates distancePoseStamped
        #     current_distance= speed_move*(t1-t0)
        # print posicion.pose.pose.position.x,' ',recorrido_total
        # vel_msg.linear.x = 0
        # velocity_publisher.publish(vel_msg)
        # rate.sleep()

        vel_msg.angular.z=(angular_speed)

        angulo_z =0# posicion.pose.pose.orientation.z+relative_angle
        
        current_angle = abs(posicion.twist.twist.angular.z)
        t0 = rospy.Time.now().to_sec()
        while(current_angle+abs(posicion.twist.twist.angular.z)/2< relative_angle): #(angulo_z > posicion.pose.pose.orientation.z):
            # print "velocidad", current_angle, ' ' , relative_angle ,' ' ,posicion.twist.twist.angular.z
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = abs(posicion.twist.twist.angular.z)*(t1-t0)
            rate.sleep()

            # current_angle = angular_speed*(t1-t0)
        
        vel_msg.angular.z = 0
        velocity_publisher.publish(vel_msg)
        rate.sleep()
        


if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass

