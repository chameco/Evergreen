#ifndef SPINNER_H
#define SPINNER_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
namespace server {
	using namespace std;
	class spinner  : public chameleon::event::manager {
		public:
			spinner();
			void main();
		private:
			level::levelManager *levelManager;
			server::db::dbManager *dbManager;
			server::networkSubsystemDelegator *netSubDelegator;
	};
}
#endif
