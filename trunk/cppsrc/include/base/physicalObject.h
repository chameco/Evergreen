#ifndef PHYSICALOBJECT_H
#define PHYSICALOBJECT_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "base/drawnObject.h"
#include "base/entity.h"
namespace base {
	using namespace std;
	class physicalObject : public base::drawnObject {
		public:
			physicalObject(vector<int> *_coords):
			virtual void hit(base::entity *hitter) =0;
			virtual void bump(base::entity *bumper) =0;
	};
}
#endif
