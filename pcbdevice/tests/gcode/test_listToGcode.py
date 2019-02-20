from unittest import TestCase

from pcbdevice.gcode.GcodeBuilder import listToGCode
from pcbdevice.models.Coordinates import Coordinate


class TestListToGCode(TestCase):
	def test_listToGCodeMultipleTrace(self):
		xSize, ySize = 2, 3
		
		coords = whenSingleTrace()
		self.assertEqual(listToGCode(coords, ySize, xSize), getExpected(coords, ySize, xSize))
		
		coords = whenTwoTrace()
		self.assertEqual(listToGCode(coords, ySize, xSize), getExpected(coords, ySize, xSize))
		
		coords = whenThreeTrace()
		self.assertEqual(listToGCode(coords, ySize, xSize), getExpected(coords, ySize, xSize))
	
	def test_listToGCodePixelSize(self):
		xSize, ySize = 1, 4
		coords = whenSingleTrace()
		self.assertEqual(listToGCode(coords, ySize, xSize), getExpected(coords, ySize, xSize))
		
		xSize, ySize = 4, 2
		coords = whenSingleTrace()
		self.assertEqual(listToGCode(coords, ySize, xSize), getExpected(coords, ySize, xSize))
		
		xSize, ySize = 8, -1
		coords = whenSingleTrace()
		self.assertRaises(RuntimeError, lambda: listToGCode(coords, ySize, xSize))


def getExpected(coords, ySize, xSize):
	header = ['G28', 'G90\n']
	footer = ['\nG0 Z0', 'G28']
	
	content = ['G0 X' + str(xSize * coords[0].getX()) + ' Y' + str(ySize * coords[0].getY()),
	           'G0 Z3',
	           ]
	
	for index, coord in enumerate(coords):
		if index > 0:
			if coord.getX() != -1 and coord.getY() != -1:
				content.append('G0 X' + str(xSize * coord.getX()) + ' Y' + str(ySize * coord.getY()))
				if coords[index - 1].getX() == -1 and coords[index - 1].getX() == -1:
					content.append('G0 Z3')
			else:
				content.append('G0 Z0')
	
	return header + content + footer


def whenSingleTrace():
	return [Coordinate(1, 2),
	        Coordinate(1, 5),
	        Coordinate(2, 5),
	        Coordinate(2, 8)]


def whenTwoTrace():
	return [Coordinate(1, 2),
	        Coordinate(1, 5),
	        Coordinate(5, 5),
	        Coordinate(5, 2),
	        Coordinate(1, 2),
	        Coordinate(-1, -1),
	        Coordinate(5, 4),
	        Coordinate(8, 4)]


def whenThreeTrace():
	return [Coordinate(1, 2),
	        Coordinate(1, 5),
	        Coordinate(5, 5),
	        Coordinate(5, 2),
	        Coordinate(1, 2),
	        Coordinate(-1, -1),
	        Coordinate(5, 4),
	        Coordinate(8, 4),
	        Coordinate(2, 9),
	        Coordinate(9, 45),
	        Coordinate(12, 12),
	        Coordinate(1, 10)]