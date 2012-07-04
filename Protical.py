from cPickle import dumps

numbers = { "requestID"      :int(0)  , 
			"givenID"        :int(1)  ,
		    "chatSend"       :int(2)  , 
		    "levelToLoad"    :int(4)  ,
		    "tankData"       :int(5)  ,
		    "uploadMove"     :int(6)  ,
		    "fire"           :int(7)  , 
			"adjustHealth"   :int(8)  ,
			"requestLevel"   :int(9)  ,
			"quiting"        :int(10) 
		    }

names = {}
#load names with the inverse of numbers so that all numbers map
# to a name that can be maped back to a number
for x in numbers:
	names[numbers[x]]=x


''' requestID, request the id to be used for the player '''
''' givenID, recieve the id to be used for the local player '''
''' chatSend, send a chat message to everyone, except the sender '''
''' chatRecieve, recieve a chat message'''
''' levelToLoad, the level that is to be loaded by the client'''
''' tankData, contains all of the data that a tank has including
	velocity tuple, position tuple, direction tuple '''
''' uploadMove, sent when a player uploads a move to the server'''
''' fire, player sends direction of firing to server, if it is 
	a valid thing to do the server lets the player fire the gun
	creating a bullet and sending it to all players, including
	the owner'''
''' adjustHealth, the health of the player is changed, this will
	happen when the server decides that the player has been shot'''
''' requestLevel, request level to be played, levelToLoad should
	be sent in response '''
''' quiting, sent when server or client is quiting so that the other knows
	that it will recieve no more information'''

def chatSend( string ):
	"""Creates a string ready to be transmited over a network
	the string created will be a chatSend packet with string
	as the payload"""
	toRet = dumps( (numbers["chatSend"], (string,) ) )
	return toRet

def sendLevelToLoad( string ):
	toRet = dumps( (numbers["levelToLoad"], (string,)))
	return toRet

def requestLevel():
	toRet = dumps( (numbers["requestLevel"],) )
	return toRet

def sendQuit():
	toRet = dumps( (numbers["quiting"],))
	return toRet


