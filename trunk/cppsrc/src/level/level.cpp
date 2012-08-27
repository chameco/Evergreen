#include "level/level.h"
using namespace std;
level::level::level(chameleon::event::manager *_manager, int _index) {
	manager = _manager;
	index = _index;
	blocks = new map<string, base::block *>();
	blockState = new base::group<base::physicalObject>();
	entityState = new base::group<base::physicalObject>();
	floorState = new base::group<base::floor>();
	startCoords = new vector<int>();
	(*startCoords)[0] = 0;
	(*startCoords)[1] = 0;
}
level::level::~level() {
	for (map<string, base::block *>::iterator it = blocks->begin(); it != blocks->end(); it++) {
		delete (*it).second;
	}
	delete blocks;
	delete blockState;
	delete entityState;
	delete floorState;
	delete startCoords;
}
void level::level::loadLevel(){
	int x, y, len;
	x = y = 0;
	len = levelImp.length() - 1;
	char cur;
	for (int c = 0; c <= len; ++c) {
		cur = levelImp[c];
		switch (cur) {
			case '\n':
				y += 32;
				x = 0;
				break;
			case 'C':
				(*startCoords)[0] = x;
				(*startCoords)[1] = y;
				x += 32;
				break;
			case ' ':
				x += 32;
				break;
			default:
				blockState->add((*blocks)[string(&c, 1)]->clone());
				break;
		}
	}
}
