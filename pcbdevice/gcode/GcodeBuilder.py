def listToGCode(listIndex, pHeight, pWidth):
	"""
	Convert a list of matrix coordinate in a list of GCode commands
	
	:param listIndex: List of coordinate
	:param pHeight: Pixel height in mm
	:param pWidth: Pixel width in mm
	:return: List of all the GCode commands
	"""
	gcodeCommand = []
	toolUp = True
	
	if pHeight <= 0 or pWidth <= 0:
		raise RuntimeError('Pixel dimension error')
	
	# HEADER
	gcodeCommand.append('G28')
	gcodeCommand.append('G90\n')
	
	for coord in listIndex:
		if coord.getX() == -1 and coord.getY() == -1:
			gcodeCommand.append('G0 Z0')
			toolUp = True
		else:
			gcodeCommand.append('G0 X' + str(round(coord.getX()*pWidth, 2)) + ' Y' + str(round(coord.getY()*pHeight, 2)))
			if toolUp:
				gcodeCommand.append('G0 Z3')
				toolUp = False
			
	# FOOTER
	gcodeCommand.append('\nG0 Z0')
	gcodeCommand.append('G28')
	
	return gcodeCommand