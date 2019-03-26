from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from tkinter.ttk import Combobox

from pcbdevice.main import main

root = Tk()
frame = Frame(root)
frame.pack()

class textBox:
  def __init__(self, master, parameter):
    self.master = master
    self.createWidget(master, parameter)

  def createWidget(self, master, parameter):
    frame = Frame(master, width=500, height=30, )
    frame.pack(side=TOP)
    frame.pack_propagate(0)

    Text = Label(frame, text=parameter)
    Text.pack(side=LEFT)
    self.Box = Entry(frame, width = 20)
    self.Box.pack(side=RIGHT)

class menuBox:
	def __init__(self, master, parameter, selection):
		self.master = master
		self.createWidget(master, parameter, selection)

	def createWidget(self, master, parameter, selection):
		frame = Frame(master, width=500, height=30, )
		frame.pack(side=TOP)
		frame.pack_propagate(0)

		Text = Label(frame, text=parameter)
		Text.pack(side=LEFT)
		self.Box = Combobox(frame, values = selection, width = 17)
		self.Box.pack(side=RIGHT)

class button:
	def __init__(self, master):
		self.master = master
		self.createWidget(master)

	def execution(self):
		main(PCB.path, Gcode.path, bool(ascii.Box.current()), int(Width.Box.get()), int(Height.Box.get()),
		     int(radius.Box.get()), unit.Box.get())


	def createWidget(self, master):
		frame = Frame(master, width=500, height=30, )
		frame.pack(side=BOTTOM)
		frame.pack_propagate(0)
		Butt = Button(frame, text = 'execute program', command = lambda: self.execution())
		Butt.pack(side = RIGHT)

class pathFind:

	path = ''

	def __init__(self, master, parameter, openSave):
	  self.master = master
	  self.createWidget(master, parameter, openSave)

	def openDir(self):
		self.path = str(askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pbm files","*.pbm"))))

	def saveDir(self):
		self.path = str(asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("pbm files","*.gcode"))))

	def createWidget(self, master, parameter, openSave):
		frame = Frame(master, width=500, height=30, )
		frame.pack(side=TOP)
		frame.pack_propagate(0)

		Text = Label(frame, text=parameter)
		Text.pack(side=LEFT)
		if openSave:
			Butt = Button(frame, text = 'find path', command = lambda: self.openDir() )
		else:
			Butt = Button(frame, text = 'find path', command = lambda: self.saveDir() )
		Butt.pack(side = RIGHT)

def display(this):
	print(this)

root.title('totally not a virus')
root.geometry("550x300")

#path = textBox(root, 'Program path')
PCB = pathFind(root, 'PCB image path', TRUE)
Gcode = pathFind(root, 'Gcode output path', FALSE)
ascii = menuBox(root, 'If the image is in ascii or binary', ['binary','ascii'])
Width = textBox(root, 'Width of the PCB')
Height = textBox(root, 'Height of the PCB')
radius = textBox(root, 'Tool\'s radius in mm')
unit = menuBox(root, 'PCB dimension unit', ['mm', 'm', 'in'])

button = button(root)

root.mainloop()
