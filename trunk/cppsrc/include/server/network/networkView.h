#ifndef SERVER_NETWORKVIEW_H
#define SERVER_NETWORKVIEW_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
#include "network/wrapper.h"
#include "level/level.h"
namespace server {
	namespace network {
		using namespace std;
		class networkView : public chameleon::event::listener {
			public:
				networkView(chameleon::event::manager *_manager, network::wrapper *_client);
				void ev_sendLevel(void *data);
				void ev_distLevel(void *data);
				void ev_entityMoved(void *data);
				void ev_entitySpawned(void *data);
				void ev_entityKilled(void *data);
				void ev_gameOver(void *data);
			private:
				chameleon::event::manager *manager;
				network::wrapper *client;
				level::level *level;
		};
	}
}
#endif
