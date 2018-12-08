import OpenGL 
OpenGL.ERROR_ON_COPY = True 

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from random import uniform



def init2D(r,g,b):
    glClearColor(r,g,b,0.0)    
    glMatrixMode (GL_PROJECTION)
    gluOrtho2D (0.0, 1024.0, 0.0, 2048.0)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    while True:
        i=j=0

        glPointSize(8)
        glColor3f(1.0, 0.0, 0.0)

        #draw two points
        glBegin(GL_POINTS)
        # puntos()
        #draw two points
        # glBegin(GL_POINTS)
        try:
            file = open('puntosmapa.txt','rb')
            # for i in range(0,10):
            #     glColor3f(1.0,uniform(0.1,1),uniform(0.1,1))
            #     glVertex2i(10+16*i,50*i+10)
            lines =file.readlines()
        except IOError:
            lines=[]
        for line  in (lines):
            # line =lines[1-n]
            point = line.split(',')
            # print int(point[0]), ' ',int(point[1])
            # glColor3f(uniform(0.1,1),uniform(0.2,1),uniform(0.3,0.9))
            glColor3f(float(point[2]),float(point[3]),float(point[4]) )
            glVertex2i(350+13*(int(point[1])),26*(int(point[0])))   

            
        glEnd()
        glFlush()
    
glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (700, 1000)
glutInitWindowPosition (10, 10)
glutCreateWindow ('points and lines')
init2D(0.0,0.0,0.0)
glutDisplayFunc(display)
glutMainLoop()


