# Saurav, Swangya
# 1001-054-908
# 2017-09-18
# Assignment_01_02


import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox


class cl_widgets:
    def __init__(self, ob_root_window, ob_world=[]):
        self.ob_root_window = ob_root_window
        self.ob_world = ob_world
        self.menu = cl_menu(self)
        self.toolbar = cl_toolbar(self)
        #self.buttons_panel_01 = cl_buttons_panel_01(self)
        #self.buttons_panel_02 = cl_buttons_panel_02(self)
        # Added status bar. Kamangar 2017_08_26
        self.statusBar_frame = cl_statusBar_frame(self.ob_root_window)
        self.statusBar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.statusBar_frame.set('%s', 'This is the status bar')
        self.ob_canvas_frame = cl_canvas_frame(self)
        self.ob_world.add_canvas(self.ob_canvas_frame.canvas)
        self.lines = []
        self.flg = 0;


class cl_canvas_frame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master.ob_root_window, width=640, height=640, bg="yellow")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind('<Configure>', self.canvas_resized_callback)

    def canvas_resized_callback(self, event):
        self.canvas.config(width=event.width - 4, height=event.height - 4)
        # self.canvas.pack()
        self.master.statusBar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.master.statusBar_frame.set('%s','Canvas width = '+str( self.canvas.cget("width"))+ \
                                        '   Canvas height = '+str( self.canvas.cget("height")))
        self.canvas.pack()
        self.master.ob_world.redisplay(self.master.ob_canvas_frame.canvas, event)


class MyDialog(tk.simpledialog.Dialog):
    def body(self, master):

        tk.Label(master, text="Integer:").grid(row=0, sticky=tk.W)
        tk.Label(master, text="Float:").grid(row=1, column=0, sticky=tk.W)
        tk.Label(master, text="String:").grid(row=1, column=2, sticky=tk.W)
        self.e1 = tk.Entry(master)
        self.e1.insert(0, 0)
        self.e2 = tk.Entry(master)
        self.e2.insert(0, 4.2)
        self.e3 = tk.Entry(master)
        self.e3.insert(0, 'Default text')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=1, column=3)

        self.cb = tk.Checkbutton(master, text="Hardcopy")
        self.cb.grid(row=3, columnspan=2, sticky=tk.W)

    def apply(self):
        try:
            first = int(self.e1.get())
            second = float(self.e2.get())
            third = self.e3.get()
            self.result = first, second, third
        except ValueError:
            tk.tkMessageBox.showwarning(
                "Bad input",
                "Illegal values, please try again"
            )

class cl_statusBar_frame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class cl_menu:
    def __init__(self, master):
        self.master = master
        self.menu = tk.Menu(master.ob_root_window)
        master.ob_root_window.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.menu_callback)
        self.filemenu.add_command(label="Open...", command=self.menu_callback)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.menu_callback)
        self.dummymenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Dummy", menu=self.dummymenu)
        self.dummymenu.add_command(label="Item1", command=self.menu_item1_callback)
        self.dummymenu.add_command(label="Item2", command=self.menu_item2_callback)
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.menu_help_callback)

    def menu_callback(self):
        self.master.statusBar_frame.set('%s',"called the menu callback!")

    def menu_help_callback(self):
        self.master.statusBar_frame.set('%s',"called the help menu callback!")

    def menu_item1_callback(self):
        self.master.statusBar_frame.set('%s',"called item1 callback!")

    def menu_item2_callback(self):
        self.master.statusBar_frame.set('%s',"called item2 callback!")

class cl_toolbar:
    def __init__(self, master):
        self.var_filename = tk.StringVar()
        self.var_filename.set('')
        self.lines = []
        self.master = master
        self.toolbar = tk.Frame(master.ob_root_window)
        self.button = tk.Button(self.toolbar, text="Draw", width=16, command=self.toolbar_draw_callback)
        self.button.pack(side=tk.LEFT, padx=2, pady=2)
        self.button = tk.Button(self.toolbar, text="Load", width=16, command=self.browse_file)
        self.button.pack(side=tk.RIGHT, padx=2, pady=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def toolbar_draw_callback(self):
        if self.lines:
            if self.master.flg>0:
                self.master.ob_canvas_frame.canvas.delete("all")
            self.master.ob_world.create_graphic_objects(self.master.ob_canvas_frame.canvas, self.lines)
            self.master.flg = 1
        else:
            messagebox.showerror("Error", "No File Loaded")


    def toolbar_callback(self):
        self.master.statusBar_frame.set('%s',"called the toolbar callback!")

    def browse_file(self):
        lines =[]
        self.var_filename.set(tk.filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")]))
        filename = self.var_filename.get()
        with open(filename) as textFile:
            lines = [line.split() for line in textFile]
        list = [x for x in lines if x != []]
        lines = list
        self.master.toolbar.lines = lines
        self.master.statusBar_frame.set('%s', "File Loaded")

