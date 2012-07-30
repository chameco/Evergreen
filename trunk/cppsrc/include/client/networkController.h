#ifndef CLIENT_NETWORKCONTROLLER_H
#define CLIENT_NETWORKCONTROLLER_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
#include "network/wrapper.h"
#include "base/group.h"
namespace client {
	using namespace std;
	class networkController : public chameleon::event::listener {
		public:
			networkController(chameleon::event::manager *_manager, network::wrapper *_server);
			void ev_levelReceived(void *data);
			void ev_update(void *data);
		private:
			chameleon::event::manager *manager;
			network::wrapper *server;
			base::group *blockState;
			base::group *floorState;
			base::group *entityState;
	};
}
#endif
