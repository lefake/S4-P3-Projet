class Coordinate:
	_x = -1
	_y = -1
	
	def __init__(self, x = -1, y = -1):
		self._x = x
		self._y = y
	
	def setX(self, x):
		self._x = x
		
	def setY(self, y):
		self._y = y
		
	def getX(self):
		return self._x
	
	def getY(self):
		return self._y