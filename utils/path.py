def scanHorizontal(image, rTool):

	width = len(image[0])
	height = len(image)

	for line in range(height):
		for column in range(width):

			if image[line][column] == 1 and image[line][ column - 1] == 0:
				for px in range(2 * rTool):
					if image[line - rTool + px][column - rTool] == 0:
						image[line - rTool + px][column - rTool] = 2

			if image[line][column] == 1 and image[line][ column + 1] == 0:
				for px in range(2 * rTool):
					if image[line - rTool + px][column + rTool] == 0:
						image[line - rTool + px][column + rTool] = 2

	return image


def scanVertical(image, rTool):

	width = len(image[0])
	height = len(image)

	for line in range(height):
		for column in range(width):

			if image[line][column] == 1 and image[line - 1][ column] == 0:
				for px in range(2 * rTool):
					if image[line - rTool][column - rTool + px] == 0:
						image[line - rTool][column - rTool + px] = 2

			elif image[line][column] == 1 and image[line + 1][column] == 0:
				for px in range(2 * rTool):
					if image[line + rTool][column - rTool + px] == 0:
						image[line + rTool][column - rTool + px] = 2

	return image

def twoRemoving(image, rTool):

	rTool -= 1
	width = len(image[0])
	height = len(image)

	for line in range(height):
		for column in range(width):

			if image[line][column] == 1:
				for px in range(2 * rTool + 1):
					if image[line - rTool + px][column] == 2:
						image[line - rTool + px][column] = 0
					if image[line][column - rTool + px] == 2:
						image[line][column - rTool + px] = 0

	return image

