from unittest import TestCase

from pcbdevice.utils import TestUtils
from pcbdevice.utils.FileUtils import FileUtils

resources = './pcbdevice/tests/resources/'

class TestFileUtils(TestCase):
	def test_pbmToCsv(self):
		actual = FileUtils.pbmToCsv(resources + 'raw/test1.pbm')
		expected = TestUtils.readIntFile(resources + 'formatted/test1.csv')
		assert actual == expected
	
	def test_saveMatrixToFile(self):
		actual = FileUtils.pbmToCsv(resources + 'raw/test1.pbm')
		FileUtils.saveMatrixToFile(actual, resources + 'output/test1.csv')
		expected = TestUtils.readIntFile(resources + 'output/test1.csv')
		assert actual == expected
