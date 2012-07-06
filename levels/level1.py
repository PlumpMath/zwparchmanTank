out = open ("level1.lvl","wb")

out.write("#comment\n")
out.write("version=0.01\n")
out.write("mapTiles=256\n")

endStr = ".png smallColor.png\n"
for i in range( 256 ):
	out.write( "levels/level01/part_"+str(i)+endStr)

out.write("models=1\n")
out.write("model=models/medTank.egg x=0 y=1 z=3 h=4 p=5 y=6 sx=1 sy=1 sz=1\n")
