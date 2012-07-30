#ifndef GROUP_H
#define GROUP_H
//LIBRARY INCLUDES:
#include <string>
#include <list>
//USER INCLUDES:
#include "chameleon.h"
#include "base/physicalObject.h"
namespace base {
	using namespace std;
	class group {
		public:
			group();
			void add(base::physicalObject *object);
			void remove(base::physicalObject *object);
			string serialize();
			static group *load(string _dump);
		private:
			list<base::physicalObject *> intern;
	};
}
#endif
