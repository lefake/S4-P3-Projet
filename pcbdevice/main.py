from pcbdevice.utils.path import path
from pcbdevice.utils.pbmformator import formatPbm
from pcbdevice.utils.plotimg import plotPath
from pcbdevice.utils.savetofile import matrixToFile

if __name__ == "__main__":
	# Usage example

	resourcesRawPath = 'tests/resources/raw/'
	resourcesFormattedPath = 'tests/resources/formatted/'
	resourcesPathOutput = 'resources/pathoutput/'
	resourcesExpectedPath = 'tests/resources/expected/'

	# matrixToFile(formatPbm(resourcesRawPath + 'test1ascii.pbm'), resourcesFormattedPath + 'test1.csv')

	matrixToFile(path(formatPbm(resourcesRawPath + 'imagestest-11.pbm'), 4), resourcesExpectedPath + 'imagestest-11.csv')
	matrixToFile(path(formatPbm(resourcesRawPath + 'imagestest-22.pbm'), 4), resourcesExpectedPath + 'imagestest-22.csv')
	matrixToFile(path(formatPbm(resourcesRawPath + 'imagestest-33.pbm'), 4), resourcesExpectedPath + 'imagestest-33.csv')
	#plotPath(path(formatPbm(resourcesRawPath + 'imagestest-22.pbm'), 8))
	#plotPath(path(formatPbm(resourcesRawPath + 'test100x100.pbm'), 5))



