from unittest import TestCase

from pcbdevice.utils import TestUtils
from pcbdevice.utils.FileUtils import FileUtils

resources = './pcbdevice/tests/resources/'

class TestFileUtils(TestCase):
	def test_pbmToMatrix(self):
		actual, h, w = FileUtils.pbmToMatrix(resources + 'raw/test1.pbm')
		expected = TestUtils.readIntFile(resources + 'formatted/test1.csv')
		assert actual == expected
	
	def test_saveMatrixToFile(self):
		actual, h, w = FileUtils.pbmToMatrix(resources + 'raw/test1.pbm')
		FileUtils.saveMatrixToFile(actual, resources + 'output/test1.csv')
		expected = TestUtils.readIntFile(resources + 'output/test1.csv')
		assert actual == expected
		
	def test_getPixelSize(self):
		assert 10, 10 == FileUtils.getPixelSize(10, 10, 100, 100)
		assert 1, 1 == FileUtils.getPixelSize(100, 100, 100, 100)
		assert 10, 10 == FileUtils.getPixelSize(10, 10, 10, 10, unit = 'cm')
		assert 10, 10 == FileUtils.getPixelSize(10, 10, 1, 1, unit = 'm')
		assert 254, 254 == FileUtils.getPixelSize(10, 10, 10, 10, unit = 'in')
		assert 10, 5 == FileUtils.getPixelSize(10, 10, 10, 20)