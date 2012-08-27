#ifndef BLOCK_H
#define BLOCK_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "base/physicalObject.h"
#include "base/drawnObject.h"
namespace base {
	using namespace std;
	class block : public base::physicalObject {
		public:
			block(vector<int> *_coords);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "block";}
	};
}
#endif
