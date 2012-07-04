import cPickle

names={1:"mainTerrain", 2: "groundModel",3:"curcularTrigerRegion",
		4:"spawnCircle",5:"heightMapNone", 6:"mainModelPath"}

numbers={}
for item in names:
	numbers[names[item]]=item

modes=["text","pickle0","pickleNeg1","binary"]

class WriteLevel (object):
	def __init__( self,fileName, mode="pickleNeg1", fileObject=None ):
		self._mode = mode

		if fileObject == None:
			self.levelFile = open(fileName, "w")
		else:
			self.levelFile = fileObject

		self._uniqueNumber=-1


	def encodeCircularTrigerRegion(self,triggerType, team, x,y,size):
		name = self.getUniqueName()
		recordType = numbers["curcularTrigerRegion"]
		payload = {team:"team","x":float(x),"y":float(y),"radius":float(size)}
		cPickle.dump( [name , recordType, payload], self.levelFile ,-1 )
		return name

	def encodeMainModelPath(self,pathString,scaleX=1,scaleY=1,posX=0,posY=0):
		name = self.getUniqueName()
		recordType = numbers["mainModelPath"]
		payload = {"pathString":pathString,"scaleX":float(scaleX,),
				"scaleY":float(scaleY),"posX": float(posX),"posY":float(posY) }
		cPickle.dump( [name,recordType,payload],self.levelFile, -1 )
		return name

	def encodeModel(self,modelPath,x,y,z=None):
		name = self.getUniqueName()
		recordType=numbers["groundModel"]
		payload = {"x":float(x),"y":float(y)}
		if z != None:
			payload["z"]=float(z)


	def encodeMainTerrain(self, heightMap, texture ):
		pass


	def getUniqueName(self,_toRet=None):
		self._uniqueNumber+=1
		a=str(self._uniqueNumber)
		return ( a )

	def closeFile(self):
		self.levelFile.close()
		return
			
if  __name__ == "__main__" :
	a=WriteLevel("file")
	a.encodeCircularTrigerRegion(1,2,3.33,4.44,5.55)
	a.encodeMainModelPath("bigModel.egg")
	a.closeFile()

	f = open ("file","rb")
	d={}
	while True:
		try:
			b = cPickle.load(f)
		except EOFError:
			break
		else:
			d[b[0]]=b[1:]

