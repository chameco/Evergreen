#ifndef BLOCK_H
#define BLOCK_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "base/physicalObject.h"
namespace base {
	using namespace std;
	class block : public base::physicalObject {
		public:
			block(vector<int> *_coords);
	};
}
#endif
