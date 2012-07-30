#ifndef NETWORKSUBSYSTEM_H
#define NETWORKSUBSYSTEM_H
//LIBRARY INCLUDES:
#include <string>
#include <list>
//USER INCLUDES:
#include "chameleon.h"
#include "network/wrapper.h"
namespace server {
	namespace network {
		using namespace std;
		class networkSubsystem : public chameleon::event::manager, public chameleon::event::listener {
			public:
				networkSubsystem(chameleon::event::manager *_manager, network::wrapper *_client);
				void ev_distEntity(void *data);
				void ev_kill(void *data);
				void ev_distLevel(void *data);
				void ev_getLevel(void *data);
				void ev_distSwitchLevel(void *data);
				void ev_entityMoved(void *data);
				void ev_entitySpawned(void *data);
				void ev_entityKilled(void *data);
				void ev_gameOver(void *data);
				void ev_update(void *data);
			private:
				list<chameleon::event::listener *> *plugins;
				chameleon::event::manager *manager;
				network::wrapper *client;
		};
	}
}
#endif
