CC = g++
SERVERSRC = spinner.cpp
SERVER_DBSRC = dbManager.cpp
SERVER_NETWORKSRC = networkSubsystemDelegator.cpp networkSubsystem.cpp networkView.cpp networkController.cpp
BASESRC = image.cpp group.cpp drawnObject.cpp floor.cpp woodFloor.cpp physicalObject.cpp block.cpp stone.cpp stairsUp.cpp stairsDown.cpp stairsWarp.cpp entity.cpp player.cpp
NETWORKSRC = wrapper.cpp
LEVELSRC = level.cpp levelManager.cpp
CLIENTSRC = glGame.cpp  networkView.cpp networkController.cpp

all : evergreen_server evergreen_client

evergreen_server : server base level network
	$(CC) src/server/*.o src/server/db/*.o src/server/network/*.o src/base/*.o src/level/*.o src/network/*.o -lboost-regex -o evergreen_server #Boost Asio requires regexes.

evergreen_client : client base level network
	$(CC) src/client/*.o src/base/*.o src/level/*.o src/network/*.o -lboost-regex -o evergreen_client

server : $(SERVERSRC) $(SERVER_DBSRC) $(SERVER_NETWORKSRC)
	cd src/server
	$(CC) -c $(SERVERSRC) -I../../include
	cd db
	$(CC) -c $(SERVER_DBSRC) -I../../../include
	cd ../network
	$(CC) -c $(SERVER_NETWORKSRC) -I../../../include
	cd ../../..

client : $(CLIENTSRC)
	cd src/client
	$(CC) -c $(CLIENTSRC) -I../../include
	cd ../..

base : $(BASESRC)
	cd src/base
	$(CC) -c $(BASESRC) -I../../include
	cd ../..

network : $(NETWORKSRC)
	cd src/network
	$(CC) -c $(NETWORKSRC) -I../../include
	cd ../..

level : $(LEVELSRC)
	cd src/level
	$(CC) -c $(LEVELSRC) -I../../include
	cd ../..

clean :
	rm -f src/base/*.o src/level/*.o src/network/*.o src/client/*.o src/server/*.o src/server/db/*.o src/server/network/*.o

builddeb:
	# build the source package in the parent directory
	# then rename it to project_version.orig.tar.gz
	make source
	# build the package
	dpkg-buildpackage -i -I -rfakeroot

source :
	tar -cf ../chameleon_1.0.orig.tar.gz include src Makefile

tags :
	ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .
