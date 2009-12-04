#!/usr/bin/env python

import Image
from optparse import OptionParser
from tempfile import mkdtemp
from sys import stdout
from os import path,popen

from life import *

def saveGrid2Img(grid,filename,scale,colored=False,colors="default",
                 bgcolor="default"): 
	"""saveGrid2Img(grid,filename,scale,colored=False,colors="default",
                 bgcolor="default")
- grid: 2 dimensional character array with ALIVE/DEAD states
- filename: string containing the full or relative path to the output file 
+-> usually a .gif file
- scale: the number of pixels per cell. 
+-> Intended for integer values
+-> 2 means each cell is 2x2 pixels
- colored: if true, cells will be coloured according to colors
+-> If False: alive=black, dead=white
- colors: a list of 9 RGB tuples representing the colors to be shown depending
on the number of living neigbours a live cell has
+-> Alternatively, the string "default" provides a default orange-red colour 
    scheme and "greyscale" provides a greyscale colour scheme
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
		bgcolor = (50,0,0)

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

def saveGrid2Anim(grid,generations,filename,scale,colored,colors,bgcolor,
                  verbose=True):
	"""saveGrid2Anim(grid,generations,filename,scale,colored,colors,bgcolor)
- grid: 2 dimensional character array with ALIVE/DEAD states
- generations: the number of generations to include in the gif animation
- filename: string containing the full or relative path to the output file 
+-> usually a .gif file
- scale: the number of pixels per cell. 
+-> Intended for integer values
+-> 2 means each cell is 2x2 pixels
- colored: if true, cells will be coloured according to colors
+-> If False: alive=black, dead=white
- colors: a list of 9 RGB tuples representing the colors to be shown depending
on the number of living neigbours a live cell has
+-> Alternatively, the string "default" provides a default orange-red colour 
    scheme and "greyscale" provides a greyscale colour scheme
- bgcolor: an RGB tuple containing the colour to be used for the background. 
+-> Ignored if colored = False
+-> "default" sets the background to dark red
+ verbose: print out each step as it's in progress

NOTE: Requires gifsicle <http://www.lcdf.org/gifsicle/>

Returns: None

"""
	tempdir = mkdtemp(prefix="lifetmp_")
	if (verbose):
		stdout.write("\rWriting generation 1/%d" % generations)
		stdout.flush()
	saveGrid2Img(grid,tempdir+("/gen%05d.gif" % 1),scale,colored,colors,bgcolor)
	for gen in range(2,generations+1):
		if (verbose):
			stdout.write("\rWriting generation %d/%d" % (gen,generations))
			stdout.flush()
		grid = nextGen(grid)
		saveGrid2Img(
			grid,
			tempdir+("/gen%05d.gif" % gen),
			scale,
			colored, colors, bgcolor
		)
	if (verbose):
		stdout.write("\n")
		stdout.write("Converting frames to animation...\n");
	popen("gifsicle --loop --delay=1 %s/%s.gif > %s" %
		(tempdir,"gen*",filename)
	)
	if (verbose):
		stdout.write("Deleting temporary files...")
	popen("rm -rf %s" % tempdir)
	if (verbose):
		stdout.write("Done.")

def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple 
From: <http://code.activestate.com/recipes/266466/>
		
"""
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)

