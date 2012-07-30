#ifndef SERVER_NETWORKCONTROLLER_H
#define SERVER_NETWORKCONTROLLER_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
#include "network/wrapper.h"
namespace server {
	namespace network {
		using namespace std;
		class networkController : public chameleon::event::listener {
			public:
				networkController(chameleon::event::manager *_manager, network::wrapper *_client);
				void ev_update(void *data);
			private:
				chameleon::event::manager *manager;
				network::wrapper *client;
		};
	}
}
#endif
