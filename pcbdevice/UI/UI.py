import os
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from tkinter.ttk import Combobox
import subprocess

from pcbdevice.main import main

root = Tk()
frame = Frame(root)
frame.pack()

class textBox:
  def __init__(self, master, parameter, text):
    self.master = master
    self.createWidget(master, parameter, text)

  def createWidget(self, master, parameter, text):
    frame = Frame(master, width=500, height=30, )
    frame.pack(side=TOP)
    frame.pack_propagate(0)

    Text = Label(frame, text=parameter)
    Text.pack(side=LEFT)
    self.v = StringVar(frame, value=text)
    self.Box = Entry(frame, width = 20, textvariable = self.v)
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
		self.v = StringVar(frame, value = selection[0])
		self.Box = Combobox(frame, state = 'readonly', values = selection, width = 17, textvariable = self.v)
		self.Box.pack(side=RIGHT)

class button:
	def __init__(self, master):
		self.master = master
		self.createWidget(master)

	def execution(self):
		if self.verifyEntry():
			main(PCB.path, Gcode.path, bool(ascii.Box.current()), int(Width.Box.get()), int(Height.Box.get()),
			     int(radius.Box.get()), unit.Box.get())
			os.startfile(Gcode.path.rsplit('/', 1)[0])
		else:
			print('FAIL')

	def verifyEntry(self):
		if not Width.Box.get().isdigit():
			self.State.config(text = 'ERROR: Width needs to be a positive integer', fg = 'red', font = 'Helvetica 10 bold')
			return 0
		if not Height.Box.get().isdigit():
			self.State.config(text = 'ERROR: Height needs to be a positive integer', fg = 'red', font = 'Helvetica 10 bold')
			return 0
		if not radius.Box.get().isdigit():
			self.State.config(text = 'ERROR: Tool radius needs to be a positive integer', fg = 'red', font = 'Helvetica 10 bold')
			return 0
		if not (radius.Box.get() < Width.Box.get() or radius.Box.get() < Height.Box.get()):
			self.State.config(text = 'ERROR: Tool radius needs to be smaller than Width and Height', fg = 'red', font = 'Helvetica 10 bold')
			return 0
		if not os.path.isfile(PCB.path) or not PCB.path.endswith('.pbm'):
			self.State.config(text = 'ERROR: Unable to find PCB file or file type is not .pbm', fg = 'red', font = 'Helvetica 10 bold')
			return 0
		if not Gcode.path.endswith('.gcode'):
			self.State.config(text = 'ERROR: File type is not .gcode', fg = 'red', font = 'Helvetica 10 bold')
			return 0

		self.State.config(text='SUCCESS: (ง ͠° ͟ل͜ ͡°)ง', fg='green', font='Helvetica 10 bold')
		return 1


	def createWidget(self, master):
		frame = Frame(master, width=500, height=30, )
		frame.pack(side=BOTTOM)
		frame.pack_propagate(0)
		self.State = Label(frame, text='')
		self.State.pack(side=LEFT)
		Butt = Button(frame, text = 'execute program', command = lambda: self.execution())
		Butt.pack(side = RIGHT)

class pathFind:

	path = ''

	def __init__(self, master, parameter, openSave):
	  self.master = master
	  self.createWidget(master, parameter, openSave)

	def openDir(self):
		self.path = str(askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pbm files","*.pbm"),("all files","*.*"))))
		self.Box.insert(END, self.path)

	def saveDir(self):
		self.path = str(asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("pbm files","*.gcode"),("all files","*.*"))))
		self.Box.insert(END, self.path)

	def createWidget(self, master, parameter, openSave):
		frame = Frame(master, width=500, height=30, )
		frame.pack(side=TOP)
		frame.pack_propagate(0)

		Text = Label(frame, text=parameter)
		Text.pack(side=LEFT)
		if openSave:
			Butt = Button(frame, text = 'search', command = lambda: self.openDir())
		else:
			Butt = Button(frame, text = 'search', command = lambda: self.saveDir())
		Butt.pack(side = RIGHT)
		self.Box = Entry(frame, width=45)
		self.Box.pack(side=RIGHT, padx = 3)

def display(this):
	print(this)

root.title('totally not a virus')
root.geometry("550x300")

#path = textBox(root, 'Program path')
PCB = pathFind(root, 'PCB image path', TRUE)
Gcode = pathFind(root, 'Gcode output path', FALSE)
ascii = menuBox(root, 'If the image is in ascii or binary', ['binary','ascii'])
Width = textBox(root, 'Width of the PCB', 100)
Height = textBox(root, 'Height of the PCB', 100)
radius = textBox(root, 'Tool\'s radius in mm', 1)
unit = menuBox(root, 'PCB dimension unit', ['mm', 'm', 'in'])

button = button(root)

root.mainloop()
