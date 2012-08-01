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
			template<class Archive>
			virtual void serialize(Archive &ar, const unsigned int version);
			void add(base::drawnObject *object);
			void remove(base::drawnObject *object);
		private:
			list<base::drawnObject *> intern;
	};
}
#endif
