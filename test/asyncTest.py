from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import sys
from time import sleep
loadPrcFileData("", """#
win-origin 0 0
sync-video 0
show-frame-rate-meter #t
"""
)
from direct.stdpy import threading
#from direct.stdpy import threading2 as threading
#import threading
import direct.directbase.DirectStart

class Tester( object ):
	def __init__(self,string):
		self.string = string
		self.updateLock = threading.Lock()
		self.updateNumber=0
		
	def update(self,task=None):
		if self.updateLock.acquire(False):
			'''if we recieved the lock'''
			print "update, ",self.updateNumber
			sleep(3)
			print "done"
			self.updateNumber+=1
			self.updateLock.release()
		if task==None:
			return
		else :
			return task.cont
			
	def asyncUpdate( self,task=None ):
		try:
			a=AsyncUpdate(self)
			a.start()
		#except Exception as ex:
		except IOError as ex :
			print "exception"
			print ex

		if task==None:
			return
		else:
			return task.cont

class AsyncUpdate( threading.Thread):
	def __init__( self, terrain):
		threading.Thread.__init__(self)
		self.terrain = terrain
	def run(self):
		self.terrain.update()
		return
		
		
class world(DirectObject):
	def setup(self):
		self.test = Tester("one")
		#taskMgr.add(self.ground.asyncUpdate,"groundUpdate")
		#taskMgr.add(self.test.update,"groundUpdate")
		
		self.accept("f-up", self.test.update )
		self.accept('g-up',self.test.asyncUpdate)
		self.accept('h-up', self.talk )
		self.accept("escape",sys.exit )

	def talk(self):
		print "in main thread"

trash = AsyncUpdate( None )
del trash

w=world()
w.setup()
print "threading support? ",Thread.isThreadingSupported()
base.disableMouse()

run()
