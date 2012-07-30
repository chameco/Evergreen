#ifndef STAIRSUP_H
#define STAIRSUP_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "chameleon.h"
#include "base/block.h"
#include "base/physicalObject.h"
namespace base {
	using namespace std;
	class stairsUp : public base::block {
		public:
			stairsUp(vector<int> *_coords);
			void hit(base::physicalObject *hitter);
	};
}
#endif
