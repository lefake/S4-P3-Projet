"""
	Save a two dimension array in a file
"""

def matrixToFile(matrix, fileName):
	with open(fileName, 'w') as f:
		for x in matrix:
			for y in x:
				f.write('%s ' % y )
			f.write('\n')
	