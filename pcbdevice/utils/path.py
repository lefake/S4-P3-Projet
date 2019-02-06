def scanHorizontal(image, rTool):
	"""
	:param image: image to apply the scan
	:param rTool: tool radius
	:return: adds 2's where there should be a path for the tool, looking at the image only horizontally
	"""

	width = len(image[0])
	height = len(image)

	for line in range(height):
		for column in range(width):

			if image[line][column] == 1 and image[line][column - 1] != 1:
				for px in range(2 * rTool + 1):
					if image[line - rTool + px][column - rTool] == 0:
						image[line - rTool + px][column - rTool] = 2

			if image[line][column] == 1 and image[line][column + 1] != 1:
				for px in range(2 * rTool + 1):
					if image[line - rTool + px][column + rTool] == 0:
						image[line - rTool + px][column + rTool] = 2

	return image


def scanVertical(image, rTool):
	"""
	:param image: image to apply the scan
	:param rTool: tool radius
	:return: adds 2's where there should be a path for the tool, looking at the image only vertically
	"""

	width = len(image[0])
	height = len(image)

	for line in range(height):
		for column in range(width):

			if image[line][column] == 1 and image[line - 1][column] != 1:
				for px in range(2 * rTool + 1):
					if image[line - rTool][column - rTool + px] == 0:
						image[line - rTool][column - rTool + px] = 2

			if image[line][column] == 1 and image[line + 1][column] != 1:
				for px in range(2 * rTool + 1):
					if image[line + rTool][column - rTool + px] == 0:
						image[line + rTool][column - rTool + px] = 2

	return image

def twoRemoving(image, rTool):
	"""
	:param image: image to apply the scan
	:param rTool: tool radius
	:return: removes unnecessary twos to leave a path of only one pixel large
	"""

	width = len(image[0])
	height = len(image)

	for line in range(height):
		for column in range(width):

			if image[line][column] == 1:
				for px in range(1, 2 * rTool):
					for pixel in range(1, 2*rTool):
						if image[line - rTool + px][column - rTool + pixel] == 2:
							image[line - rTool + px][column - rTool + pixel] = 0

	print("image width = " + str(width))
	print("image height = " + str(height))

	return image


def path(image, rTool):
	return twoRemoving(scanVertical(scanHorizontal(image, rTool), rTool), rTool)


