#include "base/stone.h"
using namespace std;
base::stone::stone(vector<int> *_coords) : base::block(_coords) {
	setImgname("stone");
}
