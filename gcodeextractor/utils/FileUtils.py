import math

class FileUtils:
	@staticmethod
	def pbmToMatrix(pbmFilePath, dimensionLineIndex = 2):
		"""
		Read a pbm file and convert in an int matrix
		
		:param str pbmFilePath: Path of the ascii pbm file to convert in a matrix
		:param int dimensionLineIndex: Line index containing the dimension of the image
		:return matrix: Matrix with image value
		:return height: Height of the matrix
		:return width: Width of the matrix
		"""
		
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
		"""
		Save a matrix in a plain text file
		
		:param matrix: Matrix to save
		:param filePath: Path of the output file
		:return: None
		"""
		with open(filePath, 'w') as f:
			for x in matrix:
				for y in x:
					f.write('%s ' % y )
				f.write('\n')
			f.close()
			
	@staticmethod
	def saveStringListToFile(stringList, filePath):
		"""
		Save a string list into a plain text file with a carriage return after each entry
		
		:param stringList: List of string to write
		:param filePath: File path to write the text
		:return: None
		"""
		with open(filePath, 'w') as f:
			for line in stringList:
				f.write('%s\n' % line)
			f.close()
			
	@staticmethod
	def getPixelSize(matHeight, matWidth, pcbHeight, pcbWidth, unit = 'mm'):
		"""
		Get pixel width and height with the real image size
		
		:param matHeight: Height of the image matrix (Nb pixels)
		:param matWidth: Width of the image matrix (Nb pixels)
		:param pcbHeight: True height of the image (PCB)
		:param pcbWidth: True width of the image (PCB)
		:param unit: Unit of the size of the image, default in mm
		:return pixelHeight: Pixel height in mm
		:return pixelWidth: Pixel width in mm
		
		"""
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