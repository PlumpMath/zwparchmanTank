all:
	cd levels ; make
	cd models ; make
	#make done

server_run: all
	./server.py &

client_run: all
	./client.py

clean:
	cd levels ; make clean
	cd models; make clean
	rm *temp *~ *pyc -f
	#clean finished
