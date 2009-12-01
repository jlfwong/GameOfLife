from random import randint
import Image

ALIVE = '@'
DEAD  = '.'

LIVECOND = [2,3]
BIRTHCOND = [3]

def numNeighbours(x,y,grid,wrap=True):
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
	temp = []
	for i in range(len(grid)):
		temp.append([])
		for j in range(len(grid[i])):
			temp[i].append(grid[i][j])
	return temp

def nextGen(grid):
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
	grid = []
	for i in range(rows):
		grid.append([])
		for j in range(columns):
			grid[i].append([ALIVE,DEAD][randint(0,1)])
	return grid

def str2grid(string, liveChar, deadChar):
	grid = string.split("\n");
	grid = filter(lambda x: len(x) > 0, grid)
	grid = map(lambda x: 
		list(x.replace(liveChar,ALIVE).replace(deadChar,DEAD)),
		grid
	)
	return grid	

def printGrid(grid):
	print "\n".join(map("".join,grid))

def saveGrid2Img(grid,filename,scale,colored=False,colors="default",bgcolor="default"): 
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
