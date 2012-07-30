#ifndef STAIRSDOWN_H
#define STAIRSDOWN_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "chameleon.h"
#include "base/block.h"
#include "base/physicalObject.h"
namespace base {
	using namespace std;
	class stairsDown : public base::block {
		public:
			stairsDown(vector<int> *_coords);
			void hit(base::physicalObject *hitter);
	};
}
#endif
