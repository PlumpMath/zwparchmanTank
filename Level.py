import TerrainClass
import TerrainManager

class Level ( object ):
	def __init__(self, levelFile ):
		'''load the levelFile'''
		'''class variables'''
		self.terrainList=[]
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
		scaleTemp = 32
		self.levelRoot.setScale( (scaleTemp,scaleTemp,scalTemp))
		del scaleTemp

	def getRoot(self):
		return self.levelRoot

	def readFile(self):
		def nextNonComment( levelFile ):
			line = "#"
			while line[0] is '#' or line[0] is '\n' :
				line = levelFile.readline()
				line = line.strip()
				if len ( line ) is 0:
					return line

			return line

		def parseNumMapTiles(line):
			where = line.find("mapTiles=")
			if where is -1:
				return -1

			return int (line[where+len("mapTiles="):] )

		def parseNumModels( line ):
			partList = line.partition( "=")
			if partList[2] is "":
				return -1
			else :
				return int ( partList[2] )

		def parseModelLine( line ):
			'''take a line as input and output a dictionary
			containing all the models data as output'''
			toRet = {}
			split = line.split()
			for part  in split  :
				pieces = part.partition('=')
				toRet[pieces[0]] = pieces[2]

			if __debug__ is True:
				listing = toRet.keys()
				listing.sort()
				expected = ['h','model','p','x','y','z','sx','sy','sz']
				expected.sort()

				if str(listing) is str(expected) :
					print "bad keys in level file's model listing"
					print "   expected:",expected
					print "   recieved:",listing

			return toRet


		self.terrainList = []
		'''get version of encoding'''
		line = nextNonComment( self.levelFile )
		if line !=  "version=0.01" :
			print "Level.py: Level.readFile(): bad version on",self.levelFile

		'''get number of mapTiles'''
		line = nextNonComment( self.levelFile )
		numMapTiles = parseNumMapTiles(line)

		if numMapTiles is not 1 :
			raise Exception("error can not support more than 1 map tiles yet")

		for i in xrange(numMapTiles):
			line = ( nextNonComment( self.levelFile ))
			parts=line.split()
			self.terrainList.append( TerrainClass.TerrainClass ( parts[0],
								parts[0] )
								)
			'''base.taskMgr.add( self.terrainList[i].asyncUpdate,
					str(self.terrainList[i] ))i'''
			#self.taskMgr.add(self.play,"play")

			try:
				self.terrainList[i].setMonoTexture(parts[1])
			except Exception as ex:
				print "Level.py readFile: noTexture"
				print "  ",ex
				pass

		'''when multi part levels are implimented this will change'''
		self.levelRoot = self.terrainList[0].getRoot()

		'''read in the models and their locations'''
		numModels = parseNumModels( nextNonComment( self.levelFile ) )

		for item in xrange(numModels):
			line = nextNonComment( self.levelFile )
			specs = parseModelLine( line )
			node = loader.loadModel(specs["model"] )
			node.reparentTo( self.levelRoot )
			node.setX( int( specs["x"] ) )
			node.setY( int( specs["y"] ) )
			node.setZ( int( specs["z"] ) )
			node.setH( int( specs["h"] ) )
			node.setY( int( specs["y"] ) )
			node.setP( int( specs["p"] ) )
			node.setSx( int (specs["sx"] ))
			node.setSy( int (specs["sy"] ))
			node.setSz( int (specs["sz"] ))
			modelList.append( item )

		return # finished loading the level
