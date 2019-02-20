from pcbdevice.utils.path import path
from pcbdevice.utils.plotimg import plotPath
from pcbdevice.utils.FileUtils import FileUtils
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog = 'main.py')
	parser.add_argument('-i', required = True, help = 'PCB image path')
	parser.add_argument('-wi', required = True, type = int, help = 'Width of the PCB')
	parser.add_argument('-he', required = True, type = int, help = 'Height of the PCB')
	parser.add_argument('-u', required = False, help = 'PCB dimension unit')
	args = parser.parse_args()
	
	matrix, height, width = FileUtils.pbmToMatrix(args.i)
	
	if args.u:
		pxHeight, pxWidth = FileUtils.getPixelSize(height, width, args.he, args.wi, unit = args.u)
	else:
		pxHeight, pxWidth = FileUtils.getPixelSize(height, width, args.he, args.wi)


	resourcesRawPath = 'tests/resources/raw/'
	resourcesFormattedPath = 'tests/resources/formatted/'
	resourcesPathOutput = 'resources/pathoutput/'
	resourcesExpectedPath = 'tests/resources/expected/'

	#FileUtils.saveMatrixToFile(FileUtils.pbmToMatrix(resourcesRawPath + 'test1ascii.pbm'), resourcesFormattedPath + 'test1.csv')

	#plotPath(path(FileUtils.pbmToMatrix(resourcesRawPath + 'test100x100.pbm'), 5))