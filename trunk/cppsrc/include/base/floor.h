#ifndef FLOOR_H
#define FLOOR_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "base/drawnObject.h"
namespace base {
	using namespace std;
	class floor : public base::drawnObject {
		public:
			floor(vector<int> *_coords);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "floor";}
	};
}
#endif
