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

	def newTerrainPart( self, heightMap, textureMap):
		'''create a new terrain element, when update is called they will be
		reorganized into a terrain grid and displayed'''
		self.dirtyGrid=True
		newPart = TerrainClass.TerrainClass(heightMap,heightMap)
		newPart.setMonoTexture( textureMap )
		newPart = self.TerrainElement( newPart, None, None )
		self.terrainElements.append( newPart )

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
		if self.dirty:
			makeTerrainGrid()

		self.root.setScale(16,16,16)
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
