#ifndef GROUP_H
#define GROUP_H
//LIBRARY INCLUDES:
#include <string>
#include <list>
#include <boost/serialization/list.hpp>
//USER INCLUDES:
#include "chameleon.h"
namespace base {
	using namespace std;
	template<class T>
	class group {
		friend class boost::serialization::access;
		public:
			group();
			group(group *copy);
			~group();
			void add(T *object);
			void remove(T *object);
			list<T *> *getList();
		private:
			template<class Archive>
			void serialize(Archive &ar, const unsigned int version);
			list<T *> intern;
	};
}
#endif
