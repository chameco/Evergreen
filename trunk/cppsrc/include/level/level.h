#ifndef LEVEL_H
#define LEVEL_H
//LIBRARY INCLUDES:
#include <string>
#include <map>
#include <vector>
//USER INCLUDES:
#include "chameleon.h"
#include "base/block.h"
#include "base/group.h"
#include "base/floor.h"
namespace level {
	using namespace std;
	class level {
		public:
			level(chameleon::event::manager *_manager, int _index);
			~level();
			base::group<base::physicalObject> *getBlockState() {return new base::group<base::physicalObject>(*blockState);}
			base::group<base::physicalObject> *getEntityState() {return new base::group<base::physicalObject>(*entityState);}
			base::group<base::physicalObject> *getFloorState() {return new base::group<base::floor>(*floorState);}
			void loadLevel();
		private:
			chameleon::event::manager *manager;
			int index;
			map<string, base::block *> *blocks;//Give base::block a clone method to instantiate new blocks.
			base::group<base::physicalObject> *blockState;
			base::group<base::physicalObject> *entityState;
			base::group<base::floor> *floorState;
			vector<int> *startCoords;
			string levelImp;
	};
}
#endif
