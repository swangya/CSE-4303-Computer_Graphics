# Saurav, Swangya
# 1001-054-908
# 2017-09-18
# Assignment_01_03


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
        self.translate_points()
        self.create_draw_list()

        a = self.view_dimension
        dimension = self.translateViewport(a[0], a[1], a[2], a[3])
        self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black'))
        for elements in self.draw_list:
            self.objects.append(canvas.create_polygon(elements, outline='black', fill='red'))

    def create_vertex_list(self):
        self.vertex_list = []
        for element in self.data:
            if element[0] == 'v':
                self.vertex_list.append(element)

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
            temp = self.translate_coordinate(element[1], element[2])
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
            temp = []
            for e in elements:
                if e != 'f':
                    x = int(e)-1
                    temp = temp+l[x]
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
            self.objects.append(canvas.create_rectangle(dimension[0], dimension[1], dimension[2], dimension[3], outline='black'))
            for elements in self.draw_list:
                self.objects.append(canvas.create_polygon(elements, outline='black', fill='red'))
