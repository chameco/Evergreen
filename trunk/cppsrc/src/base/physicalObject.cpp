#include "base/physicalObject.h"
using namespace std;
base::physicalObject::physicalObject(vector<int> *_coords) : base::drawnObject(_coords) {}
template<class Archive>
void base::physicalObject::serialize(Archive &ar, const unsigned int version) {
	ar & boost::serialization::base_object<base::drawnObject>(*this);
}
