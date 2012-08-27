#include "level/levelManager.h"
using namespace std;
level::levelManager::levelManager(chameleon::event::listener *_manager) {
	manager = _manager;
	SRAR(level::levelManager, update);
	SRAR(level::levelManager, getLevel);
	SRAR(level::levelManager, switchLevel);
	SRAR(level::levelManager, spawnEntity);
	SRAR(level::levelManager, killEntity);
	curtime = boost::chrono::system_clock::now();
}
void level::levelManager::ev_update(void *data) {
	boost::chrono::system_clock::time_point t = boost::chrono::system_clock::now();
	boost::chrono::duration<double> delta = t - curtime;
	base::group<base::physicalObject> *blockState;
	base::group<base::physicalObject> *entityState;
	if (delta.count() >= 0.1) {
		curtime = t;
		for (list<level::level *>::iterator it = levels->begin(); it != levels->end(); it++) {
			blockState = (*it)->getBlockState();
			entityState = (*it)->getEntityState();
			blockState->insert(entityState->begin(), entityState->end());
			(*it)->updateEntities(blockState);
			delete blockState;
			delete entityState;
		}
	}
}
void level::levelManager::ev_getLevel(void *data) {
	base::player *p = (base::player *) data;
	playerspec_event e = {p->getData["name"], (*levels)[p->getCurLevel()]};
	manager->alert("distLevel", (void *) &p);
}
void level::levelManager::ev_switchLevel(void *data) {
	
