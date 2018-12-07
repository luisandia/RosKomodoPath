import numpy as np
from math import *
import sys
np.set_printoptions(suppress=True)


class MatrizDH:

    def __init__(self, a=0, alpha=0, d=0, theta=0):

        self.setMatrix(a, alpha, d, theta)

    def getMatrix(self):
        return self.matrix

    def setMatrix(self, a, d, alpha, theta):
        self.matrix = np.matrix(
            [
                [cos(theta), -cos(alpha)*sin(theta),sin(alpha)*sin(theta), a*cos(theta)],
                [sin(theta), cos(alpha)*cos(theta), -sin(alpha)*cos(theta), a*sin(theta)],
                [0, sin(alpha), cos(alpha), d],
                [0, 0, 0, 1],
            ]
        )


class ArticulacionKomodo:
    def __init__(self):
        self.articulacion_1 = MatrizDH()
        self.articulacion_2 = MatrizDH()
        self.articulacion_3 = MatrizDH()
        self.articulacion_4 = MatrizDH()
        self.articulacion_5 = MatrizDH()
        self.camara = MatrizDH()

    def setArticulacion_1(self, a, d, alpha, theta):
        self.articulacion_1.setMatrix( a, d, alpha, theta)

    def setArticulacion_2(self, a, d, alpha, theta):
        self.articulacion_2.setMatrix( a, d, alpha, theta)

    def setArticulacion_3(self, a, d, alpha, theta):
        self.articulacion_3.setMatrix( a, d, alpha, theta)

    def setArticulacion_4(self, a, d, alpha, theta):
        self.articulacion_4.setMatrix( a, d, alpha, theta)

    def setArticulacion_5(self, a, d, alpha, theta):
        self.articulacion_5.setMatrix( a, d, alpha, theta)

    def setCamara(self, a, d, alpha, theta):
        self.camara.setMatrix( a, d, alpha, theta)

    def getMatrix(self):
        print "Articulacion 1"
        print self.articulacion_1.getMatrix()
        print "Articulacion 2"
        print self.articulacion_2.getMatrix()
        print "Articulacion 3"
        print self.articulacion_3.getMatrix()
        print "Articulacion 4"
        print self.articulacion_4.getMatrix()
        print "Articulacion 5"
        print self.articulacion_5.getMatrix()
        print "Camara"
        print self.camara.getMatrix()

    def getMultiMatrix(self):
        return self.articulacion_1.getMatrix()*self.articulacion_2.getMatrix()*self.articulacion_3.getMatrix() * \
        self.articulacion_4.getMatrix()*self.articulacion_5.getMatrix()*self.camara.getMatrix()

if __name__ == '__main__':


    '''
    theta_i = es el angulo formado por los ejes x_i-1 y x_i medio en un plano perpendicular
    a z_i-1 utilizando la regla de la mano derecha este es un parametro variable en articulaciones rotatorias

    d_i = es la distancia a lo largo del eje z_i-1 desde el origen o_i-1 hasta la interseccion del eje x_i con el
    eje z_i-1. Este es un parametro variable en articulaciones prismaticas

    a_i = para articulaciones 
    rotatorias: es la distancia a lo largo del eje x_i desde el origen o_i hasta la interseccion del eje z_i con el eje z_i-1
    prismaticas: es la distancia mas corta entre los ejes

    alpha_i = es el angulo formado por los ejes z_i y z_i-1 medido en un plano perpendicular al eje x_i utilizando la regla
    de la mano derecha
    '''


    # theta1 = 0
    # theta2 = 0
    # theta3 = 0
    # theta4 = 0
    # theta5 = 0

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

    x = ArticulacionKomodo()# a d alpha theta
    x.setArticulacion_1(0.0, 13.8, 0.0, theta1)
    x.setArticulacion_2(0.0, 0.0, -pi/2, -pi/2+theta2)
    x.setArticulacion_3(27.0,  0.0,-pi/2, -theta3)
    x.setArticulacion_4(22.3,  0.0,-pi/2, -pi/2-theta4)
    x.setArticulacion_5(1.0, 24.0, -pi/2, theta5)
    x.setCamara(-6.5, 4.5, 0.0, 0.0)
    x.getMatrix()

    print pi
    print ""
    print "multiplicacion 1"
    print x.articulacion_1.getMatrix()
    print "multiplicacion 2"
    print x.articulacion_1.getMatrix()*x.articulacion_2.getMatrix()
    print "multiplicacion 3"
    print x.articulacion_1.getMatrix()*x.articulacion_2.getMatrix()*x.articulacion_3.getMatrix()
    print "multiplicacion 4"
    print x.articulacion_1.getMatrix()*x.articulacion_2.getMatrix()*x.articulacion_3.getMatrix() * \
        x.articulacion_4.getMatrix()
    print "multiplicacion 5"
    print x.articulacion_1.getMatrix()*x.articulacion_2.getMatrix()*x.articulacion_3.getMatrix() * \
        x.articulacion_4.getMatrix()*x.articulacion_5.getMatrix()
    print "multiplicacion camara"
    print x.articulacion_1.getMatrix()*x.articulacion_2.getMatrix()*x.articulacion_3.getMatrix() * \
        x.articulacion_4.getMatrix()*x.articulacion_5.getMatrix()*x.camara.getMatrix()

    print x.getMultiMatrix().item(1,3)
