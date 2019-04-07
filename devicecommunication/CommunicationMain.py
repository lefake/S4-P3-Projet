from serial import Serial
from serial import SerialException

from time import sleep
from tkinter import *
from tkinter.ttk import Notebook

global serial

class LabelWithEntry:
	def __init__(self, parent, labelText, padXLeft = (0, 0), padYLeft = (0, 0), padXRight = (0, 0), padYRight = (0, 0)):
		frame = Frame(parent)
		frame.pack(side = TOP, fill = BOTH, expand = 1)
		self.label = Label(frame, text = labelText)
		self.label.pack(side = LEFT, padx = padXLeft, pady = padYLeft)
		self.entry = Entry(frame)
		self.entry.pack(side = RIGHT, padx = padXRight, pady = padYRight)
	
	def get(self):
		return self.entry.get()
	
	def setText(self, text):
		self.entry.insert(END, text)

def openSerial(com, baudRate, communicationTimeout, waitTime):
	global serial
	
	try:
		serial = Serial(com, int(baudRate), timeout = int(communicationTimeout))
		sleep(int(waitTime))
	except SerialException as errSE:
		raise errSE

def closeSerial():
	global serial
	
	try:
		serial.close()
	except SerialException as errSE:
		raise errSE

def readFile(filePath):
	file = open(filePath, 'r')
	lines = file.readlines()
	file.close()
	
	return lines

def sendAllLines(lines, timeoutCom):
	global serial
	
	for line in lines:
		if not line == '\n':
			sendWithAck(line, timeoutCom)

def sendWithAck(gcodeCommand, timeoutCom):
	global serial
	commandTimeout = 0
	
	serial.write(gcodeCommand.encode('UTF-8'))
	
	received = serial.readline().decode('UTF-8')
	
	if received.startswith('-2'):
		raise RuntimeError('Device error, please reset the device')
	elif not received.startswith('2'):
		raise RuntimeError('Communication lost')
	while True:
		received = serial.readline().decode('UTF-8')
		
		if received.startswith('1'):
			break
		elif received.startswith('-2'):
			raise RuntimeError('Device error, please reset the device')
		elif received.startswith('-1'):
			raise RuntimeError('Command error : ' + gcodeCommand)
		else:
			commandTimeout += 1
			if commandTimeout > timeoutCom * 10:
				raise RuntimeError('Command not executed')


def sendFileToPort(comPort, baudRate, communicationTimeout, waitTime, gcodePath):
	global serial
	
	try:
		openSerial(comPort, baudRate, communicationTimeout, waitTime)
		lines = readFile(gcodePath)
		sendAllLines(lines, communicationTimeout)
		closeSerial()
	except SerialException as errSE:
		print('Serial Exception' + str(errSE))
	except RuntimeError as errRE:
		print(str(errRE))
	finally:
		if serial is not None:
			closeSerial()

def callWithParameters(comPortET, communicationTimeoutET, communicationBaudrateET, waitTimeET, gcodePathET):
	timeoutCom = 2
	baudRate = 9600
	waitTime = 1

	if communicationTimeoutET.get() != '':
		timeoutCom = int(communicationTimeoutET.get())
	if communicationBaudrateET.get() != '':
		baudRate = int(communicationBaudrateET.get())
	if waitTimeET.get() != '':
		waitTime = int(waitTimeET.get())
		
	sendFileToPort(comPortET.get(), baudRate, timeoutCom, waitTime, gcodePathET.get())

def sendX(mov, timeoutCom):
	sendWithAck('G0 X' + str(mov), timeoutCom)
	
def sendY(mov, timeoutCom):
	sendWithAck('G0 Y' + str(mov), timeoutCom)

def sendZ(mov, timeoutCom):
	sendWithAck('G0 Z' + str(mov), timeoutCom)

def sendHome(timeoutCom):
	sendWithAck('G28', timeoutCom)
	
def sendAbsPosition(timeoutCom):
	sendWithAck('G90', timeoutCom)
	
def sendRelativePosition(timeoutCom):
	sendWithAck('G91', timeoutCom)


