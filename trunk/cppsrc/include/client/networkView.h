#ifndef CLIENT_NETWORKVIEW_H
#define CLIENT_NETWORKVIEW_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
namespace client {
	using namespace std;
	class networkView : public chameleon::event::listener {
		public:
			networkView(chameleon::event::manager *_manager, network::wrapper *_server);
			void ev_up(void *data);
			void ev_down(void *data);
			void ev_left(void *data);
			void ev_right(void *data);
			void ev_attack(void *data);
			void ev_logout(void *data);
		private:
			chameleon::event::manager *manager;
			network::wrapper *server;
	};
}
#endif
