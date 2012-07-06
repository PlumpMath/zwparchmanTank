#!/usr/bin/python

import socket
import Protical
import Level
import sys

import cPickle
import Queue
from direct.stdpy import threading2 as threading
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from pandac.PandaModules import *
loadPrcFileData("", """#
win-origin 0 0
sync-video 0
show-frame-rate-meter #t
"""
)

host = 'localhost'
port = 3000
if len(sys.argv) >= 2:
	port = int(sys.argv[1])
if len(sys.argv) >= 3:
	host = sys.argv[2]


class ClientGame(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		#input setup
		self.keys={"w"      :0,
				   "t"      :0
				   }

		#socket init
		self.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host,port))

		self.toSend    =Queue.Queue(1000)
		self.toProcess =Queue.Queue(1000)

		self.socket.setblocking(False)

		self.taskMgr.add(self.play,"play")
		self.keyboardSetup()
		self.msg()
		self.requestLevel()
		self.msg()

	def keyboardSetup(self):
		self.accept("w"         ,self.setKey      ,["w"      ,1])
		self.accept("w-up"      ,self.setKey      ,["w"      ,0])
		self.accept("t"         ,self.setKey      ,["t"      ,1])
		self.accept("t-up"      ,self.setKey      ,["t"      ,0])
		self.accept("escape"    ,self.die         )
		self.accept("p"         ,self.requestLevel )
		self.accept("space"     ,base.wireframeOn)
		self.accept("space-up"  ,base.wireframeOff)

	def setKey(self,key,value):
		'''used by keyboard setup to handle key presses'''
		self.keys[key] = value


	def getInput(self):
		pass
			
	def requestLevel( self ):
		msg = Protical.requestLevel()
		self.toSend.put(msg)


	def play(self,task):
		self.getInput()
		self.sendData()
		if self.keys["w"] is not 0 :
			self.msg()

		self.recvServer()
		self.processMessages()
		return Task.cont


	def processMessages(self):
		done = False
		while not done :
			item=None
			try :
				item = self.toProcess.get(False)
			except Queue.Empty:
				done = True
				continue

			if len(item) is  0 :
				continue

			message = cPickle.loads(item)
			msgType = message[0]

			'''figure out what kind of message it is'''
			if ( Protical.names[msgType]=="chatSend" ):
				self.displayChatInput( message )
			elif  Protical.names[msgType]=="levelToLoad":
				self.loadNewLevel( message )


	def loadNewLevel( self,message):
		'''load a level that the server said to load'''

		''' pull the string out for the level '''
		levelString = message[1][0]
		''' load the model for the level'''
		self.level = Level.Level(levelString)
		self.level.getRoot().reparentTo(render)

	def displayChatInput(self,message):
		'''display incoming chat messages'''
		print message[1][0]

	def sendData(self):
		'''send data to the server'''
		while True:
			try:
				msg = self.toSend.get(False)
			except Queue.Empty:
				return

			try:
				self.socket.sendall(msg)
			except socket.error as ex:
				if ex[0] is not 11 : # 11 == socket is buisy try later
					raise ex
				else:
					'''place back in queue to resend'''
					self.toSend.put(msg)
					return

	def die(self):
		''' safely quit the game'''
		self.toSend.put( Protical.sendQuit() );
		self.sendData()
		sys.exit(0)

	def recvServer(self):
		'''recieve input from the server, and send it to the toProcess queue'''
		data = None
		try:
			data = self.socket.recv(4096)
		except socket.error as ex:
			if ex[0] is not 104 and ex[0] is not 11 :
				print "recvServer : readError [", ex[0], "] ",ex[1]

		if data is not None:
			print "data:",data
			self.toProcess.put( data ) # if queue is full will hang the program


	def msg(self):
		self.toSend.put(Protical.chatSend("poop"))



app = ClientGame()
app.run()
