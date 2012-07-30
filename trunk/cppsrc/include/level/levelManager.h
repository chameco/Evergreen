#ifndef LEVELMANAGER_H
#define LEVELMANAGER_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
namespace level {
	using namespace std;
	class levelManager : public chameleon::event::listener {
		public:
			levelManager(chameleon::event::listener *_manager);
			void ev_update(void *data);
			void ev_getLevel(void *data);
			void ev_switchLevel(void *data);
			void ev_spawnEntity(void *data);
			void ev_killEntity(void *data);
		private:
			chameleon::event::manager *manager;
			double curtime;
	};
}
#endif
