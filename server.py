#!/usr/bin/python
import socket
import Queue
import time

import Protical
import cPickle
#from panda3d.bullet import BulletWorld
#from direct.showbase.ShowBase import ShowBase

'''class App(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		return'''

port_address = 2000
backLog = 1000
toWriteQueueSize = 1000

class ServerGame :

	def __init__(self, levelName):
		self.port_address = 2000
		host = ''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.levelName = levelName

		worked = False
		while not worked:
			try:
				self.socket.bind((host, self.port_address ))
			except socket.error as ex:
				self.port_address=self.port_address + 1
			else:
				worked=True

		print "listening on port ", self.port_address

		port_address = self.port_address
		del self.port_address

		self.socket.listen(backLog)
		self.connections=[]
		self.toProcess = Queue.Queue(toWriteQueueSize)
		self.toWrite = Queue.Queue(toWriteQueueSize)

		self.socket.setblocking(False)

	def gameLoop(self):
		toRun = True
		while toRun:
			self.newClients()
			self.readClients()
			self.processRequests()
			self.writeClients()
			if len( self.connections ) == 0 :
				time.sleep(.1)

	def processRequests(self):
		done = False
		while not done:
			try:
				data=self.toProcess.get(False)
			except Queue.Empty:
				done = True
				continue
			if len( data[1]) > 0  :
				msg = cPickle.loads(data[1] )#repace msg with unpickled msg
			else :
				continue # try next message

			data = ( data[0], msg )

			msgType = data[1][0]
			'''find out what message this was and take the proper action'''
			print "data: ",data
			#print "msgType",msgType
			if ( Protical.names[msgType]=="chatSend" ):
				self.sendChatServer(data)
			elif ( Protical.names[msgType]=="requestLevel"):
				self.sendLevelToLoad(data)
			elif ( Protical.names[msgType]=="quiting"):
				self.clientQuiting( data )

	def clientQuiting( self, data ):
		if data[0] in self.connections :
			self.connections.remove( data[0] )
			print data[0]," quiting Num left: ", len( self.connections)

	def sendChatServer(self,data):
		'''send the chat message to everyone but the sender'''
		for client in self.connections:
			if client != data[0]:
				#send the chat message everywhere
				stringOut=Protical.chatSend(data[1][1][0])#the string to send out
				self.toWrite.put( (client,stringOut) )
		return

	def sendLevelToLoad( self, data ):
		client = data [0]
		payload = Protical.sendLevelToLoad( self.levelName )
		self.toWrite.put( (client, payload) )
		return



	def readClients(self):
		for c in self.connections:
			try:
				data = c.recv(1024)
				self.toProcess.put( (c,data) )
			except socket.error as ex:
				if ex[0]!=104 and ex[0] != 11 :
					print "reading : bye world [", ex[0], "] ",ex[1]
		return

	def writeClients(self):
		done = False
		while not done :
			try : 
				item = self.toWrite.get(False)
			except Queue.Empty :
				done = True
				continue

			try:
				item[0].sendall(item[1]) # send the message
			except socket.error as ex:
				print "server.py: writeClient: error caught"
				if ex[0]==104 or 1 :
					print "  writing : ",ex[0]," ",ex[1]
					if item[0] in self.connections:
						self.connections.remove( item[0] )

			self.toWrite.task_done()
		return

	def newClients(self):
		try:
			conn, addr = self.socket.accept()
			conn.setblocking(False)
			print 'Connected by', addr
			self.connections.append(conn)
		except socket.error as ex:
			if ex[0]==11:
				pass
			else:
				'''windows fix'''
				#raise ex
				return



	def loadLevel(self, levelName):
		pass


server = ServerGame("levels/level1.lvl")
#app = App()
#print loader
server.gameLoop()
