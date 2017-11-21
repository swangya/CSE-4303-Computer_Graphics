# Saurav, Swangya
# 1001-054-908
# 2017-11-20
# Assignment_06_01

import sys
import OpenGL
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

data = []
Angle = 0
Incr = 1
camData = []
dispFile = "pyramid_06.txt"

vertex = []
face = []
bPoints = []
bFaces = []
res = 4

xAngle = 0
yAngle = 0
zAngle = 0

eyeX = 0
eyeY = 0
eyeZ = 0

cenX = 0
cenY = 0
cenZ = 0

switchFlg = 0

def create_graphic():
    global face
    global vertex
    global xAngle
    global yAngle
    global zAngle

    glNewList(1, GL_COMPILE)
    glBegin(GL_TRIANGLES)
    for element in face:
        a = int(element[0]-1)
        b = int(element[1]-1)
        c = int(element[2]-1)

        glColor3f(1, 1, 0)
        glVertex3f(vertex[a][0], vertex[a][1], vertex[a][2])
        glVertex3f(vertex[b][0], vertex[b][1], vertex[b][2])
        glVertex3f(vertex[c][0], vertex[c][1], vertex[c][2])
    glEnd()
    glEndList()
    glRotated(xAngle, 1, 0, 0)
    glRotated(yAngle, 0, 1, 0)
    glRotated(zAngle, 0, 0, 1)


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


