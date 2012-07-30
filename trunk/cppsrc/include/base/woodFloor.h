#ifndef WOODFLOOR_H
#define WOODFLOOR_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "base/floor.h"
namespace base {
	using namespace std;
	class woodFloor : public base::floor {
		public:
			woodFloor(vector<int> *_coords);
	};
}
#endif
