from pcbdevice.utils.path import path
from pcbdevice.utils.pbmformator import formatPbm
from pcbdevice.utils.savetofile import matrixToFile

if __name__ == "__main__":
	# Usage example

	resourcesRawPath = 'tests/resources/raw/'
	resourcesFormattedPath = 'tests/resources/formatted/'
	resourcesPathOutput = 'resources/pathoutput/'

	matrixToFile(formatPbm(resourcesRawPath + 'test1ascii.pbm'), resourcesFormattedPath + 'test1.csv')

	matrixToFile(path(formatPbm(resourcesRawPath + 'test100x100.pbm'), 4), resourcesPathOutput + 'test100x100.csv')



