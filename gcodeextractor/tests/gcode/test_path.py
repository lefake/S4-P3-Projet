from unittest import TestCase

from gcodeextractor.gcode.path import scanHorizontal, scanVertical, twoRemoving


class TestPath(TestCase):

	#inputs
	def imageTest(self):
		return [[0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 1, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0]]

	def imageTestMulti(self):
		return [[0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 1, 0, 0, 1, 0, 0],
		        [0, 0, 0, 1, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 1, 0, 0]]

	def imageTestHOut(self):
		return [[0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 1, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0]]

	def imageTestVOut(self):
		return [[0, 0, 0],
		        [0, 0, 0],
		        [0, 0, 0],
		        [0, 1, 0],
		        [0, 0, 0],
		        [0, 0, 0],
		        [0, 0, 0]]

	def imageTest2(self):
		return [[0, 0, 0, 0, 0, 0, 0],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 2, 2, 1, 2, 2, 0],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 0, 0, 0, 0, 0, 0]]

	def imageTestMulti2(self):
		return [[2, 2, 2, 2, 2, 2, 2],
		        [2, 2, 2, 2, 2, 2, 2],
		        [2, 1, 2, 2, 1, 2, 2],
		        [2, 2, 2, 1, 2, 2, 2],
		        [2, 2, 2, 2, 2, 2, 2],
		        [2, 2, 2, 2, 2, 2, 2],
		        [2, 2, 2, 2, 1, 2, 2]]


	#horizontal results
	def imageResultHr2(self):
		return [[0, 0, 0, 0, 0, 0, 0],
		        [0, 2, 0, 0, 0, 2, 0],
		        [0, 2, 0, 0, 0, 2, 0],
		        [0, 2, 0, 1, 0, 2, 0],
		        [0, 2, 0, 0, 0, 2, 0],
		        [0, 2, 0, 0, 0, 2, 0],
		        [0, 0, 0, 0, 0, 0, 0]]

	def imageResultHr3(self):
		return [[2, 0, 0, 0, 0, 0, 2],
		        [2, 0, 0, 0, 0, 0, 2],
		        [2, 0, 0, 0, 0, 0, 2],
		        [2, 0, 0, 1, 0, 0, 2],
		        [2, 0, 0, 0, 0, 0, 2],
		        [2, 0, 0, 0, 0, 0, 2],
		        [2, 0, 0, 0, 0, 0, 2]]

	def imageResultHOut(self):
		return [[0, 2, 0, 0, 0, 2, 0],
		        [0, 2, 0, 1, 0, 2, 0],
		        [0, 2, 0, 0, 0, 2, 0]]

	def imageResultMultiH(self):
		return [[0, 0, 2, 2, 0, 0, 2],
		        [0, 2, 2, 2, 0, 2, 2],
		        [0, 1, 2, 2, 1, 2, 2],
		        [0, 2, 2, 1, 0, 2, 2],
		        [0, 2, 2, 2, 0, 2, 2],
		        [0, 2, 2, 0, 0, 2, 2],
		        [0, 0, 2, 0, 1, 0, 2]]


	#vertical results
	def imageResultVr2(self):
		return [[0, 0, 0, 0, 0, 0, 0],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 1, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 0, 0, 0, 0, 0, 0]]

	def imageResultVr3(self):
		return [[2, 2, 2, 2, 2, 2, 2],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 1, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0],
		        [2, 2, 2, 2, 2, 2, 2]]

	def imageResultVOut(self):
		return [[0, 0, 0],
		        [2, 2, 2],
		        [0, 0, 0],
		        [0, 1, 0],
		        [0, 0, 0],
		        [2, 2, 2],
		        [0, 0, 0]]

	def imageResultMultiV(self):
		return [[2, 2, 2, 2, 2, 2, 2],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 1, 0, 0, 1, 0, 0],
		        [0, 0, 0, 1, 0, 0, 0],
		        [2, 2, 2, 2, 2, 2, 2],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 0, 0, 0, 1, 0, 0]]

	#two results

	def imageResult2(self):
		return [[0, 0, 0, 0, 0, 0, 0],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 2, 0, 0, 0, 2, 0],
		        [0, 2, 0, 1, 0, 2, 0],
		        [0, 2, 0, 0, 0, 2, 0],
		        [0, 2, 2, 2, 2, 2, 0],
		        [0, 0, 0, 0, 0, 0, 0]]

	def imageResultMulti2(self):
		return [[2, 2, 2, 2, 2, 2, 2],
		        [0, 0, 0, 0, 0, 0, 2],
		        [0, 1, 0, 0, 1, 0, 2],
		        [0, 0, 0, 1, 0, 0, 2],
		        [2, 2, 0, 0, 0, 2, 2],
		        [2, 2, 2, 0, 0, 0, 2],
		        [2, 2, 2, 0, 1, 0, 2]]



	def test_hori(self):

		self.assertEqual(scanHorizontal(self.imageTest(), 2), self.imageResultHr2())
		self.assertEqual(scanHorizontal(self.imageTest(), 3), self.imageResultHr3())
		self.assertEqual(scanHorizontal(self.imageTestHOut(), 2), self.imageResultHOut())
		self.assertEqual(scanHorizontal(self.imageTest(), 4), self.imageTest())
		self.assertEqual(scanHorizontal(self.imageTestMulti(), 2), self.imageResultMultiH())

	def test_vert(self):

		self.assertEqual(scanVertical(self.imageTest(), 2), self.imageResultVr2())
		self.assertEqual(scanVertical(self.imageTest(), 3), self.imageResultVr3())
		self.assertEqual(scanVertical(self.imageTestVOut(), 2), self.imageResultVOut())
		self.assertEqual(scanVertical(self.imageTest(), 4), self.imageTest())
		self.assertEqual(scanVertical(self.imageTestMulti(), 2), self.imageResultMultiV())

	def test_two(self):

		self.assertEqual(twoRemoving(self.imageTest2(), 2), self.imageResult2())
		self.assertEqual(twoRemoving(self.imageTest2(), 3), self.imageTest())
		self.assertEqual(twoRemoving(self.imageTest2(), 7), self.imageTest())
		self.assertEqual(twoRemoving(self.imageTestMulti2(), 2), self.imageResultMulti2())
