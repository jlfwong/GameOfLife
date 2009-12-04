"""
Conway's Game of Life in Python
Author: Jamie Wong - http://www.jamie-wong.com
Creation Date: Nov 30 2009
"""
from random import randint

# These characters will represent dead and alive in the grids
ALIVE = '@'
DEAD  = '.'

# Conditions to stay alive and be born if dead respective
# If an alive element has n neighbours, where n is in LIVECOND, it stays alive
# If a dead element has n neighbours, where n is in BIRTHCOND, it is brought to life
# All other numbers of neighbours will result in a dead cell
LIVECOND = [2,3]
BIRTHCOND = [3]

def getExpansion(grid):
	"""getExpansion(grid):
- grid (2D list): holds the alive/dead state of cells

Return: A list of 4 elements specifying whether or not the grid needs to be
expanded to accomadate new births

The elements are in the order [left,right,top,bottom]
"""
	expand = [False,False,False,False]
	if (len(grid) == 0 or len(grid[0]) == 0):
		return expand
	
	height = len(grid)
	width = len(grid[0])

	for y in range(-1,height+1):
		if (BIRTHCOND.count(numNeighbours(-1,y,grid,False))):
			expand[0] = True
		if (BIRTHCOND.count(numNeighbours(width,y,grid,False))):
			expand[1] = True
	
	for x in range(-1,width+1):
		if (BIRTHCOND.count(numNeighbours(x,-1,grid,False))):
			expand[2] = True
		if (BIRTHCOND.count(numNeighbours(x,height,grid,False))):
			expand[3] = True
	
	return expand

def numNeighbours(x,y,grid,wrap=True):
	"""numNeighbours(x,y,grid,wrap=True):
- x (int): the x coordinate of the cell in question
- y (int): the y coordinate of the cell in question
- grid (2D List): holds the alive/dead state of cells
- wrap (bool): If true, will wrap around to check neighbours on the opposite edge

Returns: number of alive neighbours a cell at position (x,y) in the grid.
"""
	if (len(grid) == 0 or len(grid[0]) == 0):
		return 0
	num = 0 

	height = len(grid)
	width = len(grid[0])

	for dy in [-1,0,1]:
		ny = y + dy
        
		if (ny < 0 or ny >= height):
			if (wrap):
				ny = ny % height
			else:
				continue

		for dx in [-1,0,1]:
			if (dx == 0 and dy == 0):
				continue
			nx = x + dx

			if (nx < 0 or nx >= width): 
				if (wrap):
					nx = nx % width
				else:
					continue
			
			if (grid[ny][nx] == ALIVE): 
				num += 1
#	print "Cell at (%d,%d) has %d neighbours." % (x,y,num)
	return num

def gridCopy(grid):
	"""gridCopy(grid):
- grid (2D List): holds the alive/dead state of cells

Returns: a value (as opposed to reference) copy of the grid.
Used to prevent python's automatic use of pointers from interfering with nextGen

"""
	temp = []
	for i in range(len(grid)):
		temp.append([])
		for j in range(len(grid[i])):
			temp[i].append(grid[i][j])
	return temp

def nextGen(grid,autoExpand=False):
	"""nextGen(grid):
- grid (2D List): holds the alive/dead state of cells
- autoExpand (bool): if true, the grid will automatically expand to accomodate
  the birth of cells outside the boundary of the grid

Returns: the generation following the cells described in grid

"""
	if (len(grid) == 0 or len(grid[0]) == 0):
		return 0
	startGrid = gridCopy(grid)
	
	if (autoExpand):
		expand = getExpansion(startGrid)

		# Expand the left side
		if (expand[0]):
			startGrid = map(lambda x: [DEAD] + x,startGrid)

		# Expand the right side
		if (expand[1]):
			startGrid = map(lambda x: x + [DEAD],startGrid)

		width = len(startGrid[0])

		# Expand the top side
		if (expand[2]):
			startGrid = [[DEAD] * width] + startGrid

		# Expand the bottom
		if (expand[3]):
			startGrid = startGrid + [[DEAD] * width]
	
	height = len(startGrid)
	width = len(startGrid[0])

	endGrid = gridCopy(startGrid)

	for y in range(height):
		for x in range(width):
			num = numNeighbours(x,y,startGrid,not autoExpand)
			if (startGrid[y][x] == ALIVE and LIVECOND.count(num) == 0):
				endGrid[y][x] = DEAD
			elif (startGrid[y][x] == DEAD and BIRTHCOND.count(num)):
				endGrid[y][x] = ALIVE
	return endGrid

def randGrid(rows,columns):
	"""randGrid(rows,columns)
- rows (int): the number of rows in the generated grid
- columns (int): the number of columns in the generated grid

Returns: a 2D list with randomized alive/dead cells

"""
	grid = []
	for i in range(rows):
		grid.append([])
		for j in range(columns):
			grid[i].append([ALIVE,DEAD][randint(0,1)])
	return grid

def str2grid(str, liveChar=ALIVE, deadChar=DEAD):
	"""str2grid(str, liveChar, deadChar)
- str (string): the input string with newlines to convert to a grid
- liveChar (char): the character representing an alive cell in string
- deadChar (char): the character representing a dead cell in string

Returns: a grid corresponding to the provided input string

"""
	grid = str.split("\n");
	grid = filter(lambda x: len(x) > 0, grid)
	grid = map(lambda x: 
		list(x.replace(liveChar,ALIVE).replace(deadChar,DEAD)),
		grid
	)
	return grid	

def printGrid(grid):
	"""printGrid(grid)
- grid (2D list): holds the alive/dead state of cells

Returns: None

Prints the grid to the console

"""
	print "\n".join(map("".join,grid))
