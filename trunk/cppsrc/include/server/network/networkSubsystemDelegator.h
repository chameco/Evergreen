#ifndef NETWORKSUBSYSTEMDELEGATOR_H
#define NETWORKSUBSYSTEMDELEGATOR_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
#include "server/network/networkSubsystem.h"
namespace server {
	namespace network {
		using namespace std;
		class networkSubsystemDelegator : public chameleon::event::listener {
			public:
				networkSubsystemDelegator(chameleon::event::manager *_manager);
				void ev_removeNetSubsystem(void *data);
				void ev_update(void *data);
			private:
				chameleon::event::manager *manager;
				list<server::network::networkSubsystem *> netSubsystems;
		};
	}
}
#endif
