all : level1.lvl level3.lvl
	#levels finished

level1.lvl: level1.py level01/part_0.png
	python level1.py

level3.lvl: level3.py level03/part_0.png
	python level3.py

level01/part_0.png :
	../tile.py -f rolling.png -s 257 -o level01/part_ -b 16
level03/part_0.png :
	../tile.py -f level03.png -s 257 -o level03/part_ -b 16

clean :
	rm level1.lvl -f
	rm level3.lvl -f
	rm level01/* -f
	rm level03/* -f
	rm *temp *~ -f

