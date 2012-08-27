#ifndef WOODFLOOR_H
#define WOODFLOOR_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "base/floor.h"
#include "base/drawnObject.h"
namespace base {
	using namespace std;
	class woodFloor : public base::floor {
		public:
			woodFloor(vector<int> *_coords);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "woodFloor";}
	};
}
#endif
