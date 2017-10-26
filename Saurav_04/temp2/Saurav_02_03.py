# Saurav, Swangya
# 1001-054-908
# 2017-09-29
# Assignment_02_03

import numpy as np

class cl_world:
    def __init__(self, objects=[], canvases=[]):
        self.objects = objects
        self.canvases = canvases
        self.data = []
        self.vertex_list = []
        self.edge_list = []
        self.window_dimension = []
        self.view_dimension = []
        self.translated_points = []
        self.draw_list = []
        self.width = 0
        self.height = 0
        self.viewFrameDimensions = []
        # self.display

    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.world = self

    def create_graphic_objects(self, canvas, data):
        self.data = data
        self.width = canvas.cget("width")
        self.height = canvas.cget("height")
        self.create_edge_list()
        self.create_vertex_list()
        self.get_viewport()
        self.get_window()
        self.draw(canvas)

    def translation(self, tPoints, canvas):
        Dx = float(tPoints[0])
        Dy = float(tPoints[1])
        Dz = float(tPoints[2])

        self.drawTranslation(Dx, Dy, Dz)
        canvas.delete("all")
        self.draw(canvas)


    def drawTranslation(self, x, y, z):
        points = np.array(self.vertex_list, dtype=float)
        tPoints = np.array([x, y, z], dtype=float)
        translatedPoints = points + tPoints
        self.vertex_list = translatedPoints.tolist()


    def scaling(self, point, factor, canvas):
        factor = float(factor)
        x = float(point[0])
        y = float(point[1])
        z = float(point[2])

        self.drawTranslation(-x, -y, -z)
        self.drawScaling(factor, canvas)
        self.drawTranslation(x, y, z)
        canvas.delete("all")
        self.draw(canvas)


    def drawScaling(self, factor, canvas):
        Scalepoints = np.array(self.vertex_list, dtype=float)
        sFactor = np.array([factor, factor, factor])
        translatedPoints = Scalepoints * sFactor
        self.vertex_list = translatedPoints.tolist()
        #self.draw(canvas)

    def Rotate(self, A, B, line, angle, canvas):
        tempList = []
        rotatedPoints = []

        Mat = self.rotationMat(A, B, angle)

        for element in self.vertex_list:
            element = [float(i) for i in element]
            element.append(1.0)
            tempList.append(element)

        for element in tempList:
            element = np.array(element)
            element = element.dot(Mat)
            temp = element
            temp = temp.tolist()
            del temp[-1]
            rotatedPoints.append(temp)

        self.vertex_list = rotatedPoints
        canvas.delete("all")
        self.draw(canvas)


    def rotationMat(self,N, M, angle):
        A = float(M[0]) - float(N[0])
        B = float(M[1]) - float(N[1])
        C = float(M[2]) - float(N[2])

        L = np.sqrt(A**2 + B**2 + C**2)

        V = np.sqrt(B**2 + C**2)
        if V == 0:
            V = 1

        D = np.array([[1.0, 0.0, 0.0, -N[0]], [0.0, 1.0, 0.0, -N[1]], [0.0, 0.0, 1.0, -N[2]], [0.0, 0.0, 0.0, 1.0]])

        Rx = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, (C/V), (-B/V), 0.0], [0.0, (B/V), (C/V), 0.0], [0.0, 0.0, 0.0, 1.0]])

        Ry = np.array([[(V/L), 0.0, (-A/L), 0.0], [0.0, 1.0, 0.0, 0.0], [(A/L), 0.0, (V/L), 0.0], [0.0, 0.0, 0.0, 1.0]])

        angle = angle * np.pi/180
        s = np.sin(angle)
        c = np.cos(angle)

        Rz = np.array([[c, -s, 0.0, 0.0], [s, c, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])

        revRy = np.array([[(V/L), 0.0, (A/L), 0.0], [0.0, 1.0, 0.0, 0.0], [(-A/L), 0.0, (V/L), 0.0], [0.0, 0.0, 0.0, 1.0]])

        revRx = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, (C/V), (B/V), 0.0], [0.0, (-B/V), (C/V), 0.0], [0.0, 0.0, 0.0, 1.0]])

        revD = np.array([[1.0, 0.0, 0.0, N[0]], [0.0, 1.0, 0.0, N[1]], [0.0, 0.0, 1.0, N[2]], [0.0, 0.0, 0.0, 1.0]])

        Mat = revD.dot(revRx)
        Mat = Mat.dot(revRy)
        Mat = Mat.dot(Rz)
        Mat = Mat.dot(Ry)
        Mat = Mat.dot(Rx)
        Mat = Mat.dot(D)

        if B == 0 and C == 0:
            Mat = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, c, -s, 0.0], [0.0, s, c, 0.0], [0.0, 0.0, 0.0, 1.0]])

        elif A == 0 and C == 0:
            Mat = np.array([[c, 0.0, s, 0.0], [0.0, 1.0, 0.0, 0.0], [-s, 0.0, c, 0.0], [0.0, 0.0, 0.0, 1.0]])

        elif A == 0 and B == 0:
            Mat = np.array([[c, -s, 0.0, 0.0], [s, c, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])

        return Mat

    def draw(self, canvas):
        self.translate_points()
        self.create_draw_list()
        a = self.view_dimension
        dimension = self.translateViewport(a[0], a[1], a[2], a[3])

        self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black', fill='yellow'))
        for elements in self.draw_list:
            self.objects.append(canvas.create_line(elements))

    def create_vertex_list(self):
        self.vertex_list = []
        for element in self.data:
            if element[0] == 'v':
                self.vertex_list.append([element[1], element[2], element[3]])

    def create_edge_list(self):
        self.edge_list = []
        for element in self.data:
            if element[0] == 'f':
                self.edge_list.append(element)

    def get_viewport(self):
        for element in self.data:
            if element[0] == 's':
                dimension = element
                break
        self.view_dimension = [dimension[1], dimension[2], dimension[3], dimension[4]]

    def get_window(self):
        for element in self.data:
            if element[0] == 'w':
                dimension = element
                break
        self.window_dimension = [dimension[1], dimension[2], dimension[3], dimension[4]]

    def translateViewport(self, xmin, ymin, xmax, ymax):
        a = self.width
        b = self.height
        x = float(xmin)*float(a)
        y = float(ymin)*float(b)
        width = (float(xmax) - float(xmin))*float(a)
        height = (float(ymax) - float(ymin))*float(b)
        u = x+width
        v = y+height
        dimensions = [x, y, u, v]
        self.viewFrameDimensions = dimensions
        return dimensions

    def translate_points(self):
        self.translated_points = []
        for element in self.vertex_list:
            temp = self.translate_coordinate(element[0], element[1])
            self.translated_points.append(temp)

    def translate_coordinate(self, pwx, pwy):
        a = self.window_dimension
        b = self.view_dimension

        pwx = float(pwx)
        pwy = float(pwy)

        xwmin = float(a[0])
        xwmax = float(a[2])
        ywmin = float(a[1])
        ywmax = float(a[3])
        nxvmin = float(b[0])
        nxvmax = float(b[2])
        nyvmin = float(b[1])
        nyvmax = float(b[3])
        screen_width = float(self.width)
        screen_height = float(self.height)

        xvmin = float(nxvmin * screen_width)
        xvmax = float(nxvmax * screen_width)
        yvmin = float(nyvmin * screen_height)
        yvmax = float(nyvmax * screen_height)

        sx = (xvmax - xvmin) / (xwmax - xwmin)
        psx = xvmin + float(sx * (pwx - xwmin))
        sy = (yvmax - yvmin) / (ywmax - ywmin)
        psy = yvmin + float(sy * (ywmax - pwy))

        return [psx, psy]

    def create_draw_list(self):
        self.draw_list = []
        l = self.translated_points
        for elements in self.edge_list:
            if elements[0] == 'f':
                elements.pop(0)

            for i in range(0, 3):
                temp = []
                x = int(elements[i]) - 1
                if i == 2:
                    y = int(elements[0]) - 1
                else:
                    y = int(elements[i + 1]) - 1
                point1 = l[x]
                point2 = l[y]
                temp = [point1[0], point1[1], point2[0], point2[1]]
                self.draw_list.append(temp)

    def redisplay(self, canvas, event):
        if self.objects:
            self.width = float(event.width)
            self.height = float(event.height)

            canvas.delete("all")

            self.get_viewport()
            self.get_window()
            self.translate_points()
            self.create_draw_list()

            a = self.view_dimension
            dimension = self.translateViewport(a[0], a[1], a[2], a[3])
            self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black', fill='yellow'))
            for elements in self.draw_list:
                self.objects.append(canvas.create_polygon(elements, outline='black', fill='red'))