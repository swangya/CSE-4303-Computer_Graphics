import sys
import OpenGL

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import tkinter as tk
from tkinter import filedialog

Angle = 0
Incr = 1
camData = []


def create_pyramid():
    glNewList(1, GL_COMPILE)
    glBegin(GL_TRIANGLES)

    glVertex3f(0, 0, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 1, 0)

    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(0.5, 0.5, 1)

    glColor3f(0, 0, 1)
    glVertex3f(0, 1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(0.5, 0.5, 1)

    glColor3f(1, 1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(0.5, 0.5, 1)

    glColor3f(1, 0, 1)
    glVertex3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0.5, 0.5, 1)

    glEnd()
    glEndList()


def create_3d_axes():
    glNewList(2, GL_COMPILE)
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(2, 0, 0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 2, 0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 2)
    glEnd()
    glEndList()

'''
def display():
    global Angle
    global Incr
    global camData


    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    glEnable(GL_SCISSOR_TEST)
    glScissor(int(0.05 * w), int(0.55 * h), int(0.4 * w), int(0.4 * h))
    glClearColor(0.4, 0.4, 0.6, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 30)
    gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glViewport(int(0.05 * w), int(0.55 * h), int(0.4 * w), int(0.4 * h))
    glCallList(1)
    glPushMatrix()
    glLoadIdentity()
    glCallList(2)
    glPopMatrix()

    glEnable(GL_SCISSOR_TEST)
    glScissor(int(0.05 * w), int(0.05 * h), int(0.4 * w), int(0.4 * h))
    glClearColor(0.4, 0.4, 0.6, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 30)
    gluLookAt(0, 3, 0, 0, 0, 0, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glViewport(int(0.05 * w), int(0.05 * h), int(0.4 * w), int(0.4 * h))
    glCallList(1)
    glPushMatrix()
    glLoadIdentity()
    glCallList(2)
    glPopMatrix()

    glScissor(int(0.55 * w), int(0.55 * h), int(0.4 * w), int(0.4 * h))
    glClearColor(0.4, 0.4, 0.6, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # glFrustum(-1,1,-1,1,1,30)
    gluPerspective(45, .5, 1, 30)
    gluLookAt(3, 0, 0, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glViewport(int(0.55 * w), int(0.55 * h), int(0.4 * w), int(0.4 * h))
    glCallList(1)
    glPushMatrix()
    glLoadIdentity()
    glCallList(2)
    glPopMatrix()

    glScissor(int(0.55 * w), int(0.05 * h), int(0.4 * w), int(0.4 * h))
    glClearColor(0.4, 0.4, 0.6, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, 1, 30)
    # glFrustum(-1,1,-1,1,1,30)
    gluLookAt(2, 2, 2, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glViewport(int(0.55 * w), int(0.05 * h), int(0.4 * w), int(0.4 * h))
    glCallList(1)
    glPushMatrix()
    glLoadIdentity()
    glCallList(2)
    glPopMatrix()

    glFlush()
    glutSwapBuffers()

    glLoadIdentity()
    glRotated(Angle, 0, 1, 0)
    Angle = Angle + Incr
'''


def displayInit():
    global camData

    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    for element in camData:
        a = element[6][2] - element[6][0]
        b = element[6][3] - element[6][1]
        if element[1][1] == 'parallel':
            glEnable(GL_SCISSOR_TEST)
            glScissor(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glClearColor(0.4, 0.4, 0.6, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glFrustum(element[5][0], element[5][1], element[5][2], element[5][3], element[5][4], element[5][5])
            gluLookAt(element[2][0], element[2][1], element[2][2], element[3][0], element[3][1], element[3][2], element[4][0], element[4][1], element[4][2])
            glMatrixMode(GL_MODELVIEW)
            glViewport(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glCallList(1)
            glPushMatrix()
            glLoadIdentity()
            glCallList(2)
            glPopMatrix()

        elif element[1][1] == 'perspective':
            glScissor(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glClearColor(0.4, 0.4, 0.6, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(element[5][0], element[5][1], element[5][2], element[5][3], element[5][4], element[5][5])
            # glFrustum(-1,1,-1,1,1,30)
            gluLookAt(element[2][0], element[2][1], element[2][2], element[3][0], element[3][1], element[3][2], element[4][0], element[4][1], element[4][2])
            glMatrixMode(GL_MODELVIEW)
            glViewport(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glCallList(1)
            glPushMatrix()
            glLoadIdentity()
            glCallList(2)
            glPopMatrix()

    glFlush()
    glutSwapBuffers()



def keyHandler(Key, MouseX, MouseY):
    global Incr
    if Key == b'n' or Key == b'N':
        print("n pressed")
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        print(file_path)

    elif Key == b'f' or Key == b'F':
        print(b"Speeding Up")
        Incr = Incr + 1

    elif Key == b's' or Key == b'S':
        if Incr == 0:
            print("Stopped")
        else:
            print("Slowing Down")
            Incr = Incr - 1

    elif Key == b'q' or Key == b'Q':
        print("Bye")
        sys.exit()

    else:
        print(("Invalid Key ", Key))


def timer(dummy):
    #display()
    glutTimerFunc(30, timer, 0)


def reshape(w, h):
    print(("Width=", w, "Height=", h))

#===================================================================================
#=============================MAIN==================================================
#===================================================================================


with open("cameras_06.txt") as textFile:
    lines = [line.split() for line in textFile]

flg = 0 #to check if it is the first camera
temp = []
for element in lines:
    if element[0] == 'c':
        if flg !=0:
            camData.append(temp)
            temp = []
    else:
        if element[0] == 'i':
            temp.append(element)
        elif element[0] == 't':
            temp.append(element)
        elif element[0] == 'e':
            temp.append([float(element[1]), float(element[2]), float(element[3])])
        elif element[0] == 'l':
            temp.append([float(element[1]), float(element[2]), float(element[3])])
        elif element[0] == 'u':
            temp.append([float(element[1]), float(element[2]), float(element[3])])
        elif element[0] == 'w':
            temp.append([float(element[1]), float(element[2]), float(element[3]), float(element[4]), float(element[5]), float(element[6])])
        elif element[0] == 's':
            temp.append([float(element[1]), float(element[2]), float(element[3]), float(element[4])])

        flg = 1;
camData.append(temp)
print(camData)


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"PyOpenGL Demo")
glClearColor(1, 1, 0, 0)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS);

glutDisplayFunc(displayInit)
glutKeyboardFunc(keyHandler)
glutTimerFunc(300, timer, 0)
glutReshapeFunc(reshape)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glMatrixMode(GL_MODELVIEW)
create_pyramid()
create_3d_axes()
glutMainLoop()
