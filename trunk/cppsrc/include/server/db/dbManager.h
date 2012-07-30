#ifndef DBMANAGER_H
#define DBMANAGER_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
namespace server {
	namespace db {
		using namespace std;
		class dbManager : public chameleon::event::listener {
			public:
				dbManager(chameleon::event::manager *_manager);
				void ev_fetchEntity(void *data);
				void ev_saveEntity(void *data);
			private:
				
		};
	}
}
#endif
