#ifndef STAIRSUP_H
#define STAIRSUP_H
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
	class stairsUp : public base::block {
		public:
			stairsUp(vector<int> *_coords);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "stairsUp";}
			void hit(base::entity *hitter);
	};
}
#endif
