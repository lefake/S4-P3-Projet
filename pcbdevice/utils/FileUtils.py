import math

class FileUtils:
	@staticmethod
	def pbmToCsv(pbmFile, dimensionLineIndex = 2):
		completeFile = []
		
		file = open(pbmFile, 'r')
		lines = file.readlines()
		width, height = (int(val) for val in lines[dimensionLineIndex].split())
		file.close()
		
		for line in lines[dimensionLineIndex + 1:]:
			for val in line.split():
				completeFile += [int(val)]
		
		matrix = [[0 for i in range(width)] for j in range(height)]
		for index, value in enumerate(completeFile):
			matrix[math.floor(index / width)][index % width] = value
		
		return matrix
	
	@staticmethod
	def saveMatrixToFile(matrix, filePath):
		with open(filePath, 'w') as f:
			for x in matrix:
				for y in x:
					f.write('%s ' % y )
				f.write('\n')
			f.close()