from pcbdevice.utils.path import path
from pcbdevice.utils.plotimg import plotPath
from pcbdevice.utils.FileUtils import FileUtils

if __name__ == "__main__":
	# Usage example

	resourcesRawPath = 'tests/resources/raw/'
	resourcesFormattedPath = 'tests/resources/formatted/'
	resourcesPathOutput = 'resources/pathoutput/'

	FileUtils.saveMatrixToFile(FileUtils.pbmToCsv(resourcesRawPath + 'test1ascii.pbm'), resourcesFormattedPath + 'test1.csv')

	plotPath(path(FileUtils.pbmToCsv(resourcesRawPath + 'test100x100.pbm'), 5))