#ifndef LEVELMANAGER_H
#define LEVELMANAGER_H
//LIBRARY INCLUDES:
#include <string>
#include <list>
#include <boost/bind.hpp>
#include <boost/chrono.hpp>
//USER INCLUDES:
#include "chameleon.h"
#include "utils.h"
#include "level/level.h"
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
		protected:
			list<level::level *> *levels;
		private:
			chameleon::event::manager *manager;
			boost::chrono::system_clock::time_point curtime;
	};
}
#endif
