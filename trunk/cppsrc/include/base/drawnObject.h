#ifndef DRAWNOBJECT_H
#define DRAWNOBJECT_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
//USER INCLUDES:
#include "chameleon.h"
namespace base {
	using namespace std;
	class drawnObject {
		public:
			drawnObject(vector<int> *_coords);
			void draw(int scale=1);
			string serialize();
			drawnObject *load(string dump);
			drawnObject *load(string dump, chameleon::event::manager *_manager);
			virtual void update(base::group *allSprites) const=0;
		private:
			string imgname;//For loading client-side.
			vector<int> *coords;
			int width;
			int height;
			FIXME_OPENGL_TEXTURE_TYPE image;
			map<string, string> *data;
	};
}
#endif
