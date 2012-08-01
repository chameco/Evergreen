#ifndef ENTITY_H
#define ENTITY_H
//LIBRARY INCLUDES:
#include <cstddef>
#include <string>
#include <vector>
#include <map>
#include <boost/lexical_cast.hpp>
//USER INCLUDES:
#include "chameleon.h"
#include "base/physicalObject.h"
namespace base {
	using namespace std;
	class entity : public base::physicalObject {
		static int amountCreated = 0;
		public:
			entity(vector<int> *_coords, map<string, string> *_data=NULL, chameleon::event::manager *_manager=NULL, int _curLevel=0);
			void moveup(bool down);
			void movedown(bool down);
			void moveleft(bool down);
			void moveright(bool down);
			void attack(base::group *allSprites);
			void update(base::group *allSprites);
			chameleon::event::manager *getManager() {return manager;}
			void setCurLevel(int _curLevel) {curLevel = _curLevel;}
			int getAttr(string key) {return attrs[key];}
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
