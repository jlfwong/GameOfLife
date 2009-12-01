"""
Conway's Game of Life in Python
Author: Jamie Wong - http://www.jamie-wong.com
Date: Nov 30 2009
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

def numNeighbours(x,y,grid,wrap=True):
	"""numNeighbours(x,y,grid,wrap=True):
- x: the x coordinate of the cell in question
- y: the y coordinate of the cell in question
- grid: The 2 dimensional character array containing the ALIVE/DEAD states of the cells
- wrap: If true, this function will wrap around to check neighbours on the opposite edge

Returns: number of alive neighbours a cell at position (x,y) in the provided grid has.
"""
	num = 0 
	for dy in [-1,0,1]:
		ny = y + dy
        
		if (ny < 0 or ny >= len(grid)):
			if (wrap):
				ny = ny % len(grid)
			else:
				continue

		for dx in [-1,0,1]:
			if (dx == 0 and dy == 0):
				continue
			nx = x + dx

			if (nx < 0 or nx >= len(grid[ny])): 
				if (wrap):
					nx = nx % len(grid[ny])
				else:
					continue
			
			if (grid[ny][nx] == ALIVE): 
				num += 1
	return num

def gridCopy(grid):
	"""gridCopy(grid):
- grid: the 2 dimensional character array to make a copy of

Returns: a value (as opposed to reference) copy of the grid.
This is used to prevent python's automatic use of pointers from interfering with nextGen

"""
	temp = []
	for i in range(len(grid)):
		temp.append([])
		for j in range(len(grid[i])):
			temp[i].append(grid[i][j])
	return temp

def nextGen(grid):
	"""nextGen(grid):
- grid: the 2 dimensional character array to process

Returns: the generation following the cells described in grid

"""
	newgrid = gridCopy(grid)
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			num = numNeighbours(j,i,grid)
			if (grid[i][j] == ALIVE and LIVECOND.count(num) == 0):
				newgrid[i][j] = DEAD
			elif (grid[i][j] == DEAD and BIRTHCOND.count(num)):
				newgrid[i][j] = ALIVE
	return gridCopy(newgrid)

def randGrid(rows,columns):
	"""randGrid(rows,columns)
- rows: the number of rows in the generated grid
- columns: the number of columns in the generated grid

Returns: a randomized ALIVE/DEAD grid

"""
	grid = []
	for i in range(rows):
		grid.append([])
		for j in range(columns):
			grid[i].append([ALIVE,DEAD][randint(0,1)])
	return grid

def str2grid(string, liveChar, deadChar):
	"""str2grid(string, liveChar, deadChar)
- string: the input string with newlines to convert to a grid
- liveChar: the character representing an alive cell in string
- deadChar: the character representing a dead cell in string

Returns: a grid correspoding to the provided input string

"""
	grid = string.split("\n");
	grid = filter(lambda x: len(x) > 0, grid)
	grid = map(lambda x: 
		list(x.replace(liveChar,ALIVE).replace(deadChar,DEAD)),
		grid
	)
	return grid	

def printGrid(grid):
	"""printGrid(grid)
- grid: 2 dimensional character list

Returns: None

Prints the grid to the console

"""
	print "\n".join(map("".join,grid))
