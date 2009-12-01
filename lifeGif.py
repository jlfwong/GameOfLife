from life import *
import Image

default_colors = [
	(50,0,0),
	(70,0,0),
	(120,0,0),
	(150,100,0),
	(150,100,0),
	(150,150,0),
	(180,180,0),
	(220,220,0),
	(255,255,0)
]

def saveGrid2Img(grid,filename,scale=1,colored=False,colors=default_colors): 
	height = len(grid)
	width = len(grid[0])
	
	im = Image.new("RGB",
		[width,height]
	)

	if (colored):
		for i in range(height):
			for j in range(width):
				num = numNeighbours(j,i,grid)
				im.putpixel((i,j),colors[num])
	else:
		for i in range(height):
			for j in range(width):
				num = numNeighbours(j,i,grid)
				im.putpixel((i,j),[(0,0,0),(255,255,255)][grid[i][j] == ALIVE])
	im = im.resize((width*scale,height*scale))
	im.save(filename)
