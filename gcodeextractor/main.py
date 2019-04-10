import math

from gcodeextractor.gcode.GcodeBuilder import listToGCode

from gcodeextractor.gcode.GcodeCreator import createSequence
from gcodeextractor.gcode.path import path
from gcodeextractor.utils.FileUtils import FileUtils
import argparse
import subprocess

def main(inputPath, outputPath, isAscii, heightReal, widthReal, tool, unit):
	converterPath = '.\\gcodeextractor\\utils\\convertiseur.exe'
	
	if outputPath.rfind('\\') != -1:
		asciiPbmPath = outputPath[0:outputPath.rfind('\\')] + '\\pcbImageAscii.pbm'
	elif outputPath.rfind('/') != -1:
		asciiPbmPath = outputPath[0:outputPath.rfind('/')] + '/pcbImageAscii.pbm'
	else:
		asciiPbmPath = '.\\gcodeextractor\\resources\\output\\pcbImageAscii.pbm'
		
	if not isAscii:
		subprocess.check_call([converterPath, inputPath, asciiPbmPath])
	
	matrix, height, width = FileUtils.pbmToMatrix(asciiPbmPath)
	
	pxHeight, pxWidth = FileUtils.getPixelSize(height, width, heightReal, widthReal, unit = unit)
	
	if pxHeight > pxWidth:
		rTool = int(math.ceil(tool / pxHeight))
	else:
		rTool = int(math.ceil(tool / pxWidth))
	
	matrixUpdated = path(matrix, rTool)
	listIndexes = createSequence(matrixUpdated)
	gcode = listToGCode(listIndexes, pxHeight, pxWidth)
	FileUtils.saveStringListToFile(gcode, outputPath)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog = 'main.py')
	parser.add_argument('-i', required = True, help = 'PCB image path')
	parser.add_argument('--ascii', required = False, dest='imgTypeisAscii', action = 'store_true', help = 'If the image is in ascii(True) or binary(False)')
	parser.add_argument('-o', required = True, help = 'Gcode output path')
	parser.add_argument('-wi', required = True, type = float, help = 'Width of the PCB')
	parser.add_argument('-he', required = True, type = float, help = 'Height of the PCB')
	parser.add_argument('-t', required = True, type = float, help = 'Tool\'s radius in mm')
	parser.add_argument('-u', required = False, help = 'PCB dimension unit')
	args = parser.parse_args()
	
	unitValue = 'mm'
	isAscii = args.imgTypeisAscii
	
	if args.u:
		unitValue = args.u
		
	if isAscii:
		asciiPbmPath = args.i
	
	main(args.i, args.o, isAscii, args.wi, args.he, args.t, unitValue)