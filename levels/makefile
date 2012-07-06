all : level1.lvl 
	#levels finished

level1.lvl: level1.py level1/part_0.png
	python level1.py

level1/part_0.png :
	../tile.py -f rolling.png -s 257 -o level01/part_ -b 16

clean :
	rm level1.lvl -f
	rm level01/* -f

