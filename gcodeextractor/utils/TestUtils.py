def readIntFile(filePath):
	"""
	Read a matrix file
	
	:param filePath: File path to read from
	:return: The matrix in int
	"""
	completeFile = []
	file = open(filePath, 'r')
	lines = file.readlines()
	file.close()
	
	for line in lines:
		tempArray = []
		for val in line.split():
			tempArray.append(int(val))
			
		completeFile.append(tempArray)
	
	return completeFile

def readStringFile(filePath):
	"""
	Read all lines of a file
	
	:param filePath: File path to read from
	:return: Array of all lines in the file
	"""
	file = open(filePath, 'r')
	lines = file.readlines()
	file.close()
	
	return lines