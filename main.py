from utils.pbmformator import formatPbm
from utils.savetofile import matrixToFile

if __name__ == "__main__":
	# Usage example
	matrixToFile(formatPbm('resources/original/test1ascii.pbm'), 'resources/reformatted/test1.csv')