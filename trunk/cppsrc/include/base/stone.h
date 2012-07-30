#ifndef STONE_H
#define STONE_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "chameleon.h"
#include "base/block.h"
namespace base {
	using namespace std;
	class stone : public base::block {
		public:
			stone(vector<int> *_coords);
	};
}
#endif
