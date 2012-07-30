#ifndef GLGAME_H
#define GLGAME_H
//LIBRARY INCLUDES:
#include <string>
#include <map>
//USER INCLUDES:
#include "chameleon.h"
#include "base/group.h"
#include "base/entity.h"
namespace client {
	using namespace std;
	class glGame : public chameleon::event::manager, public chameleon::event::listener {
		public:
			glGame();
			void ev_distLevel(void *data);
			void ev_entityMoved(void *data);
			void ev_entitySpawned(void *data);
			void ev_entityKilled(void *data);
			void ev_gameOver(void *data);
			void main();
		private:
			base::group *blockState;
			base::group *floorState;
			map<string, base::entity *> *entities;
	};
}
#endif
