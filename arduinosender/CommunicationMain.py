import serial
import argparse
from time import sleep

from serial import SerialException

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog = 'main.py')
	parser.add_argument('-g', required = True, help = 'GCode file path')
	parser.add_argument('-c', required = True, help = 'Arduino com port')
	parser.add_argument('-t', required = False, type = int, help = 'Communication timout')
	parser.add_argument('-b', required = False, type = int, help = 'Communication baudrate')
	parser.add_argument('-waittime', required = False, type = int, help = 'Sleep time before sending (s)')
	args = parser.parse_args()
	
	timeoutCom = 2
	baudRate = 9600
	commandTimeout = 0
	waitTime = 1
	
	if args.t:
		timeoutCom = int(args.t)
	if args.b:
		baudRate = int(args.b)
	if args.waittime:
		waitTime = int(args.waittime)
		
	ser = None
	try:
		ser = serial.Serial(args.c, baudRate, timeout = timeoutCom)
		sleep(waitTime)
	
		file = open(args.g, 'r')
		lines = file.readlines()
		file.close()
		
		for line in lines:
			if not line == '\n':
				ser.write(line.encode('UTF-8'))

				if not ser.readline().decode('UTF-8').startswith('2'):
					raise RuntimeError('Communication lost')

				while True:
					received = ser.readline().decode('UTF-8')
					if not received.startswith('1') or received.startswith('-1'):
						commandTimeout += 1
						if commandTimeout > timeoutCom * 10:
							raise RuntimeError('Command not executed')
						if received.startswith('-1'):
							raise RuntimeError('Command error')
					else:
						break

		print('Done')
		
		ser.close()
		
	except SerialException as errSE:
		print('Serial Exception' + str(errSE))
	except RuntimeError as errRE:
		print(str(errRE))
	finally:
		if ser is not None:
			ser.close()