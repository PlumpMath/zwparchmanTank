import TerrainClass
from panda3d.core import PandaNode, NodePath
import math
import random

class TerrainManager (object):
	class TerrainElement():
		def __init__(self,terrain,xPos,yPos):
			self.terrain=terrain
			self.xPos=xPos
			self.yPos=yPos

	def __init__(self):
		self.terrainElements=[]#holds all terrainElements
		self.terrainGrid=[[]]#holds terrainElements as they will be displayed
		self.dirty=True # the terrainGrid should be refreshed on next update
		self.rootNode = PandaNode("terrainManager root")
		self.root = NodePath( self.rootNode )
		self.terrainSize=257  #first=textureSize
		self.scale=16
		#locatoin that whereIsCamera returned last frame
		self.lastCamearaLocation = (0,0)
		self.currentCamearaLocation = (0,0)
		self.defaultBlockSize=64

	def whereIsCamera (self):
		'''where is the camera over the terrain
		returns a tuple of (x,y) for the grid location'''
		cam = base.camera.getPos()
		cam = (int (cam[0]) /(self.scale*self.terrainSize) ,
				int(cam[1]) /(self.scale*self.terrainSize ))
		return cam


	def newTerrainPart( self, heightMap, textureMap):
		'''create a new terrain element, when update is called they will be
		reorganized into a terrain grid and displayed'''
		self.dirtyGrid=True
		newPart = TerrainClass.TerrainClass(heightMap,heightMap)
		newPart.setMonoTexture( textureMap )
		newPart = self.TerrainElement( newPart, None, None )
		self.terrainElements.append( newPart )

	def getBlockSize(self):
		return self.terrainElements[0].terrain.getBlockSize()

	def setBlockSize( self, size=None ):
		if size is None:
			print "current block size:",self.getBlockSize()
			size = int ( raw_input( " input new blockSize:") )

		for i in self.terrainElements:
			i.terrain.setBlockSize( size )

		return

	def gridsAway( self, src, dst):
		'''src==tuple of starting grid location
		dst == tuple of ending grid location
		returns an integer containing number of grids seperating
		the two locations, does not take into account differences between
		diagnal and strait distance'''
		toRet = (abs(src[0]-dst[0]), 
				abs(src[1]-dst[1]))
		toRet = abs( toRet[0]+toRet[1])
		return toRet

	def autoBlockSizes(self):
		'''set the block sizes of the terrains based on the distance from
		the camera'''
		here = self.currentCamearaLocation
		default = self.defaultBlockSize
		if here == default:
			'''don't try to update if nothing changed'''
			return

		for row in range( len( self.terrainGrid ) ):
			for col in range( len( self.terrainGrid[row] ) ):
				new = default #defalut is defaultBlockSize
				distance = self.gridsAway( here, (row,col) )
				if distance > 2:
					new = new*(2**(distance-2))
					new = min ( self.terrainSize-1 , new )

				self.terrainGrid[row][col].setBlockSize( new )



	def update( self, task=None):
		'''update the terrain elements that need it
		and generate the terrain grid if it needs to be done ( is dirty)'''
		def isPerfectSquare( x ):
			y = int( math.sqrt(x) ) **2
			return y == x
		def makeTerrainGrid():
			self.terrainGrid=[] # empty list of lists
			self.dirty=False
			if not isPerfectSquare( len(self.terrainElements) ):
				raise Exception( "can't deal with non perfect square number "+
						"of terrains")
			side = int( math.sqrt( len( self.terrainElements ) ) )
			'''make terrain grid'''
			for i in xrange(side):
				y = i*self.terrainSize
				self.terrainGrid.append([])
				for j in xrange(side):
					x = j*self.terrainSize
					element = self.terrainElements[i*side+j]
					element.x=x
					element.y=y

					self.terrainGrid[i].append( element.terrain )
					element.terrain.getRoot().setPos( element.x, element.y,0 )

					elementNode= element.terrain.getRoot().getNode(0)
					self.rootNode.addChild(elementNode)

					
		#start the update
		'''reset camera locations'''
		self.lastCamearaLocation= self.currentCamearaLocation
		self.currentCamearaLocation= self.whereIsCamera()

		if self.lastCamearaLocation!= self.currentCamearaLocation:
			self.autoBlockSizes()

		if self.dirty:
			makeTerrainGrid()

		self.root.setScale(self.scale, self.scale, self.scale)
		#update one of the terrains
		side = len( self.terrainGrid )
		updateX = random.randint(0,side-1)
		updateY = random.randint(0,side-1)
		self.terrainGrid[updateX][updateY].asyncUpdate()

		

		if task is None:
			return
		else:
			return task.cont

	
	def getRoot(self):
		return  self.root