def displayInit():
    global camData
    global eyeX
    global eyeY
    global eyeZ
    global cenX
    global cenY
    global cenZ
    global switchFlg



    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    for element in camData:
        a = element[6][2] - element[6][0]
        b = element[6][3] - element[6][1]
        if element[1][1] == 'parallel' and switchFlg == 0:
            glEnable(GL_SCISSOR_TEST)
            glScissor(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glClearColor(0.4, 0.4, 0.6, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(element[5][0], element[5][1], element[5][2], element[5][3], element[5][4], element[5][5])

            ex = element[3][0] - element[2][0]
            ey = element[3][1] - element[2][1]
            ez = element[3][2] - element[2][2]

            gluLookAt((element[2][0]+(eyeX*ex)), (element[2][1]+(eyeY*ey)), (element[2][2]+(eyeZ*ez)), (element[3][0]+cenX), (element[3][1]+cenY), (element[3][2]+cenZ), element[4][0], element[4][1], element[4][2])
            glMatrixMode(GL_MODELVIEW)
            glViewport(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glCallList(1)
            glPushMatrix()
            glLoadIdentity()
            glCallList(2)
            glPopMatrix()

        elif element[1][1] == 'perspective' and switchFlg == 0:
            glScissor(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glClearColor(0.4, 0.4, 0.6, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glFrustum(element[5][0], element[5][1], element[5][2], element[5][3], element[5][4], element[5][5])

            ex = element[3][0] - element[2][0]
            ey = element[3][1] - element[2][1]
            ez = element[3][2] - element[2][2]

            gluLookAt((element[2][0]+(eyeX*ex)), (element[2][1]+(eyeY*ey)), (element[2][2]+(eyeZ*ez)), (element[3][0]+cenX), (element[3][1]+cenY), (element[3][2]+cenZ), element[4][0], element[4][1], element[4][2])
            glMatrixMode(GL_MODELVIEW)
            glViewport(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glCallList(1)
            glPushMatrix()
            glLoadIdentity()
            glCallList(2)
            glPopMatrix()

        elif element[1][1] == 'parallel' and switchFlg == 1:
            glScissor(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glClearColor(0.4, 0.4, 0.6, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glFrustum(element[5][0], element[5][1], element[5][2], element[5][3], element[5][4], element[5][5])

            ex = element[3][0] - element[2][0]
            ey = element[3][1] - element[2][1]
            ez = element[3][2] - element[2][2]

            gluLookAt((element[2][0] + (eyeX * ex)), (element[2][1] + (eyeY * ey)), (element[2][2] + (eyeZ * ez)), (element[3][0] + cenX), (element[3][1] + cenY), (element[3][2] + cenZ), element[4][0], element[4][1], element[4][2])
            glMatrixMode(GL_MODELVIEW)
            glViewport(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glCallList(1)
            glPushMatrix()
            glLoadIdentity()
            glCallList(2)
            glPopMatrix()

        elif element[1][1] == 'perspective' and switchFlg == 1:
            glEnable(GL_SCISSOR_TEST)
            glScissor(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glClearColor(0.4, 0.4, 0.6, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(element[5][0], element[5][1], element[5][2], element[5][3], element[5][4], element[5][5])

            ex = element[3][0] - element[2][0]
            ey = element[3][1] - element[2][1]
            ez = element[3][2] - element[2][2]

            gluLookAt((element[2][0] + (eyeX * ex)), (element[2][1] + (eyeY * ey)), (element[2][2] + (eyeZ * ez)), (element[3][0] + cenX), (element[3][1] + cenY), (element[3][2] + cenZ), element[4][0], element[4][1], element[4][2])
            glMatrixMode(GL_MODELVIEW)
            glViewport(int(element[6][0] * w), int(element[6][1] * h), int(a * w), int(b * h))
            glCallList(1)
            glPushMatrix()
            glLoadIdentity()
            glCallList(2)
            glPopMatrix()

    glFlush()
    glutSwapBuffers()


def handleArrowPress(key, MouseX, MouseY):
    global cenX
    global cenY
    global cenZ

    if key == GLUT_KEY_LEFT:
        cenX = cenX + 0.05
        #cenY = cenY + 0.05
        #cenZ = cenZ + 0.05
        glutDisplayFunc(displayInit)
        glutPostRedisplay()

    if key == GLUT_KEY_RIGHT:
        cenX = cenX - 0.05
        #cenY = cenY - 0.05
        #cenZ = cenZ - 0.05
        glutDisplayFunc(displayInit)
        glutPostRedisplay()

    if key == GLUT_KEY_UP:
        #cenX = cenX + 0.05
        cenY = cenY + 0.05
        #cenZ = cenZ + 0.05
        glutDisplayFunc(displayInit)
        glutPostRedisplay()

    if key == GLUT_KEY_DOWN:
        #cenX = cenX - 0.05
        cenY = cenY - 0.05
        #cenZ = cenZ - 0.05
        glutDisplayFunc(displayInit)
        glutPostRedisplay()


def keyHandler(Key, MouseX, MouseY):
    global Incr
    global data
    global xAngle
    global yAngle
    global zAngle
    global eyeZ
    global eyeX
    global eyeY
    global switchFlg
    global res

    if Key == b'n' or Key == b'N':
        root = tk.Tk()
        root.withdraw()

        var_filename = tk.StringVar()
        var_filename.set('')
        var_filename.set(tk.filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")]))

        file_path = var_filename.get()
        #file_path = simpledialog.askstring('Load File', 'Enter File name')

        if file_path == '' or file_path == None:
            file_path = "pyramid_06.txt"

        if file_path != None:
            with open(file_path) as textFile:
                lines = [line.split() for line in textFile]
            data = [x for x in lines if x != []]
            createVertex(data, 4, 0)
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    if Key == b'r':
        res = res - 1
        if res < 2:
            res = 2
        createVertex(data, res, 1)
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    if Key == b'R':
        res = res + 1
        if res > 100:
            res = 100
        createVertex(data, res, 1)
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    elif Key == b'x':
        print(b"Rotating X by 5 degrees")
        xAngle = 5
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    elif Key == b'X':
        print(b"Rotating X by 5 degrees")
        xAngle = -5
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    elif Key == b'y':
        print(b"Rotating Y by 5 degrees")
        yAngle = 5
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    elif Key == b'Y':
        print(b"Rotating Y by -z5 degrees")
        yAngle = -5
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    elif Key == b'z':
        print(b"Rotating Z by 5 degrees")
        zAngle = 5
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    elif Key == b'Z':
        print(b"Rotating Z by 5 degrees")
        zAngle = -5
        glMatrixMode(GL_MODELVIEW)
        create_graphic()
        glutPostRedisplay()

    elif Key == b's':
        glMatrixMode(GL_MODELVIEW)
        glScalef(1.05, 1.05, 1.05)
        glutPostRedisplay()

    elif Key == b'S':
        glMatrixMode(GL_MODELVIEW)
        glScalef((1/1.05), (1/1.05), (1/1.05))
        glutPostRedisplay()

    elif Key == b'f':
        eyeX = eyeX + (0.05 / 1.05)
        eyeY = eyeY + (0.05 / 1.05)
        eyeZ = eyeZ + (0.05/1.05)
        glutDisplayFunc(displayInit)
        glutPostRedisplay()

    elif Key == b'b':
        eyeX = eyeX - (0.05 / 1.05)
        eyeY = eyeY - (0.05 / 1.05)
        eyeZ = eyeZ - (0.05 / 1.05)
        glutDisplayFunc(displayInit)
        glutPostRedisplay()

    elif Key == b'p':
        if switchFlg == 0:
            switchFlg = 1
        elif switchFlg ==1:
            switchFlg = 0
        glutPostRedisplay()

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
#=======================Getting Points From Bezier Data=============================


def createVertex(data, res, flg):
    global vertex
    global face
    global bPoints
    global bFaces

    bezierList = []
    resolution = 4

    for element in data:
        if element[0] == 'n':
              resolution = int(element[1])
        elif element[0] == 'b':
            bezierList.append([float(element[1]), float(element[2]), float(element[3])])
        elif element[0] == 'v':
            vertex.append([float(element[1]), float(element[2]), float(element[3])])
        elif element[0] == 'f':
            face.append([float(element[1]), float(element[2]), float(element[3])])

    if flg == 1:
        resolution = res

    get_bezier_points(bezierList, resolution)




def get_bezier_points(bezier_list, lim):
    total = len(bezier_list)
    bezier_P_list = []
    temp = []
    for i in range(0, total, 4):
        temp = []
        for j in range(i, (i+4)):
            temp.append(bezier_list[j])
        bezier_P_list.append(temp)

    P_length = len(bezier_P_list)

    for i in range(0, P_length, 4):
        end = i + 4
        create_bezier_surface(bezier_P_list[i:end], lim)



def create_bezier_surface(bezier_P_list, lim):
    global bPoints
    global vertex
    global face
    lim = lim + 1
    # Bernstein basis functions
    uinc = 1.0 / float(lim - 1)
    u = 0
    B = []
    B0 = []
    B1 = []
    B2 = []
    B3 = []

    for i in range(0, lim):
        u_sqr = np.square(u)
        tmp = 1.0 - u
        tmp_sqr = np.square(tmp)
        B0.append(tmp * tmp_sqr)
        B1.append(3 * u * tmp_sqr)
        B2.append(3 * u_sqr * tmp)
        B3.append(u * u_sqr)
        u = u + uinc
    B.append(B0)
    B.append(B1)
    B.append(B2)
    B.append(B3)
    point = []

    for i in range(0, lim):
        a1 = Curve(i, [bezier_P_list[0][0], bezier_P_list[1][0], bezier_P_list[2][0], bezier_P_list[3][0]], B)
        a2 = Curve(i, [bezier_P_list[0][1], bezier_P_list[1][1], bezier_P_list[2][1], bezier_P_list[3][1]], B)
        a3 = Curve(i, [bezier_P_list[0][2], bezier_P_list[1][2], bezier_P_list[2][2], bezier_P_list[3][2]], B)
        a4 = Curve(i, [bezier_P_list[0][3], bezier_P_list[1][3], bezier_P_list[2][3], bezier_P_list[3][3]], B)
        for j in range(0, lim):
            temp = []
            temp = Curve(j, [a1, a2, a3, a4], B)
            point.append(temp)

    n = len(vertex)
    bPoints = point

    for i in range((lim*lim)-1):
        n1 = i+1
        if n1%lim != 0 and n1+lim < (lim*lim):
            temp = [(i+n+1), (n1 + n+1), (n1+lim+n+1)]
            bFaces.append(temp)

    vertex = vertex + bPoints
    face = face + bFaces

def Curve(t, c, B):
    c = np.array(c)
    a = []
    curve = np.multiply(c[0], B[0][t]) + np.multiply(c[1], B[1][t]) + np.multiply(c[2], B[2][t]) + np.multiply(c[3], B[3][t])
    temp = np.add(np.multiply(c[0], B[0][t]), np.add(np.multiply(c[1], B[1][t]), np.add(np.multiply(c[2], B[2][t]), np.multiply(c[3], B[3][t]))))
    return curve.tolist()

#===================================================================================
#=============================MAIN==================================================
#===================================================================================


# Opening camera data and reading it into list
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

        flg = 1
camData.append(temp)
#===================================================================================


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Saurav_06")
glClearColor(1, 1, 0, 0)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS);

glutDisplayFunc(displayInit)
glutSpecialFunc(handleArrowPress);
glutKeyboardFunc(keyHandler)
glutTimerFunc(300, timer, 0)
glutReshapeFunc(reshape)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glMatrixMode(GL_MODELVIEW)
create_3d_axes()
glutMainLoop()
