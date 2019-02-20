def listToGCode(listIndex, pHeight, pWidth):
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
			gcodeCommand.append('G0 X' + str(coord.getX()*pWidth) + ' Y' + str(coord.getY()*pHeight))
			if toolUp:
				gcodeCommand.append('G0 Z3')
				toolUp = False
			
	# FOOTER
	gcodeCommand.append('\nG0 Z0')
	gcodeCommand.append('G28')
	
	return gcodeCommand