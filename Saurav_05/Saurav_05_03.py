# Saurav, Swangya
# 1001-054-908
# 2017-11-06
# Assignment_05_03

import numpy as np

class cl_world:
    def __init__(self, objects=[], canvases=[]):
        self.objects = objects
        self.canvases = canvases
        self.data = []
        self.vertex_list = []
        self.original_vertex_list = []
        self.edge_list = []
        self.window_dimension = [-1, -1, 1, 1]
        self.view_dimension = []
        self.translated_points = []
        self.draw_list = []
        self.width = 0
        self.height = 0
        self.viewFrameDimensions = []

        self.camData = []
        self.camFrames = []
        self.camNum = 0
        self.progenitorCam = []

        self.cameraName = ''
        self.cameraType = "parallel"
        self.VRP = [0, 0, 0]
        self.VPN = [0, 0, 1]
        self.VUP = [0, 1, 0]
        self.PRP = [0, 0, 1]
        self.VRC = [-1, 1, -1, 1, -1, 1]
        self.viewPort = [0.1, 0.1, 0.4, 0.4]
        self.projMat = []

        #Assignment 5 variables
        self.bezier_list = []
        self.bezier_points = []
        self.init_res = 0

    def put_cameras(self, data, canvas):
        self.camData = data
        self.camNum = len(data)
        temp =[]
        for element1 in data:
            for element2 in element1:
                if element2[0] == 's':
                    temp = self.get_listData(element2)
                    self.view_dimension.append(temp)
        self.width = canvas.cget("width")
        self.height = canvas.cget("height")

        for elements in self.view_dimension:
            a = elements
            dimension = self.translateViewport(a[0], a[1], a[2], a[3])
            self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black', fill='white'))

        for elem in data:
            flg = 0
            for element in elem:
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

            if not self.progenitorCam:
                self.progenitorCam = elem

            if self.cameraType == 'parallel':
                matTemp = self.get_pllProjMat(0)
                self.projMat.append(matTemp)
            else:
                matTemp = self.get_perProjMat(0)
                self.projMat.append(matTemp)
        #print(self.projMat[1])

    def fly_camera(self, canvas, point):
        for element in self.progenitorCam:
            if element[0] == 'i':
                self.cameraName = element[1]
            elif element[0] == 't':
                self.cameraType = element[1]
            elif element[0] == 'r':
                self.VRP = point
                print(self.VRP)
            elif element[0] == 'n':
                self.VPN = self.get_listData(element)
            elif element[0] == 'u':
                self.VUP = self.get_listData(element)
            elif element[0] == 'p':
                self.PRP = self.get_listData(element)
            elif element[0] == 'w':
                self.VRC = self.get_listData(element)

        if self.cameraType == 'parallel':
            matTemp = self.get_pllProjMat(0)
        else:
            matTemp = self.get_perProjMat(0)

        self.projMat[0] = matTemp
        self.vertex_list = self.original_vertex_list
        self.get_projectedVertex()
        i = 0;
        for element in self.vertex_list:
            self.draw(canvas, element, self.view_dimension[i])
            i = i + 1

    def get_listData(self, list):
        retList = []
        length = int(len(list))

        for i in range(1, length):
            retList.append(float(list[i]))

        return retList

    def get_pllProjMat(self, flg):
        if flg == 0:
            VRP = self.VRP
            VRP.append(1)
            VPN = self.VPN
            VPN.append(1)
            VUP = self.VUP
            VUP.append(1)
            PRP = self.PRP
            PRP.append(1)
            UVN = self.VRC
        else:
            VRP = self.VRP
            VRP.append(1)
            VPN = self.VPN
            VUP = self.VUP
            PRP = self.PRP
            UVN = self.VRC

        VRP = np.array(VRP)
        VPN = np.array(VPN)
        VUP = np.array(VUP)
        PRP = np.array(PRP)

        tranVRP_ORJ = np.array([[1.0, 0.0, 0.0, -VRP[0]], [0.0, 1.0, 0.0, -VRP[1]], [0.0, 0.0, 1.0, -VRP[2]], [0.0, 0.0, 0.0, 1.0]])
        VRP = np.dot(tranVRP_ORJ, VRP)

        hyp = np.sqrt(VPN[1] ** 2 + VPN[2] ** 2)
        if hyp == 0:
            a = 1
            b = 0
        else:
            a = float(VPN[2] / hyp)
            b = float(VPN[1] / hyp)
        Rx = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, a, -b, 0.0], [0.0, -b, a, 0.0], [0.0, 0.0, 0.0, 1.0]])
        VPN = np.dot(Rx, VPN)
        VUP = np.dot(Rx, VUP)

        hyp = np.sqrt(VPN[0] ** 2 + VPN[2] ** 2)
        if hyp == 0: hyp = 1
        a = float(VPN[2] / hyp)
        b = float(VPN[0] / hyp)
        Ry = np.array([[a, 0.0, -b, 0.0], [0.0, 1.0, 0.0, 0.0], [b, 0.0, a, 0.0], [0.0, 0.0, 0.0, 1.0]])
        VPN = np.dot(Ry, VPN)
        VUP = np.dot(Ry, VUP)

        hyp = np.sqrt(VUP[0] ** 2 + VUP[1] ** 2)
        if hyp == 0: hyp = 1
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

    def get_perProjMat(self, flg):
        if flg == 0:
            VRP = self.VRP
            VRP.append(1)
            VPN = self.VPN
            VPN.append(1)
            VUP = self.VUP
            VUP.append(1)
            PRP = self.PRP
            PRP.append(1)
            UVN = self.VRC
        else:
            VRP = self.VRP
            VRP.append(1)
            VPN = self.VPN
            VUP = self.VUP
            PRP = self.PRP
            UVN = self.VRC

        VRP = np.array(VRP)
        VPN = np.array(VPN)
        VUP = np.array(VUP)
        PRP = np.array(PRP)

        tranVRP_ORJ = np.array([[1.0, 0.0, 0.0, -VRP[0]], [0.0, 1.0, 0.0, -VRP[1]], [0.0, 0.0, 1.0, -VRP[2]], [0.0, 0.0, 0.0, 1.0]])
        VRP = np.dot(tranVRP_ORJ, VRP)

        hyp = np.sqrt(VPN[1] ** 2 + VPN[2] ** 2)
        if hyp == 0:
            a = 1
            b = 0
        else:
            a = float(VPN[2] / hyp)
            b = float(VPN[1] / hyp)
        Rx = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, a, -b, 0.0], [0.0, b, a, 0.0], [0.0, 0.0, 0.0, 1.0]])
        VPN = np.dot(Rx, VPN)
        VUP = np.dot(Rx, VUP)
        VRP = np.dot(Rx, VRP)

        hyp = np.sqrt(VPN[0] ** 2 + VPN[2] ** 2)
        if hyp == 0: hyp = 1
        a = float(VPN[2] / hyp)
        b = float(VPN[0] / hyp)
        Ry = np.array([[a, 0.0, -b, 0.0], [0.0, 1.0, 0.0, 0.0], [b, 0.0, a, 0.0], [0.0, 0.0, 0.0, 1.0]])
        VPN = np.dot(Ry, VPN)
        VUP = np.dot(Ry, VUP)
        VRP = np.dot(Ry, VRP)

        hyp = np.sqrt(VUP[0] ** 2 + VUP[1] ** 2)
        if hyp == 0: hyp = 1
        a = float(VUP[1] / hyp)
        b = float(VUP[0] / hyp)

        Rz = np.array([[a, -b, 0.0, 0.0], [b, a, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
        VPN = np.dot(Rz, VPN)
        VUP = np.dot(Rz, VUP)
        VRP = np.dot(Rz, VRP)

        #Translate2
        a = -PRP[0]
        b = -PRP[1]
        c = -PRP[2]
        tran2 = np.array([[1, 0, 0, a], [0, 1, 0, b], [0, 0, 1, c], [0, 0, 0, 1]])
        VRP = np.dot(tran2, VRP)

        #shear
        a = (-(PRP[0] - ((UVN[1] + UVN[0]) / 2)) / PRP[2])
        b = (-(PRP[1] - ((UVN[3] + UVN[2]) / 2)) / PRP[2])
        shear = np.array([[1, 0, a, 0], [0, 1, b, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        VRP = np.dot(shear, VRP)

        #scale
        if (np.absolute(VRP[2] + UVN[5]))> (np.absolute(VRP[2]+UVN[4])):
            a = np.absolute(VRP[2])/(((UVN[1] - UVN[0])/2)*(VRP[2]+UVN[5]))

        else:
            a = np.absolute(VRP[2]) / (((UVN[1] - UVN[0]) / 2) * (VRP[2] + UVN[4]))

        if (np.absolute(VRP[2] + UVN[5]))> (np.absolute(VRP[2]+UVN[4])):
            b = np.absolute(VRP[2]) / (((UVN[3] - UVN[2]) / 2) * (VRP[2] + UVN[5]))
        else:
            b = np.absolute(VRP[2]) / (((UVN[3] - UVN[2]) / 2) * (VRP[2] + UVN[4]))

        if ((VRP[2]+UVN[5])*(VRP[2]+UVN[4]))<0:
            print("Error: Two sided Volume")
        elif (np.absolute(VRP[2] + UVN[5]))> (np.absolute(VRP[2]+UVN[4])):
            c = 1/(VPN[2]+UVN[5])
        else:
            c = 1/(VPN[2]+UVN[4])

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


    def translation(self, tPoints, canvas):
        Dx = float(tPoints[0])
        Dy = float(tPoints[1])
        Dz = float(tPoints[2])

        self.drawTranslation(Dx, Dy, Dz)

        i = 0;
        for element in self.vertex_list:
            self.draw(canvas, element, self.view_dimension[i])
            i = i + 1

    def drawTranslation(self, x, y, z):
        self.vertex_list = []
        points = np.array(self.original_vertex_list, dtype=float)
        tPoints = np.array([x, y, z, 0], dtype=float)
        translatedPoints = points + tPoints
        self.vertex_list = translatedPoints.tolist()
        self.original_vertex_list = self.vertex_list
        self.get_projectedVertex()

    def scaling(self, point, factor, canvas):
        factor = float(factor)
        x = float(point[0])
        y = float(point[1])
        z = float(point[2])

        self.drawTranslation(-x, -y, -z)
        self.drawScaling(factor, canvas)
        self.drawTranslation(x, y, z)
        canvas.delete("all")

        i = 0;
        for element in self.vertex_list:
            self.draw(canvas, element, self.view_dimension[i])
            i = i + 1

    def drawScaling(self, factor, canvas):
        self.vertex_list = []
        Scalepoints = np.array(self.original_vertex_list, dtype=float)
        sFactor = np.array([factor, factor, factor, 1])
        translatedPoints = Scalepoints * sFactor
        self.original_vertex_list = translatedPoints.tolist()
        self.vertex_list = self.original_vertex_list
        self.get_projectedVertex()
        i = 0;
        for element in self.vertex_list:
            self.draw(canvas, element, self.view_dimension[i])
            i = i + 1

    def Rotate(self, A, B, line, angle, canvas):
        tempList = []
        rotatedPoints = []

        Mat = self.rotationMat(A, B, angle)

        for element in self.original_vertex_list:
            element = [float(i) for i in element]
            tempList.append(element)

        for element in tempList:
            element = np.array(element)
            element = element.dot(Mat)
            temp = element
            temp = temp.tolist()
            rotatedPoints.append(temp)


        self.vertex_list = []
        self.vertex_list = rotatedPoints
        self.original_vertex_list = rotatedPoints
        self.get_projectedVertex()
        canvas.delete("all")
        i = 0;
        for element in self.vertex_list:
            self.draw(canvas, element, self.view_dimension[i])
            i = i + 1

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

    def create_graphic_objects(self, canvas, data):
        canvas.delete("all")
        self.data = data
        self.width = canvas.cget("width")
        self.height = canvas.cget("height")
        self.create_edge_list()
        self.create_vertex_list()

        i = 0;
        for element in self.vertex_list:
            self.draw(canvas, element, self.view_dimension[i])
            i = i+1

    def draw(self, canvas, vList, vPort):
        #canvas.delete("all")
        tpoints = self.translate_points(vList, vPort)
        dlist = self.create_draw_list(vList, tpoints)

        a = vPort
        dimension = self.translateViewport(a[0], a[1], a[2], a[3])
        self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black', fill='white'))

        for elements in dlist:
            self.objects.append(canvas.create_line(elements))

    def create_vertex_list(self):
        self.vertex_list = []
        self.bezier_list = []
        temp = []
        temp1 = []
        for element in self.data:
            if element[0] == 'n':
                self.init_res = int(element[1])
            if element[0] == 'v':
                temp.append([float(element[1]), float(element[2]), float(element[3]), 1.0])
            if element[0] == 'b':
                temp1.append([float(element[1]), float(element[2]), float(element[3])])
        self.bezier_list = temp1
        self.original_vertex_list = temp
        self.get_bezier_points()
        self.get_projectedVertex()

    def get_bezier_points(self):
        total = len(self.bezier_list)
        bezier_P_list = []
        temp = []
        for i in range(0, total, 4):
            temp = []
            for j in range(i, (i+4)):
                temp.append(self.bezier_list[j])
            bezier_P_list.append(temp)

        #Bernstein basis functions
        uinc = 1.0/float(self.init_res)
        u = uinc;
        B = []
        B0 = []
        B1 = []
        B2 = []
        B3 = []

        for i in range(0, self.init_res):
            u_sqr = np.square(u)
            tmp = 1.0 - u
            tmp_sqr = np.square(tmp)
            B0.append(tmp * tmp_sqr)
            B1.append(3 * u * tmp_sqr)
            B2.append(3 * u_sqr * tmp)
            B3.append(u * u_sqr)
            u = u+uinc
        B.append(B0)
        B.append(B1)
        B.append(B2)
        B.append(B3)

        


    '''
    def get_b_surface_points(self, Plist):
        M = np.array([[1.0, 0.0, 0.0, 0.0], [-3.0, 3.0, 0.0, 0.0], [3.0, -6.0, 3.0, 0.0], [-1.0, 3.0, -3.0, 1.0]])
        t0 = np.array([1.0, 0.0, 0.0, 0.0])
        t1 = np.array([1.0, 1.0, 1.0, 1.0])
        P = np.array(Plist)

        Point0 = t0.dot(M.dot(P))
        Point1 = t1.dot(M.dot(P))

        return [Point0.tolist(), Point1.tolist()]
    '''

    def get_projectedVertex(self):
        vertTemp = []
        for element in self.projMat:
            mat = element
            temp = []
            for element1 in self.original_vertex_list:
                element1 = np.array(element1)
                element1 = np.dot(mat, element1)
                element1 = element1.tolist()
                temp.append(element1)
            vertTemp.append(temp)
        self.vertex_list = vertTemp

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

    def translate_points(self, vList, vPort):
        translated_points = []
        for element in vList:
            temp = self.translate_coordinate(element[0], element[1], vPort)
            translated_points.append(temp)
        return translated_points

    def translate_coordinate(self, pwx, pwy, vd):
        a = self.window_dimension
        b = vd

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

    def create_draw_list(self, vList, tList):
        dlist = []
        l = tList
        clip = []
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

                p1 = vList[x]
                p2 = vList[y]


                clip = self.clip_line_parallel(p1, p2)

                if clip != []:
                    temp = [point1[0], point1[1], point2[0], point2[1]]
                    dlist.append(temp)
        return dlist

    def assign_parallel_outcode(self, x, y, z):
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

    def redisplay(self, canvas, event):
        if self.objects:
            self.width = float(event.width)
            self.height = float(event.height)

            canvas.delete("all")

            i = 0;
            for element in self.vertex_list:
                self.draw(canvas, element, self.view_dimension[i])
                i = i + 1

            #self.translate_points()
            #self.create_draw_list()
            for a in self.view_dimension:
                dimension = self.translateViewport(a[0], a[1], a[2], a[3])
                self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black'))
            for elements in self.draw_list:
                self.objects.append(canvas.create_polygon(elements, outline='black', fill='red'))