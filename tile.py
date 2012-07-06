#!/usr/bin/python

'''read in a file specified on the command line and split it into parts
	args:
		args[1]=filename
		args[2]=size ( will be square tiles )
		args[3]=outFilePrefix ( will be numbered after the prefix )
'''

from png_ import png
import argparse

class Namer (object):
	def __init__(self, startName ):
		self.prefix=str(startName)
		self.counter=0
		return

	def getNext(self):
		self.counter+=1
		return self.prefix+str(self.counter-1)+".png"

def doIt(outSize =64, inImageName=None, prefix=None, bitDepth=8 ):

	inImage = png.Reader(inImageName)

	inImageRead = inImage.asFloat()
	inPixels = inImageRead[2]

	inSize = inImageRead[0]

	rowBuffer = []
	k=0

	namer = Namer(prefix)

	for line in inPixels:
		rowBuffer.append( line )
		if len( rowBuffer ) == outSize :
			'''time to write the sub images'''
			writeImageRow( size=outSize,
					namer=namer,
					bitDepth=8 ,
					inPixels=rowBuffer)
			rowBuffer=[]

def writeImageRow( size, namer, bitDepth, inPixels):
	length = len( inPixels[0] )
	numImages = length/size


	out = png.Writer( size,size, greyscale=True,
				bitdepth=bitDepth)

	for i in range( numImages ):
		outPixels=[]
		for y in range( size ):
			outPixels.append( inPixels[y][i*size:(i+1)*size] )

		outFile = open( namer.getNext() ,"wb")
		out.write( outFile,outPixels )
		outFile.close()



def setUpArgParser(parser):
	parser.add_argument('-f',help="the input file containing the png") 
	parser.add_argument('-s',help="the size in pixels of the output files")
	parser.add_argument('-o',help="prefix that the generated files will have")
	parser.add_argument('-b',help="bitdepth of generated image, defaults to 8")


oFile = None
iFile = None
size  = None 
bitDepth=8
parser = argparse.ArgumentParser(
		description="take a large png and break it up into smaller pieces"
		)

setUpArgParser(parser)
args = parser.parse_args()
if args.o != None:
	oFile = args.o
if args.f != None:
	iFile = args.f
if args.s != None:
	size = int ( args.s )
if args.b != None:
	bitDepth= int( args.b )

badArg = False
while oFile == None:
	print "OutputFile prefix: "
	oFile = raw_input()
while iFile == None:
	print "InputFile: "
	iFile = raw_input()
while size == None:
	print "size in pixels for output files"
	size = int(raw_input())


if not badArg:
	#print "size: ",size
	#print "oFile: ", oFile
	#print "iFile: ", iFile
	doIt( size, iFile, oFile, bitDepth)
else:
	print "see help for usage (-h)"













