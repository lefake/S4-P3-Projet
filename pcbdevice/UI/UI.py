from tkinter import *

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
    self.Box = Entry(frame)
    self.Box.pack(side=RIGHT)

class button:
	def __init__(self, master):
		self.master = master
		self.createWidget(master)

	def execution(self):
		main(PCB.Box.get(), Gcode.Box.get(), bool(ascii.Box.get()), int(Width.Box.get()), int(Height.Box.get()),
		     int(radius.Box.get()), unit.Box.get())

	def createWidget(self, master):
		frame = Frame(master, width=500, height=30, )
		frame.pack(side=BOTTOM)
		frame.pack_propagate(0)
		Butt = Button(frame, text = 'execute program', command = self.execution)
		Butt.pack(side = RIGHT)

root.title('totally not a virus')
root.geometry("550x300")

#path = textBox(root, 'Program path')
PCB = textBox(root, 'PCB image path')
Gcode = textBox(root, 'Gcode output path')
ascii = textBox(root, 'If the image is in ascii(True) or binary(False)')
Width = textBox(root, 'Width of the PCB')
Height = textBox(root, 'Height of the PCB')
radius = textBox(root, 'Tool\'s radius in mm')
unit = textBox(root, 'PCB dimension unit')

button = button(root)

root.mainloop()
