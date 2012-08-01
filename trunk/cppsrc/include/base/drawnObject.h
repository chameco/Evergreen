#ifndef DRAWNOBJECT_H
#define DRAWNOBJECT_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
#include <cstdio>
#include <boost/serialization/string.h>
#include <boost/serialization/map.h>
#include <boost/serialization/vector.h>
//USER INCLUDES:
#include "chameleon.h"
#include "base/image.h"
namespace base {
	using namespace std;
	class drawnObject {
		public:
			drawnObject(vector<int> *_coords);
			template<class Archive>
			virtual void serialize(Archive &ar, const unsigned int version);
			void draw(int scale=1);
			virtual void update(base::group *allSprites) =0;
		private:
			string imgname;//For loading client-side.
			vector<int> *coords;
			int width;
			int height;
			base::image *image;
			map<string, string> *data;
	};
}
#endif
