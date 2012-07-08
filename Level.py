import TerrainClass
import TerrainManager

from panda3d.core import PandaNode, NodePath
from math import sqrt

class Level ( object ):
	def __init__(self, levelFile ):
		'''load the levelFile'''
		'''class variables'''
		self.terrainMgr = TerrainManager.TerrainManager()
		self.modelList = []
		self.levelRoot=None

		try:
			'''test for file'''
			temp = levelFile.readline
			del temp
		except:
			'''level file is a string'''
			self.levelFile = open( levelFile )

		self.readFile()
		temp = 16
		self.levelRoot.setScale( (temp,temp,temp) )
		del temp

	def getRoot(self):
		return self.levelRoot


	def nextNonComment(self, levelFile ):
		line = "#"
		while line[0] is '#' or line[0] is '\n' :
			line = levelFile.readline()
			line = line.strip()
			if len ( line ) is 0:
				return line

		return line

	def parseNumMapTiles(self,line):
		where = line.find("mapTiles=")
		if where is -1:
			return -1

		return int (line[where+len("mapTiles="):] )

	def parseNumModels( self,line ):
		partList = line.partition( "=")
		if partList[2] is "":
			string = "parsing error on line expected model=x recieved : "+line
			raise Exception(string )
		else :
			return int ( partList[2] )


	def parseModelLine( self,line ):
		'''take a line as input and output a dictionary
		containing all the models data as output'''
		toRet = {}
		split = line.split()
		for part  in split  :
			pieces = part.partition('=')
			toRet[pieces[0]] = pieces[2]

		if __debug__ is True or True:
			listing = toRet.keys()
			listing.sort()
			expected = ['h','model','p','x','y','r','z','sx','sy','sz']
			expected.sort()

			if str(listing) is str(expected) :
				print "bad keys in level file's model listing"
				print "   expected:",expected
				print "   recieved:",listing

		return toRet




	def readFile(self):
		self.terrainList = []
		'''get version of encoding'''
		line = self.nextNonComment( self.levelFile )
		if line !=  "version=0.01" :
			print "Level.py: Level.readFile(): bad version on",self.levelFile

		'''get number of mapTiles'''
		line = self.nextNonComment( self.levelFile)
		numMapTiles = self.parseNumMapTiles(line)

		'''make sure we can make a square out of the images'''
		if numMapTiles is not int( sqrt( numMapTiles) )**2:
			raise Exception( " can't make level with non square image set" )

		for i in xrange( numMapTiles ):
			line = self.nextNonComment( self.levelFile )
			parts = line.split() # split the line on the space if any
			'''first part is the height map, second is the texture(if there)'''
			heightMapName=parts[0]
			textureName=parts[0]
			if len( parts) == 2 :
				textureName=parts[1]
			elif len(parts)>2:
				raise Exception("Error, to many parts in: "+line) 

			self.terrainMgr.newTerrainPart( heightMapName, textureName )


			base.taskMgr.add( self.terrainMgr.update,"1" )
			'''base.taskMgr.add( self.terrainList[i].asyncUpdate,
					str(self.terrainList[i] ))i'''

		'''make our root the terrainMgr root'''
		self.levelRoot = self.terrainMgr.getRoot()

		'''read in the models and their locations'''
		numModels = self.parseNumModels( self.nextNonComment( self.levelFile ) )

		for item in xrange(numModels):
			line = self.nextNonComment( self.levelFile )
			specs = self.parseModelLine( line )
			node = loader.loadModel(specs["model"] )
			node.reparentTo( self.levelRoot )
			node.setX( float( specs["x"] ) )
			node.setY( float( specs["y"] ) )
			node.setZ( float( specs["z"] ) )
			node.setH( float( specs["h"] ) )
			node.setR( float( specs["r"] ) )
			node.setP( float( specs["p"] ) )
			node.setSx( float (specs["sx"] ))
			node.setSy( float (specs["sy"] ))
			node.setSz( float (specs["sz"] ))
			self.modelList.append( item  )

		self.levelFile.close()
		print "levelLoaded"
		return # finished loading the level
