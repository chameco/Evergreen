#ifndef LEVEL_H
#define LEVEL_H
//LIBRARY INCLUDES:
#include <string>
#include <map>
#include <vector>
//USER INCLUDES:
#include "chameleon.h"
#include "base/group.h"
namespace level {
	using namespace std;
	class level {
		public:
			level(chameleon::event::manager *_manager, int _index);
			string serialize();
			static level *load(string dump, chameleon::event::manager *_manager);
			void loadLevel();
		private:
			map<string, base::block *> *blocks;//Give base::block a clone method to instantiate new blocks.
			base::group *blockState;
			base::group *entityState;
			base::group *floorState;
			vector<int> *startCoords;
	};
}
#endif
