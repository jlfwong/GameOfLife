"""
Conway's Game of Life in Python
Author: Jamie Wong - http://www.jamie-wong.com
Date: Nov 30 2009
"""
from random import randint
import Image

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
	""" numNeighbours(x,y,grid,wrap=True):
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
	""" gridCopy(grid):
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
	""" nextGen(grid):
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
	""" randGrid(rows,columns)
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
	""" str2grid(string, liveChar, deadChar)
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
	""" printGrid(grid)
	- grid: 2 dimensional character list

	Returns: None

	Prints the grid to the console

	"""
	print "\n".join(map("".join,grid))

def saveGrid2Img(grid,filename,scale,colored=False,colors="default",bgcolor="default"): 
	""" saveGrid2Img(grid,filename,scale,colored=False,colors="default",bgcolor="default")
	- grid: 2 dimensional character array with ALIVE/DEAD states
	- filename: string containing the full or relative path to the output file 
	+-> usually a .gif file
	- scale: the number of pixels per cell. 
	+-> Intended for integer values
	+-> 2 means each cell is 2x2 pixels
	- colored: if true, cells will be coloured according to colors
	-> If False: alive=black, dead=white
	- colors: a list of 9 RGB tuples representing the colors to be shown depending
		on the number of living neigbours a live cell has
	+-> Alternatively, the string "default" provides a default orange-red colour scheme
			and "greyscale" provides a greyscale colour scheme
	- bgcolor: an RGB tuple containing the colour to be used for the background. 
	+-> Ignored if colored = False
	+-> "default" sets the background to dark red

	Returns: None

	Saves the DEAD/ALIVE states stored in grid to a gif with customizable colour 
	scheme and scale

	"""
	if (colors == "default"):
		colors = [
			(100,0,0),
			(120,0,0),
			(140,0,0),
			(160,0,0),
			(180,0,0),
			(200,20,0),
			(220,40,0),
			(240,60,0),
			(255,80,0),
			(255,120,0)
		]
	if (colors == "greyscale"):
		colors = [
			(160,160,160),
			(140,140,140),
			(120,120,120),
			(100,100,100),
			(80,80,80),
			(60,60,60),
			(40,40,40),
			(20,20,20),
			(0,0,0)
		]
	if (bgcolor == "default"):
		bgcolor = (255,255,255)


	height = len(grid)
	width = len(grid[0])

	if (colored):
		im = Image.new("P",
			[width,height]
		)
		palette = []
		for bgcomp in bgcolor:
			palette.append(bgcomp)
		for col in colors:
			for comp in col:
				palette.append(comp)
		im.putpalette(palette)
	else:
		im = Image.new("1",
			[width,height],
			1
		)

	if (colored):
		for y in range(height):
			for x in range(width):
				num = numNeighbours(x,y,grid)
				if (grid[y][x] == ALIVE):
					im.putpixel((x,y),num+1)
				else:
					im.putpixel((x,y),0)
	else:
		for y in range(height):
			for x in range(width):
				num = numNeighbours(x,y,grid)
				if (grid[y][x] == ALIVE):
					im.putpixel((x,y),0)
	im = im.resize((width*scale,height*scale))
	im.save(filename)	
