#ifndef RECT_H
#define RECT_H
//LIBRARY INCLUDES:
#include <string>
#include <list>
//USER INCLUDES:
#include "base/group.h"
#include "base/physicalObject.h"
namespace base {
	using namespace std;
	class rect {
		public:
			rect(int _x, int _y, int _w, int _h);
			list<base::physicalObject *> *collideGroup(base::group<base::physicalObject> *group);
			bool overlaps(rect *other);
			int getX() {return x;}
			int getY() {return y;}
			int getW() {return w;}
			int getH() {return h;}
		private:
			int x;
			int y;
			int w;
			int h;
	};
}
#endif

