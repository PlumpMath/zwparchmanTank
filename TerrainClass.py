from pandac.PandaModules import *
from direct.stdpy import threading
from panda3d.core import Thread
class TerrainClass(GeoMipTerrain):
	'''slightly imporoved GeoMipTerrain'''
	def __init__(self,
		name,
		geomap,
		blocksize=16,
		near = 24,
		far = 115,
		elevation=100
	):
		GeoMipTerrain.__init__(self, name)
		self.setBorderStitching(True)
		self.setHeightfield(Filename(geomap))
		self.setBlockSize(blocksize)
		self.setNear(near)
		self.setFar( far )
		self.setMinLevel(0)
		#self.setBruteforce(True)
		try:
			self.setFocalPoint(base.camera)
		except:
			pass
		self.root = self.getRoot()
		self.root.setSz(elevation)
		self.generate()
		self.updateSemaphore = threading.Semaphore(0)
		self.updateThread = self.AsyncUpdate(self,self.updateSemaphore)
		self.updateThread.start()

	def update(self, task=None):
		GeoMipTerrain.update(self)

		if task is not None:
			return task.cont
		'''dummy is None'''
		return

	def asyncUpdate( self,task=None ):
		if self.updateSemaphore.getCount() is 0 :
			self.updateSemaphore.release()

		if task is None:
			return
		else :
			return task.cont

	class AsyncUpdate( threading.Thread ):
		'''update the GeoMipTerrain in it's own thread'''
		def __init__( self, terrain, sema ):
			threading.Thread.__init__(self)
			self.sema= sema
			self.terrain = terrain

		def run(self):
			while True :
				self.sema.acquire()
				self.terrain.update()
			return
		

	def setMonoTexture(self, texture):
		ts = TextureStage('ts')
		tex = loader.loadTexture(texture)
		self.root.setTexture(ts, tex)

	def reparentTo(self, target):
		self.getRoot().reparentTo(target)




