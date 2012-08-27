#ifndef STAIRSDOWN_H
#define STAIRSDOWN_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "chameleon.h"
#include "base/block.h"
#include "base/physicalObject.h"
#include "base/drawnObject.h"
#include "base/entity.h"
namespace base {
	using namespace std;
	class stairsDown : public base::block {
		public:
			stairsDown(vector<int> *_coords);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "stairsDown";}
			void hit(base::entity *hitter);
	};
}
#endif
