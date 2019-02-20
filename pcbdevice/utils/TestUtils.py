def readIntFile(filePath):
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
	file = open(filePath, 'r')
	lines = file.readlines()
	file.close()
	
	return lines