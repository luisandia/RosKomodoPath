#!/usr/bin/env python
import rospy
from math import *
import abc
PI = 3.1415926535897
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from nav_msgs.msg import Odometry
from collections import defaultdict


class BaseSubsPUbls():

    def __init__(self, modeSimulator=True):
        # Creating our node,publisher and subscriber
        if modeSimulator:
            rospy.init_node('komodo_simulador_controller', anonymous=True)
            self.velocity_publisher = rospy.Publisher(
                '/mobile_base_controller/cmd_vel', Twist, queue_size=10)
            self.pose_subscriber = rospy.Subscriber(
                '/URF/rear', Range, self.callback_rear)
            self.pose_subscriber = rospy.Subscriber(
                '/URF/left', Range, self.callback_left)
            self.pose_subscriber = rospy.Subscriber(
                '/URF/right', Range, self.callback_right)
            self.pose_subscriber = rospy.Subscriber(
                '/mobile_base_controller/odom', Odometry, self.callback_pose)
            self.cloud_subscriber = rospy.Subscriber(
                '/camera/depth/color/points', PointCloud2, self.callback_cloud)
        else:
            rospy.init_node('komodo_real_controller', anonymous=True)
            # self.velocity_publisher = rospy.Publisher(
            #     '/komodo_1/diff_driver/command', Twist, queue_size=10)
            self.velocity_publisher = rospy.Publisher(
                '/komodo_1/cmd_vel', Twist, queue_size=10)
            self.pose_subscriber = rospy.Subscriber(
                '/komodo_1/Rangers/Rear_URF', Range, self.callback_rear)
            self.pose_subscriber = rospy.Subscriber(
                '/komodo_1/Rangers/Left_URF', Range, self.callback_left)
            self.pose_subscriber = rospy.Subscriber(
                '/komodo_1/Rangers/Right_URF', Range, self.callback_right)
            self.pose_subscriber = rospy.Subscriber(
                '/komodo_1/odom_pub', Odometry, self.callback_pose)
            self.cloud_subscriber = rospy.Subscriber(
                '/depth_camera/points', PointCloud2, self.callback_cloud)

        # poner en escala de grises
        # y representar de acuerdo al mundo real
        # 10x10 seria un cuadrado
        self.rear = Range()
        self.left = Range()
        self.right = Range()
        self.posicion = Odometry()
        self.cloud = PointCloud2()
        self.lista_final = defaultdict(list)
        self.odom_x = self.odom_y = 0

        # self.pose = Range()
        self.rate = rospy.Rate(10)
        self.vel_msg = Twist()

    def callback_rear(self, data):
        self.rear = data

    def callback_left(self, data):
        self.left = data

    def callback_right(self, data):
        self.right = data

    def callback_pose(self, data):
        self.posicion = data
        self.odom_x = self.posicion.pose.pose.position.x
        self.odom_y = self.posicion.pose.pose.position.y

    def callback_cloud(self, msg):
        self.cloud = msg

    def move_distance(self, distance, speed=0.1):

        # recorrido_total = abs(self.posicion.pose.pose.position.x)+distance
        # print self.posicion.pose.pose.position.x, ' ', recorrido_total
        self.vel_msg.linear.x = speed
        current_distance = abs(self.posicion.twist.twist.linear.x)
        t0 = rospy.Time.now().to_sec()
        while(current_distance<distance): #(angulo_z > self.posicion.pose.pose.orientation.z):
            print "velocidad", current_distance, ' ', distance, ' ', self.posicion.twist.twist.linear.x
            self.velocity_publisher.publish(self.vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_distance = abs(self.posicion.twist.twist.linear.x)*(t1-t0)
            self.rate.sleep()
    
        self.vel_msg.linear.x = 0
        self.velocity_publisher.publish(self.vel_msg)
        self.rate.sleep()

    def girar(self, angle, speed=0.1):
        angle=angle-2
        angular_speed = speed*2*pi/360*100
        relative_angle = angle*2*pi/360

        self.vel_msg.angular.z = angular_speed
        current_angle = abs(self.posicion.twist.twist.angular.z)
        t0 = rospy.Time.now().to_sec()
        while(current_angle+abs(self.posicion.twist.twist.angular.z)/2< relative_angle): #(angulo_z > self.posicion.pose.pose.orientation.z):
            # print "velocidad", angular_speed, ' ' , self.posicion.twist.twist.angular.z
            self.velocity_publisher.publish(self.vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = abs(self.posicion.twist.twist.angular.z)*(t1-t0)
            self.rate.sleep()
            # current_angle = angular_speed*(t1-t0)

        self.vel_msg.angular.z = 0
        self.velocity_publisher.publish(self.vel_msg)
        self.rate.sleep()

    @abc.abstractmethod
    def interactua(self):
        print "base interactua"
        return
