#ifndef STAIRSWARP_H
#define STAIRSWARP_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "chameleon.h"
#include "base/block.h"
#include "base/physicalObject.h"
namespace base {
	using namespace std;
	class stairsWarp : public base::block {
		public:
			stairsWarp(vector<int> *_coords, vector<int> *_warp);
			void hit(base::physicalObject *hitter);
		private:
			vector<int> *warp;
	};
}
#endif
