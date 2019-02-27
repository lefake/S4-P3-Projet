import math

from pcbdevice.gcode.GcodeBuilder import listToGCode

from pcbdevice.gcode.GcodeCreator import createSequence
from pcbdevice.gcode.path import path
from pcbdevice.utils.FileUtils import FileUtils
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog = 'main.py')
	parser.add_argument('-i', required = True, help = 'PCB image path')
	parser.add_argument('-o', required = True, help = 'Gcode output path')
	parser.add_argument('-wi', required = True, type = int, help = 'Width of the PCB')
	parser.add_argument('-he', required = True, type = int, help = 'Height of the PCB')
	parser.add_argument('-t', required = True, type = int, help = 'Tool\'s radius in mm')
	parser.add_argument('-u', required = False, help = 'PCB dimension unit')
	args = parser.parse_args()
	
	matrix, height, width = FileUtils.pbmToMatrix(args.i)
	
	if args.u:
		pxHeight, pxWidth = FileUtils.getPixelSize(height, width, args.he, args.wi, unit = args.u)
	else:
		pxHeight, pxWidth = FileUtils.getPixelSize(height, width, args.he, args.wi)
	
	if pxHeight > pxWidth:
		rTool = int(math.ceil(args.t * pxHeight))
	else:
		rTool = int(math.ceil(args.t * pxWidth))
	
	matrixUpdated = path(matrix, rTool)
	listIndexes = createSequence(matrixUpdated)
	gcode = listToGCode(listIndexes, pxHeight, pxWidth)
	FileUtils.saveStringListToFile(gcode, args.o)