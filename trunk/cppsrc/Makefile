CC = g++
CPPFLAGS = "-Iinclude"
SERVERSRC = src/server/spinner.o
SERVER_DBSRC = src/server/db/dbManager.o
SERVER_NETWORKSRC = src/server/network/networkSubsystemDelegator.o src/server/network/networkSubsystem.o \
					src/server/network/networkView.o src/server/network/networkController.o
BASESRC = src/base/image.o src/base/group.o src/base/drawnObject.o src/base/floor.o src/base/woodFloor.o \
		  src/base/physicalObject.o src/base/block.o src/base/stone.o src/base/stairsUp.o src/base/stairsDown.o \
		  src/base/stairsWarp.o src/base/entity.o src/base/player.o
NETWORKSRC = src/network/wrapper.o
LEVELSRC = src/level/level.o src/level/levelManager.o
CLIENTSRC = src/client/glGame.o  src/client/networkView.o src/client/networkController.o

all : evergreen_server evergreen_client

evergreen_server : server base level network
	$(CC) src/server/*.o src/server/db/*.o src/server/network/*.o src/base/*.o src/level/*.o src/network/*.o -lboost-regex -o evergreen_server #Boost Asio requires regexes.

evergreen_client : client base level network
	$(CC) src/client/*.o src/base/*.o src/level/*.o src/network/*.o -lboost-regex -o evergreen_client

server : $(SERVERSRC) $(SERVER_DBSRC) $(SERVER_NETWORKSRC)

server_clean :
	rm -f src/server/*.o src/server/db/*.o src/server/network/*.o

client : $(CLIENTSRC)

client_clean :
	rm -f src/client/*.o

base : $(BASESRC)

base_clean :
	rm -f src/base/*.o

network : $(NETWORKSRC)

network_clean :
	rm -f src/network/*.o

level : $(LEVELSRC)

level_clean :
	rm -f src/level/*.o

clean : server_clean client_clean base_clean network_clean level_clean

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
