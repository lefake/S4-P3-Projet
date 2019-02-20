from pcbdevice.models.Coordinates import Coordinate


def findEndOfLine(image, direction, line, column, sequence):
	"""
	Start from a pixel and finds the end of a line of pixel in the direction specified
	:param image: image the sequence is created from
	:param direction: direction to go to find the end of line
	:param line: line index of the pixel to apply the function
	:param column: column index of the pixel to apply the function
	:param sequence: list of coordinates to append the end of line coordinates
	:return:
	"""

	distance = 0

	if direction == 0:
		while (line - distance) >= 0 and image[line - distance][column] == 2:
			image[line - distance][column] = 3
			distance += 1
		sequence.append(Coordinate(column, line - (distance - 1)))
		image[line - (distance-1)][column] = 2

	elif direction == 1:
		while (column + distance) < len(image[line]) and image[line][column + distance] == 2:
			image[line][column + distance] = 3
			distance += 1
		sequence.append(Coordinate(column + (distance - 1), line))
		image[line][column + (distance-1)] = 2

	elif direction == 2:
		while (line + distance) < len(image) and image[line + distance][column] == 2:
			image[line + distance][column] = 3
			distance += 1
		sequence.append(Coordinate(column, line + (distance - 1)))
		image[line + (distance-1)][column] = 2

	elif direction == 3:
		while (column - distance) >= 0 and image[line][column - distance] == 2:
			image[line][column - distance] = 3
			distance += 1
		sequence.append(Coordinate(column - (distance - 1), line))
		image[line][column - (distance-1)] = 2

	elif direction == -1:
		image[line][column] = 3

	return distance


def findDirection(image, line, column):
	"""
	Looks for a nearby pixel to choose a direction to start a line
	:param image: image the sequence is created from
	:param line: line index of the pixel to apply the function
	:param column: column index of the pixel to apply the function
	:return: direction of a nearby pixel, up = 0, right = 1, down = 2, left = 3, no pixel = -1. priorities is this order
	"""

	if line != 0:
		if image[line-1][column] == 2:
			return 0

	if column != (len(image[0]) - 1):
		if image[line][column+1] == 2:
			return 1

	if line != (len(image)-1):
		if image[line+1][column] == 2:
			return 2

	if column != 0:
		if image[line][column-1] == 2:
			return 3

	return -1


def createSequence(image):

	width = len(image[0])
	height = len(image)
	sequence = []

	for line in range(height):
		for column in range(width):

			if image[line][column] == 2:
				sequence.append(Coordinate(-1, -1))
				sequence.append(Coordinate(column, line))
				direction = 4
				while direction > -1:
					x, y = sequence[-1].getX(), sequence[-1].getY()
					direction = findDirection(image, y, x)
					findEndOfLine(image, direction, y, x, sequence)

	return sequence
