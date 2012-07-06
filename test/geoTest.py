# -*- coding: utf-8 -*-
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import sys
from math import radians , sin , cos, degrees
loadPrcFileData("", """#
win-origin 0 0
sync-video 0
show-frame-rate-meter #t
"""
)
from TerrainClass import TerrainClass
from direct.stdpy import threading
import direct.directbase.DirectStart


textureName="color.png"
heightMapName="genesis.png"

if len(sys.argv) >= 2 :
	heightMapName= sys.argv[1]
if len( sys.argv) >= 3 :
	textureName=sys.argv[2]

#=================================================================
#

class world(DirectObject):
	def setup(self):
		self.ground=TerrainClass(
			name='scenario_ground',
			geomap=heightMapName,
			elevation= 50
		)
		self.ground.setMonoTexture(textureName)
		self.ground.reparentTo(render)


		self.camera = camera
		
		taskMgr.add(self.fpsInput,"fpsInput")
		taskMgr.add(self.ground.asyncUpdate,"groundUpdate")
		#taskMgr.add(self.ground.update,"groundUpdate")
		'''fps cam controls'''
		self.keymap={"w":0,"a":0,"s":0,"d":0,"e":0,"q":0,
				"j":0,"k":0,"l":0,"i":0}
		
		self.fps = FpsCam(self.camera, .8)
		self.accept("a", self.setKey,     ["a",1] )
		self.accept("a-up", self.setKey,  ['a',0] )
		self.accept("w", self.setKey,     ["w",1] )
		self.accept("w-up", self.setKey,  ["w",0] )
		self.accept("s", self.setKey,     ["s",1] )
		self.accept("s-up", self.setKey,  ["s",0] )
		self.accept("d", self.setKey,     ["d",1] )
		self.accept("d-up", self.setKey,  ["d",0] )
		self.accept("e", self.setKey,     ["e",1] )
		self.accept("e-up", self.setKey,  ["e",0] )
		self.accept("q", self.setKey,     ["q",1] )
		self.accept("q-up", self.setKey,  ["q",0] )
		self.accept("j", self.setKey,     ["j",1] )
		self.accept("j-up", self.setKey,  ["j",0] )
		self.accept("k", self.setKey,     ["k",1] )
		self.accept("k-up", self.setKey,  ["k",0] )
		self.accept("l", self.setKey,     ["l",1] )
		self.accept("l-up", self.setKey,  ["l",0] )
		self.accept("i", self.setKey,     ["i",1] )
		self.accept("i-up", self.setKey,  ["i",0] )
		self.accept("f", self.ground.update )
		self.accept('g',self.ground.asyncUpdate)
		self.accept("space", base.wireframeOn)
		self.accept("space-up", base.wireframeOff)
		self.accept("-",self.deltaFar,[-2])
		self.accept("=",self.deltaFar,[2])
		self.accept("9",self.deltaNear,[-2])
		self.accept("0",self.deltaNear,[2])
		self.accept("7",self.deltaBlock,[-2])
		self.accept("8",self.deltaBlock,[2 ])
		self.accept("5",self.deltaSpeed,[-2])
		self.accept("6",self.deltaSpeed,[2])
		self.accept("escape",sys.exit )




	def setKey(self,key,value):
		self.keymap[key]=value
		return

	def fpsInput(self,task):
		dt = task.getDt()
		if dt > .05 :
			return task.cont

		self.fps.moveX( (self.keymap["d"]-self.keymap["a"])*dt*10000)
		self.fps.moveY( (self.keymap["w"]-self.keymap["s"])*dt*10000)
		self.fps.moveZ( (self.keymap["e"]-self.keymap["q"])*dt*10000)
		self.fps.yaw  ( (self.keymap["j"]-self.keymap["l"])*dt*10000)
		self.fps.pitch( (self.keymap["i"]-self.keymap["k"])*dt*10000)
		return task.cont

	def deltaSpeed( self, x ):
		cur = self.fps.speed
		if x>1:
			cur = cur * 2
		else:
			cur = cur /2

		self.fps.speed = cur
		print "fpsSpeed:",cur
		return

	


	def deltaBlock( self, x ):
		cur = self.ground.getBlockSize()
		if x>1:
			cur = cur * 2
		else:
			cur = cur /2

		self.ground.setBlockSize(cur)
		print "block size:",cur
		return


	def deltaFar( self, x ):
		cur = self.ground.getFar()
		if x>1:
			cur = cur *1.1
		else:
			cur = cur /1.1

		self.ground.setFar(cur)
		print "far:",cur
		return

	def deltaNear(self, x):
		cur = self.ground.getNear()
		if x>1:
			cur = cur *1.1
		else:
			cur = cur /1.1

		self.ground.setNear(cur)
		print "near:",cur
		return





#=================================================================
#
class FpsCam :
	def __init__(self,camera, speed=10):
		self.cam = camera
		self.speed = speed 

	def moveX(self,amt):
		angle = self.cam.getH()
		angle = radians(angle)

		x = self.cam.getX()
		y = self.cam.getY()
		self.cam.setX( x + amt*cos(angle)* self.speed)
		self.cam.setY( y + amt*sin(angle)* self.speed)
		return

	def moveY(self,amt):
		angle = radians ( self.cam.getH() )

		x = self.cam.getX()
		y = self.cam.getY()
		self.cam.setX( x - amt*sin(angle)* self.speed)
		self.cam.setY( y + amt*cos(angle)* self.speed)
		return

	def yaw( self,amt):
		angle = self.cam.getH()
		self.cam.setH( angle + .64*amt)
		return

	def pitch( self,amt):
		angle = self.cam.getP()
		self.cam.setP( angle + .64*amt)
	
	def moveZ(self,amt):
		self.cam.setZ( self.cam.getZ()+amt* self.speed)
		return






w=world()
w.setup()
base.cam.setPos(0,0,90)
#base.cam.lookAt(w.ground.root)
base.disableMouse()

run()
