from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL import GLX
import random
import os
import time
from random import uniform
import math
nuble_1d = []
# width=1280
# height=800
width=640
height=480
def puntos():
    print "leyendo"
    # os.system("cp nube1metro.txt nube1metrotmp.txt") 
    file = open('nube1metro.txt','rb')
    lineas = file.readlines()

    global nuble_1d
    # if tam> 30000000:
    # del nuble_1d[:]
    print(u"len  " ,len(lineas))
    if len(lineas)>=width*height-width:#1020000:

        for linea in lineas:#while linea[0:3] != '---':
            # print "my linea ",linea
            
                #linea = str(linea)
            if linea[0:3] == '---':
                break
            linea = linea.split(',')
            if len(linea)>2:
                nuble_1d.append(linea[2])
            else:
                nuble_1d.append(0)

            # linea = file.readline()
    else:
        del nuble_1d[:]

        

    file.close()
    # os.system("rm nube1metrotmp.txt") 




def init2D(r,g,b):
    glClearColor(r,g,b,0.0)    
    glMatrixMode (GL_PROJECTION)
    # gluOrtho2D (0.0, 640.0, 0.0, 460.0)
    gluOrtho2D (0.0,width, 0.0, height)
def is_number_tryexcept(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def display():
    # global nuble_1d
    glClear(GL_COLOR_BUFFER_BIT)
    while True:
        i=j=0

        glPointSize(10)
        glColor3f(1.0, 0.0, 0.0)

        #draw two points
        glBegin(GL_POINTS)
        # puntos()
        file = open('nube1metro.txt','rb')
        nuble_1d = file.readlines()

        # global nuble_1d
        # if tam> 30000000:
        # del nuble_1d[:]
        # print(u"len  " ,len(nuble_1d)," ",width*height-width*2)
        if len(nuble_1d)>=0:#width*height:#1022440:
            print "pintando"
            # if len(nuble_1d)!=1024000:
            #     del nuble_1d[:]
            # print "si pintando"
            for n in range(len(nuble_1d)-1):#range (0,width*height-1):
                if i == width-1:
                    i = 0
                    j += 1
                else:
                    i += 1
                # if is_number_tryexcept(nuble_1d[1-n]):
                linea =nuble_1d[1-n]
                linea = linea.split(',')
                # print linea
                if len(linea)>2:
                    gris = float(linea[2]) if is_number_tryexcept(linea[2]) else uniform(0.2,1)
                else:
                    gris=1.0
                # gris = float(nuble_1d[1-n]) if is_number_tryexcept(nuble_1d[1-n]) else 0.0

                gris = gris/3.5
                # print "valor ",float(gris)
                x =  i
                y =  j
                #print(i , " ", j)
                # glColor3f(1-gris, 1-gris,1- gris)
                glColor3f(gris*1.0, gris*1.0, gris*1.0)
                glVertex2i(width-x,y)
        # del nuble_1d[:]
            print "termine pintar"
        glEnd()
        glFlush()
        # GLX.SwapBuffer() 
    
# puntos()
glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (1000, 1000)
glutInitWindowPosition (100, 100)
glutCreateWindow ('points and lines')
init2D(1.0,1.0,1.0)
glutDisplayFunc(display)
glutMainLoop()