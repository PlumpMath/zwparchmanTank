from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight
from panda3d.core import VBase4
from math import radians,degrees,cos,sin,pi
import sys
 
class FpsCam :
	def __init__(self,camera):
		self.cam = camera

	def moveX(self,amt):
		angle = self.cam.getH()
		angle = radians(angle)

		x = self.cam.getX()
		y = self.cam.getY()
		self.cam.setX( x + amt*cos(angle))
		self.cam.setY( y + amt*sin(angle))
		return

	def moveY(self,amt):
		angle = radians ( self.cam.getH() )

		x = self.cam.getX()
		y = self.cam.getY()
		self.cam.setX( x - amt*sin(angle))
		self.cam.setY( y + amt*cos(angle))
		return

	def yaw( self,amt):
		angle = self.cam.getH()
		self.cam.setH( angle + .32*amt)
		return

	def pitch( self,amt):
		angle = self.cam.getP()
		self.cam.setP( angle + .32*amt)
	
	def moveZ(self,amt):
		self.cam.setZ( self.cam.getZ()+amt)
		return





class MyApp(ShowBase):
 
	def __init__(self):
		ShowBase.__init__(self)
		dir(self)
		self.disableMouse()
 
		# Load the environment model.
		self.environ = self.loader.loadModel("../levels/level01.egg")
		# Reparent the model to render.
		self.environ.reparentTo(self.render)
		'''add a light'''
		self.light = PointLight("dLight")
		self.light.setAttenuation( (.01,.01,.01 ) )
		self.light.setSpecularColor ( VBase4(1,1,0,1 ) )
		self.lightNode = render.attachNewNode(self.light)
		self.lightNode.setZ(10)
		render.setLight(self.lightNode)

		'''move light constants'''
		self.moveLightDirection = -1000

		self.taskMgr.add(self.moveLight,"lightMove")
		self.taskMgr.add(self.fpsInput,"fpsInput")

		'''fps cam controls'''
		self.keymap={"w":0,"a":0,"s":0,"d":0,"e":0,"q":0,
				"j":0,"k":0,"l":0,"i":0}
		
		self.fps = FpsCam(self.camera)
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
		self.accept("escape",sys.exit )




	def setKey(self,key,value):
		self.keymap[key]=value
		return

	def fpsInput(self,task):
		self.fps.moveX( self.keymap["d"]-self.keymap["a"])
		self.fps.moveY( self.keymap["w"]-self.keymap["s"])
		self.fps.moveZ( self.keymap["e"]-self.keymap["q"])
		self.fps.yaw  ( self.keymap["j"]-self.keymap["l"])
		self.fps.pitch( self.keymap["i"]-self.keymap["k"])
		return task.cont

	def moveLight(self,task):
		#print dir(self.lightNode)
		where = self.lightNode.getX()
		#print where
		self.lightNode.setX(where-task.getDt()*self.moveLightDirection)
		if self.lightNode.getX()< -10:
			self.moveLightDirection *= -1
		elif self.lightNode.getX() > 10:
			self.moveLightDirection *= -1

		return task.cont



 
 
app = MyApp()
app.run()
