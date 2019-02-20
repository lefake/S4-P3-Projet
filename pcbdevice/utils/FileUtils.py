import math

class FileUtils:
	@staticmethod
	def pbmToMatrix(pbmFilePath, dimensionLineIndex = 2):
		completeFile = []
		
		file = open(pbmFilePath, 'r')
		lines = file.readlines()
		width, height = (int(val) for val in lines[dimensionLineIndex].split())
		file.close()
		
		for line in lines[dimensionLineIndex + 1:]:
			for val in line.split():
				completeFile += [int(val)]
		
		matrix = [[0 for i in range(width)] for j in range(height)]
		for index, value in enumerate(completeFile):
			matrix[int(math.floor(index / width))][index % width] = value
		
		return matrix, height, width
	
	@staticmethod
	def saveMatrixToFile(matrix, filePath):
		with open(filePath, 'w') as f:
			for x in matrix:
				for y in x:
					f.write('%s ' % y )
				f.write('\n')
			f.close()
			
	@staticmethod
	def getPixelSize(matHeight, matWidth, pcbHeight, pcbWidth, unit = 'mm'):
		if unit == 'mm':
			return pcbHeight / matHeight, pcbWidth / matWidth
		elif unit == 'cm':
			return pcbHeight / matHeight * 10, pcbWidth / matWidth * 10
		elif unit == 'm':
			return pcbHeight / matHeight * 100, pcbWidth / matWidth * 100
		elif unit == 'in':
			return pcbHeight / matHeight * 25.4, pcbWidth / matWidth * 25.4
		else:
			raise RuntimeError('Unit not handle')