if __name__ == "__main__":
	mainWindow = Tk()
	mainWindow.title('Hello World!')
	tabControl = Notebook(mainWindow)
	tabAuto = Frame(tabControl)
	tabManual = Frame(tabControl)
	
	# Frames
	autoMainFrame = Frame(tabAuto, width = 300, height = 100)
	autoMainFrame.pack(fill = None, expand = False)
	manualMainFrame = Frame(tabManual, width = 300, height = 100)
	manualMainFrame.pack(fill = None, expand = False)
	
	# Auto mode
	padding = 20
	gcodeEntry = LabelWithEntry(autoMainFrame, 'GCode file', padXLeft = (0, padding))
	comEntry = LabelWithEntry(autoMainFrame, 'COM port', padXLeft = (0, padding))
	baudrateEntry = LabelWithEntry(autoMainFrame, 'Baudrate', padXLeft = (0, padding))
	baudrateEntry.setText('57600')
	
	comTimoutEntry = LabelWithEntry(autoMainFrame, 'Com timout (s)', padXLeft = (0, padding))
	comTimoutEntry.setText('2')
	
	sleepEntry = LabelWithEntry(autoMainFrame, 'Sleep init (s)', padXLeft = (0, padding))
	sleepEntry.setText('2')
	
	Button(autoMainFrame, text = 'Start',
	       command = lambda: callWithParameters(comEntry, baudrateEntry, comTimoutEntry, sleepEntry, gcodeEntry)) \
		.pack(side = BOTTOM, fill = BOTH, expand = 1, pady = (15, 0))
	
	# Manual mode
	buttonsFrame = Frame(manualMainFrame)
	buttonsFrame.pack(side = TOP)
	
	openButton = Button(buttonsFrame, text = 'Open', command = lambda: openSerial(comEntry.get(), int(baudrateEntry.get()), int(comTimoutEntry.get()), int(sleepEntry.get())))
	openButton.grid(row = 0, column = 0)
	closeButton = Button(buttonsFrame, text = 'Close', command = lambda: closeSerial())
	closeButton.grid(row = 0, column = 2)
	
	sendXP5Button = Button(buttonsFrame, text = '+5X', command = lambda: sendX(5, int(comTimoutEntry.get())))
	sendXP5Button.grid(row = 2, column = 2, padx = 5)
	sendXM5Button = Button(buttonsFrame, text = '-5X', command = lambda: sendX(-5, int(comTimoutEntry.get())))
	sendXM5Button.grid(row = 2, column = 0, padx = 5)
	
	sendYP5Button = Button(buttonsFrame, text = '+5Y', command = lambda: sendY(5, int(comTimoutEntry.get())))
	sendYP5Button.grid(row = 1, column = 1, pady = 5)
	sendYM5Button = Button(buttonsFrame, text = '-5Y', command = lambda: sendY(-5, int(comTimoutEntry.get())))
	sendYM5Button.grid(row = 3, column = 1, pady = 5)
	
	sendHomeButton = Button(buttonsFrame, text = 'Home', command = lambda: sendHome(int(comTimoutEntry.get())))
	sendHomeButton.grid(row = 2, column = 1)
	
	sendZP5Button = Button(buttonsFrame, text = '+5Z', command = lambda: sendZ(5, int(comTimoutEntry.get())))
	sendZP5Button.grid(row = 3, column = 2)
	sendZM5Button = Button(buttonsFrame, text = '-5Z', command = lambda: sendZ(-5, int(comTimoutEntry.get())))
	sendZM5Button.grid(row = 1, column = 2)
	
	sendZP5Button = Button(buttonsFrame, text = 'G90', command = lambda: sendAbsPosition(int(comTimoutEntry.get())))
	sendZP5Button.grid(row = 1, column = 0)
	sendZM5Button = Button(buttonsFrame, text = 'G91', command = lambda: sendRelativePosition(int(comTimoutEntry.get())))
	sendZM5Button.grid(row = 3, column = 0)
	
	customCommandFrame = Frame(manualMainFrame)
	customCommandFrame.pack(side = BOTTOM, fill = BOTH, expand = 1)
	
	customCommand = Entry(customCommandFrame)
	customCommand.pack(side = LEFT, fill = BOTH, expand = 1)
	Button(customCommandFrame, text = 'Send', command = lambda: sendWithAck(customCommand.get(), int(comTimoutEntry.get()))).pack(side = RIGHT)
	
	tabControl.add(tabAuto, text = 'Auto')
	tabControl.add(tabManual, text = 'Manual')
	tabControl.pack(expand = 1, fill = BOTH)
	mainWindow.mainloop()
	
	closeSerial()