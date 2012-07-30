#ifndef PHYSICALOBJECT_H
#define PHYSICALOBJECT_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "base/drawnObject.h"
namespace base {
	using namespace std;
	class physicalObject : public base::drawnObject {
		public:
			physicalObject(vector<int> *_coords):
			virtual void hit(physicalObject *hitter) const=0;
			virtual void bump(physicalObject *bumper) const=0;
	};
}
#endif
