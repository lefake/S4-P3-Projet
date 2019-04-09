from unittest import TestCase

from gcodeextractor.gcode.GcodeBuilder import listToGCode
from gcodeextractor.utils.Coordinates import Coordinate


class TestListToGCode(TestCase):
	
	oneTrace = [Coordinate(1, 2),
	        Coordinate(1, 5),
	        Coordinate(2, 5),
	        Coordinate(2, 8)]
	
	twoTrace = [Coordinate(1, 2),
	        Coordinate(1, 5),
	        Coordinate(5, 5),
	        Coordinate(5, 2),
	        Coordinate(1, 2),
	        Coordinate(-1, -1),
	        Coordinate(5, 4),
	        Coordinate(8, 4)]
	
	threeTrace = [Coordinate(1, 2),
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
	
	def test_listToGCodeMultipleTrace(self):
		xSize, ySize = 2.0, 3.0
		
		self.assertEqual(listToGCode(self.oneTrace, ySize, xSize), getExpected(self.oneTrace, ySize, xSize))
		self.assertEqual(listToGCode(self.twoTrace, ySize, xSize), getExpected(self.twoTrace, ySize, xSize))
		self.assertEqual(listToGCode(self.threeTrace, ySize, xSize), getExpected(self.threeTrace, ySize, xSize))
	
	def test_listToGCodePixelSize(self):
		xSize, ySize = 1.0, 4.0
		self.assertEqual(listToGCode(self.oneTrace, ySize, xSize), getExpected(self.oneTrace, ySize, xSize))
		
		xSize, ySize = 4.0, 2.0
		self.assertEqual(listToGCode(self.oneTrace, ySize, xSize), getExpected(self.oneTrace, ySize, xSize))
		
		xSize, ySize = 8.0, -1.0
		self.assertRaises(RuntimeError, lambda: listToGCode(self.oneTrace, ySize, xSize))

def getExpected(coords, ySize, xSize):
	header = ['G28', 'G90\n']
	footer = ['\nG0 Z0', 'G28', 'M18']
	
	content = ['G0 X' + str(round(xSize * coords[0].getX(), 2)) + ' Y' + str(round(ySize * coords[0].getY(), 2)),
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