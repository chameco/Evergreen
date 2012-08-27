#ifndef STAIRSWARP_H
#define STAIRSWARP_H
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
	class stairsWarp : public base::block {
		public:
			stairsWarp(vector<int> *_coords, int _warp);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "stairsWarp";}
			void hit(base::entity *hitter);
		private:
			int warp;
	};
}
#endif
