#include "base/drawnObject.cpp"
using namespace std;
base::drawnObject::drawnObject(vector<int> *_coords) {
	coords = _coords;
	width = 32;
	height = 32;
}

void base::drawnObject::draw(int scale) {
	image->draw(coords, scale);
}

template<class Archive>
void base::drawnObject::serialize(Archive &ar, const unsigned int version) {
	ar & coords;
	ar & width;
	ar & height;
	ar & data;
}
