#ifndef ENTITY_H
#define ENTITY_H
//LIBRARY INCLUDES:
#include <cstddef>
#include <string>
#include <vector>
#include <map>
//USER INCLUDES:
#include "chameleon.h"
#include "base/physicalObject.h"
namespace base {
	using namespace std;
	class entity : public base::physicalObject {
		public:
			entity(vector<int> *_coords, map<string, string> *_data=NULL, chameleon::event::manager *_manager=NULL, int _curLevel=0);
			void moveup(bool down);
			void movedown(bool down);
			void moveleft(bool down);
			void moveright(bool down);
			void attack(base::group *allSprites);
			void update(base::group *allSprites);
		private:
			static amountCreated;
			chameleon::event::manager *manager;
			int curlevel;
			int requestx;
			int requesty;
			map<string, int> attrs;
	};
}
#endif
