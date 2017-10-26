# Saurav, Swangya
# 1001-054-908
# 2017-10-12
# Assignment_03_03

import numpy as np

class cl_world:
    def __init__(self, objects=[], canvases=[]):
        self.objects = objects
        self.canvases = canvases
        self.data = []
        self.vertex_list = []
        self.edge_list = []
        self.window_dimension = [-1, -1, 1, 1]
        self.view_dimension = []
        self.translated_points = []
        self.draw_list = []
        self.width = 0
        self.height = 0
        self.viewFrameDimensions = []

        self.cameraName = ''
        self.cameraType = "parallel"
        self.VRP = [0, 0, 0]
        self.VPN = [0, 0, 1]
        self.VUP = [0, 1, 0]
        self.PRP = [0, 0, 1]
        self.VRC = [-1, 1, -1, 1, -1, 1]
        self.viewPort = [0.1, 0.1, 0.4, 0.4]
        self.projMat = np.identity(4)

        # self.display

    def set_camera(self, canvas, fly):
        filename = "cameras.txt"
        with open(filename) as textFile:
            lines = [line.split() for line in textFile]
        list = [x for x in lines if x != []]
        lines = list

        flg = 0

        for element in lines:
            if element[0] == 'c':
                flg = flg + 1;

            if flg == 1:
                if element[0] == 'i':
                    self.cameraName = element[1]
                elif element[0] == 't':
                    self.cameraType = element[1]
                elif element[0] == 'r':
                    self.VRP = self.get_listData(element)
                elif element[0] == 'n':
                    self.VPN = self.get_listData(element)
                elif element[0] == 'u':
                    self.VUP = self.get_listData(element)
                elif element[0] == 'p':
                    self.PRP = self.get_listData(element)
                elif element[0] == 'w':
                    self.VRC = self.get_listData(element)
                elif element[0] == 's':
                    self.view_dimension = self.get_listData(element)

        if fly != "X":
            Points = str.split(fly)
            points = [float(Points[0]), float(Points[1]), float(Points[2])]
            self.VRP = points

        self.width = canvas.cget("width")
        self.height = canvas.cget("height")

        a = self.view_dimension
        dimension = self.translateViewport(a[0], a[1], a[2], a[3])

        self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black'))

        self.projMat = self.get_pllProjMat()


    def get_listData(self, list):
        retList = []
        length = int(len(list))

        for i in range(1, length):
            retList.append(float(list[i]))

        return retList

    def get_pllProjMat(self):
        VRP = self.VRP
        VRP.append(1)
        VPN = self.VPN
        VPN.append(1)
        VUP = self.VUP
        VUP.append(1)
        PRP = self.PRP
        PRP.append(1)
        UVN = self.VRC

        VRP = np.array(VRP)
        VPN = np.array(VPN)
        VUP = np.array(VUP)
        PRP = np.array(PRP)


        tranVRP_ORJ = np.array([[1.0, 0.0, 0.0, -self.VRP[0]], [0.0, 1.0, 0.0, -self.VRP[1]], [0.0, 0.0, 1.0, -self.VRP[2]], [0.0, 0.0, 0.0, 1.0]])
        VRP = np.dot(tranVRP_ORJ, VRP)

        hyp = np.sqrt(self.VPN[1] ** 2 + self.VPN[2] ** 2)
        a = float(self.VPN[2] / hyp)
        b = float(self.VPN[1] / hyp)
        Rx = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, a, -b, 0.0], [0.0, -b, a, 0.0], [0.0, 0.0, 0.0, 1.0]])
        VPN = np.dot(Rx, VPN)
        VUP = np.dot(Rx, VUP)

        hyp = np.sqrt(VPN[0] ** 2 + VPN[2] ** 2)
        a = float(VPN[2] / hyp)
        b = float(VPN[0] / hyp)
        Ry = np.array([[a, 0.0, b, 0.0], [0.0, 1.0, 0.0, 0.0], [-b, 0.0, a, 0.0], [0.0, 0.0, 0.0, 1.0]])
        VPN = np.dot(Ry, VPN)
        VUP = np.dot(Ry, VUP)

        hyp = np.sqrt(VUP[0] ** 2 + VUP[1] ** 2)
        a = float(VUP[1] / hyp)
        b = float(VUP[0] / hyp)

        Rz = np.array([[a, -b, 0.0, 0.0], [b, a, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
        VPN = np.dot(Rz, VPN)
        VUP = np.dot(Rz, VUP)

        #Sheer
        a = (-(PRP[0]-((UVN[1]+UVN[0])/2)))/PRP[2]
        b = (-(PRP[1]-((UVN[3]+UVN[2])/2)))/PRP[2]

        shear = np.array([[1, 0, a, 0], [0, 1, b, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        VRP = np.dot(shear, VRP)
        PRP = np.dot(shear, PRP)

        a = -(UVN[0]+UVN[1])/2
        b = -(UVN[2]+UVN[3])/2
        if UVN[5]>UVN[4]:
            c = -UVN[4]
        else:
            c = -UVN[5]

        tran2 = np.array([[1, 0, 0, a], [0, 1, 0, b], [0, 0, 1, c], [0, 0, 0, 1]])
        VRP = np.dot(tran2, VRP)
        PRP = np.dot(tran2, PRP)

        #Scale
        if UVN[1]>UVN[0]:
            a = 2/(UVN[1]-UVN[0])
        else:
            a = 2/(UVN[0]-UVN[1])

        if UVN[3]>UVN[2]:
            b = 2/(UVN[3]-UVN[2])
        else:
            b = 2/(UVN[2]-UVN[3])

        if UVN[5]>UVN[4]:
            c = 1/(UVN[5]-UVN[4])
        else:
            c = 1/(UVN[4]-UVN[5])

        scale = np.array([[a, 0, 0, 0], [0, b, 0, 0], [0, 0, c, 0], [0, 0, 0, 1]])

        projMat = np.dot(Rx, tranVRP_ORJ)
        projMat = np.dot(Ry, projMat)
        projMat = np.dot(Rz, projMat)
        projMat = np.dot(shear, projMat)
        projMat = np.dot(tran2, projMat)
        projMat = np.dot(scale, projMat)
        return projMat

    def get_projectedpoints(self):
        temp = []
        for element in self.vertex_list:
            #element.append(1)
            element = np.array(element, dtype=float)
            pPoint = self.projMat.dot(element)
            pPoint = pPoint.tolist()
            pPoint = pPoint[:-1]
            temp.append(pPoint)
        self.vertex_list = temp

    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.world = self

    def create_graphic_objects(self, canvas, data):
        self.data = data
        self.width = canvas.cget("width")
        self.height = canvas.cget("height")
        self.create_edge_list()
        self.create_vertex_list()
        #self.get_viewport()
        #self.get_window()
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
            tempList.append(element)

        for element in tempList:
            element = np.array(element)
            element = element.dot(Mat)
            temp = element
            temp = temp.tolist()
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
        canvas.delete("all")
        self.translate_points()
        self.create_draw_list()
        a = self.view_dimension
        dimension = self.translateViewport(a[0], a[1], a[2], a[3])

        self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black'))
        for elements in self.draw_list:
            self.objects.append(canvas.create_line(elements))

    def clip(self):
        list = []
        temp = []
        #for element in self.vertex_list:



    def assign_parallel_outcode(x, y, z):
        outcode = 0b000000
        if x > 1:
            outcode = 0b100000
        elif x < -1:
            outcode = 0b010000
        if y > 1:
            outcode = outcode | 0b001000
        elif y < -1:
            outcode = outcode | 0b000100
        if z > 1:
            outcode = outcode | 0b000010
        elif z < 0:
            outcode = outcode | 0b000001
        return outcode

    def clip_line_parallel(self, p1, p2):
        # This function returns [] if the line is rejected.
        x1 = p1[0]
        y1 = p1[1]
        z1 = p1[2]
        x2 = p2[0]
        y2 = p2[1]
        z2 = p2[2]
        RIGHT = 0b100000
        LEFT = 0b010000
        TOP = 0b001000
        BOTTOM = 0b000100
        FAR = 0b000010
        NEAR = 0b000001
        input_point_1_outcode = self.assign_parallel_outcode(x1, y1, z1);
        input_point_2_outcode = self.assign_parallel_outcode(x2, y2, z2);
        while True:
            if input_point_1_outcode & input_point_2_outcode:
                return []
            if not (input_point_1_outcode | input_point_2_outcode):
                return [[x1, y1, z1], [x2, y2, z2]]
            if input_point_1_outcode:
                outcode = input_point_1_outcode
            else:
                outcode = input_point_2_outcode
            if outcode & RIGHT:
                # Point is on the right of volume
                x = 1
                y = (y2 - y1) * (1 - x1) / (x2 - x1) + y1
                z = (z2 - z1) * (1 - x1) / (x2 - x1) + z1
            elif outcode & LEFT:
                # Point is on the left of volume
                x = -1
                y = (y2 - y1) * (-1 - x1) / (x2 - x1) + y1
                z = (z2 - z1) * (-1 - x1) / (x2 - x1) + z1
            elif outcode & TOP:
                # Point is on above the volume
                x = (x2 - x1) * (1 - y1) / (y2 - y1) + x1
                y = 1
                z = (z2 - z1) * (1 - y1) / (y2 - y1) + z1
            elif outcode & BOTTOM:
                # Point is below the volume
                x = (x2 - x1) * (-1 - y1) / (y2 - y1) + x1
                y = -1
                z = (z2 - z1) * (-1 - y1) / (y2 - y1) + z1
            elif outcode & FAR:
                x = (x2 - x1) * (1 - z1) / (z2 - z1) + x1
                y = (y2 - y1) * (1 - z1) / (z2 - z1) + y1
                z = 1
            elif outcode & NEAR:
                x = (x2 - x1) * (-z1) / (z2 - z1) + x1
                y = (y2 - y1) * (-z1) / (z2 - z1) + y1
                z = 0
            if outcode == input_point_1_outcode:
                x1 = x
                y1 = y
                z1 = z
                input_point_1_outcode = self.assign_parallel_outcode(x1, y1, z1)
            else:
                x2 = x
                y2 = y
                z2 = z
                input_point_2_outcode = self.assign_parallel_outcode(x2, y2, z2)

    def create_vertex_list(self):
        self.vertex_list = []
        for element in self.data:
            if element[0] == 'v':
                self.vertex_list.append([float(element[1]), float(element[2]), float(element[3]), 1.0])

        temp = []
        mat = self.projMat
        for element in self.vertex_list:
            element = np.array(element)
            element = np.dot(mat, element)
            element = element.tolist()
            temp.append(element)

        self.vertex_list = temp


    def create_edge_list(self):
        self.edge_list = []
        for element in self.data:
            if element[0] == 'f':
                self.edge_list.append(element)

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

            self.translate_points()
            self.create_draw_list()

            a = self.view_dimension
            dimension = self.translateViewport(a[0], a[1], a[2], a[3])
            self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black'))
            for elements in self.draw_list:
                self.objects.append(canvas.create_polygon(elements, outline='black', fill='red'))