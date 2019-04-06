from unittest import TestCase

from gcodeextractor.gcode.GcodeCreator import createSequence, findDirection, findEndOfLine
from gcodeextractor.models.Coordinates import Coordinate


class TestGcodeCreator(TestCase):


	def imageTest(self):
		return [[0, 2, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 2, 2, 0],
            [0, 2, 2, 0, 0, 2, 0],
            [0, 0, 2, 0, 0, 2, 0],
            [0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]

	expectedSequence = [Coordinate(-1, -1),
	                    Coordinate(1, 0),
	                    Coordinate(1, 3),
	                    Coordinate(2, 3),
	                    Coordinate(2, 5),
	                    Coordinate(-1, -1),
	                    Coordinate(4, 2),
	                    Coordinate(5, 2),
	                    Coordinate(5, 4)]

	def imageTestDots(self):
		return [[0, 0, 0, 2],
	          [0, 2, 0, 0],
	          [0, 0, 0, 0],
	          [0, 0, 2, 0]]

	expectedSequenceDots = [Coordinate(-1, -1),
	                        Coordinate(3, 0),
	                        Coordinate(-1, -1),
	                        Coordinate(1, 1),
	                        Coordinate(-1, -1),
	                        Coordinate(2, 3)]

	def imageTestEmpty(self):
		return [[0, 0, 0, 0],
	          [0, 0, 0, 0],
	          [0, 0, 0, 0],
	          [0, 0, 0, 0]]

	expectedSequenceEmpty = []

	def imageTestFull(self):
		return [[2, 2, 2, 2],
		        [2, 2, 2, 2],
		        [2, 2, 2, 2],
		        [2, 2, 2, 2]]

	expectedSequenceFull = [Coordinate(-1, -1),
	                        Coordinate(0, 0),
	                        Coordinate(3, 0),
	                        Coordinate(3, 3),
	                        Coordinate(0, 3),
	                        Coordinate(0, 1),
	                        Coordinate(2, 1),
	                        Coordinate(2, 2),
	                        Coordinate(1, 2)]


	def test_createSequence(self):

		self.assertEqual(createSequence(self.imageTest()), self.expectedSequence)
		self.assertEqual(createSequence(self.imageTestDots()), self.expectedSequenceDots)
		self.assertEqual(createSequence(self.imageTestEmpty()), self.expectedSequenceEmpty)
		self.assertEqual(createSequence(self.imageTestFull()), self.expectedSequenceFull)

	def test_findDirection(self):

		self.assertEqual(findDirection(self.imageTest(), 1, 1), 0)
		self.assertEqual(findDirection(self.imageTest(), 2, 4), 1)
		self.assertEqual(findDirection(self.imageTest(), 1, 4), 2)
		self.assertEqual(findDirection(self.imageTest(), 3, 3), 3)
		self.assertEqual(findDirection(self.imageTest(), 5, 4), -1)

	def test_findEndOfLine(self):

		sequenceTest = []

		self.assertEqual(findEndOfLine(self.imageTest(), 2, 0, 1, sequenceTest), 4)
		self.assertEqual(findEndOfLine(self.imageTest(), 1, 3, 1, sequenceTest), 2)
		self.assertEqual(findEndOfLine(self.imageTest(), 0, 5, 2, sequenceTest), 3)
		self.assertEqual(findEndOfLine(self.imageTest(), 3, 0, 1, sequenceTest), 1)
		self.assertEqual(findEndOfLine(self.imageTestFull(), 1, 1, 1, sequenceTest), 3)
		self.assertEqual(findEndOfLine(self.imageTestFull(), 0, 1, 1, sequenceTest), 2)


