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
		friend class boost::serialization::access;
		public:
			physicalObject(vector<int> *_coords);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "physicalObject";}
			virtual void hit(physicalObject *hitter) {}
			virtual void bump(physicalObject *bumper) {}
		private:
			template<class Archive>
			void serialize(Archive &ar, const unsigned int version);
	};
}
#endif
