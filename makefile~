all:
	cd levels ; make
	cd models ; make
	#make done

server_run: all
	./server.py &

client_run: all
	./client.py
