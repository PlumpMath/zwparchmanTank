out = open ("level3.lvl","wb")

out.write("#comment\n")
out.write("version=0.01\n")
out.write("mapTiles=16\n")

endStr = ".png smallColor.png\n"
for i in range( 16 ):
	out.write( "levels/level03/part_"+str(i)+endStr)

out.write("models=1\n")
out.write("model=models/medTank.egg x=0 y=1 z=3 h=4 p=5 y=6 sx=1 sy=1 sz=1\n")
