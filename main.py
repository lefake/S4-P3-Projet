from utils.path import path, scanHorizontal, scanVertical
from utils.pbmformator import formatPbm
from utils.savetofile import matrixToFile

if __name__ == "__main__":
	# Usage example
	matrixToFile(formatPbm('resources/original/test1ascii.pbm'), 'resources/reformatted/test1.csv')

	#matrixToFile(scanHorizontal(formatPbm('resources/original/test1ascii.pbm'), 4), 'resources/reformatted/testhori.csv')
	#matrixToFile(scanVertical(formatPbm('resources/original/test1ascii.pbm'), 4 ), 'resources/reformatted/testvert.csv')
	#matrixToFile(twoTooMany(scanVertical(scanHorizontal(formatPbm('resources/original/test1ascii.pbm'), 4),4),4), 'resources/reformatted/testfinal.csv')
#	matrixToFile(path(formatPbm('resources/original/imagestest-11.pbm'), 4), 'resources/reformatted/testimagestest-11.csv')
#	matrixToFile(path(formatPbm('resources/original/imagestest-22.pbm'), 4), 'resources/reformatted/testimagestest-22.csv')
#	matrixToFile(path(formatPbm('resources/original/imagestest-33.pbm'), 4), 'resources/reformatted/testimagestest-33.csv')
	matrixToFile(path(formatPbm('resources/original/test100x100_1.pbm'), 4), 'resources/reformatted/test100x100.csv')
	matrixToFile(scanVertical(formatPbm('resources/original/test100x100_1.pbm'), 4), 'resources/reformatted/test100x100V.csv')
	matrixToFile(scanHorizontal(formatPbm('resources/original/test100x100_1.pbm'), 4), 'resources/reformatted/test100x100H.csv')
	matrixToFile(scanVertical(scanHorizontal(formatPbm('resources/original/test100x100_1.pbm'), 4) ,4), 'resources/reformatted/test100x100VH.csv')



