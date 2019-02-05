import math

"""
	Reformat the file receive by the binary to ascii converter to have matrix with the right width and height
"""


def formatPbm(pbmFile):
	dimensionLineIndex = 2
	completeFile = []
	
	lines = open(pbmFile, 'r').readlines()
	width, height = (int(val) for val in lines[dimensionLineIndex].split())
	
	for line in lines[dimensionLineIndex+1:]:
		for val in line.split():
			completeFile += [int(val)]
	
	formattedFile = [[0 for i in range(width)] for j in range(height)]
	for index, value in enumerate(completeFile):
		formattedFile[math.floor(index/width)][index%width] = value
	
	return formattedFile

