#!/usr/bin/env python

import rospy

import mapa_ocupacion
import base_subs_publ
from math import *
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from sensor_msgs import point_cloud2
import threading
import logging
from MatrizDH import *
import os

class Lab8(base_subs_publ.BaseSubsPUbls):

    def __init__(self, square_size=0.10):
        base_subs_publ.BaseSubsPUbls.__init__(self, True)
        self.fin_hilo = True
        self.movement_stop = False
        self.width = square_size
        self.height = square_size
        self.x = 10
        self.y = 10
        self.speed=0.1
        self.speed_move=0.1
        self.mapa = mapa_ocupacion.MapaOcupacion(
            200, 200, self.width, self.height, self.x, self.y)
        self.angular_speed = self.speed*2*pi/360
        self.alpha = 0.01
        self.square_x = square_size

        # set matrixdh

        # theta1 = pi/2
        # theta2 = -pi/2
        # theta3 = pi/2
        # theta4 = -pi/2
        # theta5 = pi/3

        theta1 = pi/4
        theta2 = 2*(pi/3)
        theta3 = -pi/8
        theta4 = pi/5
        theta5 = -3*(pi/4)

        self.matrix_DH = ArticulacionKomodo()  # a d alpha theta
        self.matrix_DH.setArticulacion_1(0.0, 13.8, 0.0, theta1)
        self.matrix_DH.setArticulacion_2(0.0, 0.0, -pi/2, -pi/2+theta2)
        self.matrix_DH.setArticulacion_3(27.0,  0.0, -pi/2, -theta3)
        self.matrix_DH.setArticulacion_4(22.3,  0.0, -pi/2, -pi/2-theta4)
        self.matrix_DH.setArticulacion_5(1.0, 24.0, -pi/2, theta5)
        self.matrix_DH.setCamara(-6.5, 4.5, 0.0, 0.0)
        print self.matrix_DH.getMultiMatrix()

    def getProbabilidad(self, x, y, val_sensor):
        ve = self.mapa.getValue(x, y)
        if ve:
            ve = 1
        else:
            ve = 0

        return ve + self.alpha*(val_sensor-ve)

    def setProbabilidad(self, x, y, val_sensor):
        # ve= self.mapa.getValue(x,y)
        self.mapa.setCoord(x, y, val_sensor)

    def scan(self, sensor_ultrasonido, orientacion):
        puntos = open(
            '/home/it-grupo/luis/10semestre/robotica_/final_ros/puntosmapa.txt', 'a+')
        if sensor_ultrasonido >= 0.01 and sensor_ultrasonido <= 2.0:

            posicion = 0
            tmp = 0
            str_color = ""
            while tmp < sensor_ultrasonido:
                posicion += 1
                tmp += self.square_x
            if orientacion == "r":
                y_final = self.y+posicion
                x_final = self.x
                prob = self.getProbabilidad(
                    x_final, y_final, sensor_ultrasonido)
                self.setProbabilidad(x_final, y_final, prob)
                prob = self.getProbabilidad(
                    x_final, y_final, sensor_ultrasonido)
                intensidad = 255*(1-prob)
                str_color = str(intensidad)+',' + \
                    str(intensidad)+','+str(intensidad)
            elif orientacion == "l":
                y_final = self.y-posicion
                x_final = self.x
                prob = self.getProbabilidad(
                    x_final, y_final, sensor_ultrasonido)
                self.setProbabilidad(x_final, y_final, prob)
                prob = self.getProbabilidad(
                    x_final, y_final, sensor_ultrasonido)
                intensidad = 255*(1-prob)
                str_color = '0,'+str(intensidad)+',0'
            elif orientacion == "b":
                x_final = self.x-posicion
                y_final = self.y
                str_color = "0,0,1"
            else:
                # para posicionar arriba
                y_final = self.y
                x_final = self.x-posicion
                str_color = "1,0,0"

            print "obstaculo %f en %s" % (
                sensor_ultrasonido, orientacion), posicion, '(', x_final, '...', y_final, ')'
            # if x_final != self.x or self.y != y_final:

            print "escribiendo"
            puntos.write(str(x_final) + ',' +
                         str(y_final) + ','+str_color+'\n')
        puntos.close()
        return True

    def scan_top(self, p_z, p_x):
        puntos = open(
            '/home/it-grupo/luis/10semestre/robotica_/final_ros/puntosmapa.txt', 'a+')
        if p_z >= 0.01 and p_z <= 2.0:
            posicion = 0
            tmp = 0
            while tmp < p_z:
                posicion += 1
                tmp += self.square_x
            x_final = self.x+posicion

            if x_final != self.x:
                prob = self.getProbabilidad(
                    x_final, self.y, p_z)
                self.setProbabilidad(x_final, self.y, prob)

            tmp = 0
            posicion_y = 0
            while tmp <= abs(p_x):
                posicion_y += 1
                tmp += self.square_x

            # print "mi position_y",posicion_y
            if posicion_y != self.y:
                y_final = self.y-posicion_y if p_x < 0 else self.y+posicion_y

            # y_final = int(abs(self.y+p_x))

            # print "obstaculo %f en %f" % (
            #     p_z, p_x), posicion, '(', x_final, '...', y_final, ')'
            # if x_final != self.x or self.y != y_final:
            prob = self.getProbabilidad(
                x_final, y_final, p_z)
            self.setProbabilidad(x_final, y_final, prob)
            prob = self.getProbabilidad(
                x_final, y_final, p_z)
            intensidad = 256*(1-prob)
            puntos.write(str(x_final) + ',' + str(y_final) +
                        ','+str(intensidad)+',0,0' + '\n')
            puntos.close()

    def scan_cloud(self, msg,my_pos_x):
        import os
        # print(msg.height, "  ", msg.width)
        f = open(
            '/home/it-grupo/luis/10semestre/robotica_/final_ros/nube1metro.txt', 'w')
        temp_x = 0
        # self.lista_final.clear()
        lista_grafico = dict()
        for point in point_cloud2.read_points(msg, skip_nans=False):
            p_x = point[0]
            p_y = point[1]
            p_z = point[2]
            # print p_y
            if self.fin_hilo:
                print "fin de hilo por nuevo punto"
                return True
            # a menos de 0.70 se vuelve ciego
            # p_z<0.60:#abs(p_y)>0.20:# and p_y>0.20:
            if str(p_z) != 'nan' and abs(p_x) < 0.30 and p_z < 3.4:
                # print('{0:.2f}'.format(round(p_x,2))," ",'{0:.2f}'.format(round(p_y,2))," ",'{0:.2f}'.format(round(p_z,2)))

                if p_y < 0.1 and p_z < 3:
                    # print('{0:.2f}'.format(round(p_x,2))," ",'{0:.2f}'.format(round(p_y,2))," ",'{0:.2f}'.format(round(p_z,2)))

                    if temp_x != (round(p_x, 2)) and (round(p_x, 2)) not in lista_grafico:
                        temp_x = (round(p_x, 2))
                        self.scan_top(p_z, p_x)
                    if  my_pos_x not in self.lista_final:
                        self.lista_final[my_pos_x].append(p_x)
                        self.lista_final[my_pos_x].append(p_y)
                        self.lista_final[my_pos_x].append(p_z)
                        print('{0:.2f}'.format(round(p_x, 2)), " ", '{0:.2f}'.format(
                        round(p_y, 2)), " ", '{0:.2f}'.format(round(p_z, 2)))
                        self.scan_top(p_z, p_x)


                    if p_z < 0.67:
                        print "fin"
                        # print('{0:.2f}'.format(round(p_x, 2)), " ", '{0:.2f}'.format(
                        #     round(p_y, 2)), " ", '{0:.2f}'.format(round(p_z, 2)))
                        self.movement_stop = True
                        self.fin_hilo = True
                        return True
                        # break
                else:
                    print "salgo"
                    # print('{0:.2f}'.format(round(p_x,2))," ",'{0:.2f}'.format(round(p_y,2))," ",'{0:.2f}'.format(round(p_z,2)))
                    break
                    # self.fin_hilo=True
            f.write(str(p_x) + ',' + str(p_y) + ','+str(p_z) + '\n')

        print("----------------------EOF---------------------------------------")
        self.movement_stop = False
        self.fin_hilo = True
        return False

    def procesaPuntos(self, puntos):
        max_y=0
        for x,vals in puntos.iteritems():
            print x,vals
            if (abs(vals[1])>max_y ):
                max_y=abs(vals[1])
        print "altura: ",max_y*100," , brazo:",self.matrix_DH.getMultiMatrix().item(1,3)+30,max_y*100 > float(self.matrix_DH.getMultiMatrix().item(1,3)+30) 
        if (max_y*100 < (self.matrix_DH.getMultiMatrix().item(1,3)+30) ):
            print "no pasa"
            self.girar(90)#izquierda
            self.move_distance(0.80,self.speed_move)
            self.girar(90,-0.1)#derecha
            self.move_distance(1,self.speed_move)
        else:
            print "si pasa"
            self.move_distance(1,self.speed_move)


    def mover_distancia(self):
        # import pudb;pudb.set_trace()
        vel_msg = Twist()

        vel_msg.linear.x = self.speed_move
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        detect = self.rear.range
        while detect == self.rear.range:
            a = self.rear.range
        detect = self.rear.range

        t0 = float(rospy.Time.now().to_sec())
        current_distance = 0
        meta = abs(self.odom_x)+self.square_x  # self.rear.range-self.square_x
        tmp_distance = meta
        # self.rear.range > self.square_x:  # (abs(current_distance) < distance):
        while True:
            # print current_distance, ' ', distance, " meta", meta, "(x: " + str(
            #     self.x), " - y:"+str(self.y) + ") range ", self.rear.range
            print "(x: " + str(self.x), " - y:"+str(self.y)
            # self.mapa.getMapa()
            # self.rate.sleep()
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
            t1 = float(rospy.Time.now().to_sec())
            current_distance = self.speed_move*(t1-t0)
            tmp_distance = abs(self.odom_x)  # self.rear.range
            # print abs(tmp_distance) ,' la meta ', meta
            if abs(tmp_distance) > meta:

                self.fin_hilo = True
                self.setProbabilidad(self.x, self.y, "0.000")
                puntos = open(
                    '/home/it-grupo/luis/10semestre/robotica_/final_ros/puntosmapa.txt', 'a+')
                puntos.write(str(self.x) + ',' + str(self.y)+',0,0,0' + '\n')
                self.x += 1
                meta += self.square_x
                # print "mi x ", self.x, " nueva mta ", meta
                self.setProbabilidad(self.x, self.y, self.mapa.komodo)
                puntos.write(str(self.x) + ',' + str(self.y)+',1,1,0' + '\n')
                puntos.close()
                # estaba positivo pero como esta negativo el odom le pongo esto
                tmp_distance -= self.square_x
                # self.scan_cloud(self.cloud)
                # if self.fin_hilo:
                #     print "iniciando hilo"
                #     d = threading.Thread(target=self.scan_cloud, args=(
                #         self.cloud,), name="Daemon")
                #     d.setDaemon(True)
                #     d.start()
                self.fin_hilo = False
            self.fin_hilo = False
            self.scan(self.left.range, "l")
            self.scan(self.rear.range, "b")
            self.scan(self.right.range, "r")
            self.scan_cloud(self.cloud,self.x)

            if self.movement_stop:
                # print self.lista_final
                self.procesaPuntos(self.lista_final)
                break

            if self.x == 0:
                break
        # print "fin bucle"
        vel_msg.linear.x = 0
        self.velocity_publisher.publish(vel_msg)
        self.rate.sleep()
        # self.scan(self.left.range, "r")
        # self.scan(self.right.range, "l")
        # self.scan(self.rear.range, "b")
        # self.mapa.getMapa()

    def interactua(self):
        import os
        os.system('rm /home/it-grupo/luis/10semestre/robotica_/final_ros/puntosmapa.txt')
        # while not rospy.is_shutdown():
            # self.rate.sleep()
            # self.mapa.getMapa()
            # print self.rear.range
        self.mover_distancia()


if __name__ == '__main__':
    try:
        # Testing our function
        x = Lab8()
        x.interactua()

    except rospy.ROSInterruptException:
        pass