def main():
	"""saveGrid2Img(grid,filename,scale,colored=False,colors="default",
                bgcolor="default")
	"""
	usage = "usage: %prog [options] outputfile.gif"
	parser = OptionParser(usage)
	parser.set_defaults(
		stdin = True,
		colored = False,
		scale = 1,
		verbose = True,
		generations = 1,
		filein = "",
		colors = "default",
		bgcolor = "default",
		liveChar = "@",
		deadChar = "."
	)
	parser.add_option(
		"-L", "--liveChar",
		type = "string",
		metavar = "LIVECHAR",
		dest = "liveChar",
		help = '''the character to represent a live cell in the input. Default
		is '@' '''
	)
	parser.add_option(
		"-D", "--deadChar",
		type = "string",
		metavar = "DEADCHAR",
		dest = "deadChar",
		help = '''the character to represent a dead cell in the input. Default
		is '.' '''
	)
	parser.add_option(
		"-i", "--stdin",
		action = "store_true",
		dest = "stdin",
		help = '''read cell data from standard input. Default if --filein flag
is not set used'''
	)
	parser.add_option(
		"-f", "--filein",
		dest = "filein",
		type = "string",
		metavar = "FILENAME",
		help = "read cell data from plaintext file"
	)
	parser.add_option(
		"-n", "--ngenerations",
		dest = "generations",
		type = "int",
		help = '''sets the number of generations to be displayed in the output
file. Defaults to 1'''
	)
	parser.add_option(
		"-c", "--colored",
		dest = "colored",
		action = "store_true",
		help = "make the output colored instead of just black and white"
	)
	parser.add_option(
		"-C", "--colorlist",
		type = "string",
		metavar = "C0 C1 C2 C3 C4 C5 C6 C7 C8",
		nargs = 9,
		dest = "colors",
		help = '''use the nine specified 24 bit hex encoded colors (e.g.
FF0000) for the colors of live cells in the animation. Cn corresponds 
to a live cell with n live neighbours'''
	)
	parser.add_option(
		"-b","--bgcolor",
		type = "string",
		metavar = "BGCOLOR",
		dest = "bgcolor",
		help = '''Hex encoded background color to use. Defaults to dark red,
ignored if --colored flag is not set'''
	)
	parser.add_option(
		"-s", "--scale",
		dest = "scale",
		type = "int",
		metavar = "CELLSIZE",
		help = '''the size of each cell in pixels. CELLSIZE = 2 will make
each cell 2x2 pixels'''
	)
	parser.add_option(
		"-q", "--quiet",
		dest = "verbose",
		action = "store_false",
		help = '''do not print anything to stdout'''
	)
	(options,args) = parser.parse_args()
	verbose = options.verbose
	if (len(args) < 1):
		parser.error("incorrect number of arguments")
	else:
		outfile = args[0]

	if (options.generations > 1 and outfile.lower().find("gif") == -1):
		parser.error("animations can only be output as animated GIFs")
	else:
		generations = options.generations

	scale = options.scale
	colored = options.colored
	if (options.colored and options.colors != 'default'):
		colors = [HTMLColorToRGB(c) for c in options.colors]
	else:
		colors = "default"
	if (options.colored and options.bgcolor != 'default'):
		bgcolor = HTMLColorToRGB(options.bgcolor)
	else:
		bgcolor = "default"
	
	if (options.filein != ""):
		options.stdin = False
		if (not path.exists(options.filein)):
			parser.error("specified file '%s' does not exist" % options.filein)
		else:
			filein = options.filein

	if (len(options.liveChar) != 1):
		stdout.write("LIVECHAR must be a single character.\n")
		exit()
	else:
		liveChar = options.liveChar

	if (len(options.deadChar) != 1):
		stdout.write("DEADCHAR must be a single character.\n")
		exit()
	else:
		deadChar = options.deadChar

	if (options.stdin):
		if (verbose):
			stdout.write('''Write the cell configuration below. Use only only
characters in the set (%c,%c) and the newline character. Each line
represents one row. Terminate input with an empty line. Ensure that
each row has the same number of characters\n''' % (liveChar,deadChar))

		gridstr = ""
		while(1):
			row = raw_input()
			if (len(row) == 0):	
				break
			gridstr += row + "\n"
		grid = str2grid(gridstr,liveChar,deadChar)
	else:
		grid = str2grid(open(filein).read(),liveChar,deadChar)

	if (generations == 1):
		saveGrid2Img(grid,outfile,scale,colored,colors,bgcolor)
	else:
		saveGrid2Anim(
			grid,generations,
			outfile,
			scale,
			colored,colors,bgcolor,
			verbose
		)


if __name__ == "__main__":
	main()
