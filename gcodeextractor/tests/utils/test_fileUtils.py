from unittest import TestCase

from gcodeextractor.utils import TestUtils
from gcodeextractor.utils.FileUtils import FileUtils
from gcodeextractor.utils.TestUtils import readStringFile

resources = './gcodeextractor/tests/resources/'

class TestFileUtils(TestCase):
	def test_pbmToMatrix(self):
		actual, h, w = FileUtils.pbmToMatrix(resources + 'raw/test1.pbm')
		expected = TestUtils.readIntFile(resources + 'formatted/test1.csv')
		self.assertEqual(actual, expected)
	
	def test_saveMatrixToFile(self):
		actual, h, w = FileUtils.pbmToMatrix(resources + 'raw/test1.pbm')
		FileUtils.saveMatrixToFile(actual, resources + 'output/test1.csv')
		expected = TestUtils.readIntFile(resources + 'output/test1.csv')
		self.assertEqual(actual, expected)
		
	def test_saveStringListToFile(self):
		stringList = ['This',
		             'is',
		              'a\n',
		              'test']
		
		FileUtils.saveStringListToFile(stringList, resources + 'output/text1.txt')
		self.assertEqual(readStringFile(resources + 'output/text1.txt'), readStringFile(resources+'expected/text1.txt'))
		
		stringList = ['G28',
		              'G90',
		              'G0 Z3\n',
		              'G0 X15 Y45']
		
		FileUtils.saveStringListToFile(stringList, resources + 'output/text2.txt')
		self.assertEqual(readStringFile(resources + 'output/text2.txt'), readStringFile(resources + 'expected/text2.txt'))
		
	def test_getPixelSize(self):
		self.assertEqual((10, 10), FileUtils.getPixelSize(10, 10, 100, 100))
		self.assertEqual((1, 1), FileUtils.getPixelSize(100, 100, 100, 100))
		self.assertEqual((10, 10), FileUtils.getPixelSize(10, 10, 10, 10, unit = 'cm'))
		self.assertEqual((25.4, 25.4), FileUtils.getPixelSize(10, 10, 10, 10, unit = 'in'))
		self.assertEqual((1, 2), FileUtils.getPixelSize(10, 10, 10, 20))
		self.assertRaises(RuntimeError, lambda: FileUtils.getPixelSize(10, 10, 10, 10, 'ft'))