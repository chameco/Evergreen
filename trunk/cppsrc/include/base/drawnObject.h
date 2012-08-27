#ifndef DRAWNOBJECT_H
#define DRAWNOBJECT_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
#include <cstdio>
#include <boost/serialization/string.hpp>
#include <boost/serialization/map.hpp>
#include <boost/serialization/vector.hpp>
#include <boost/python.hpp>
//USER INCLUDES:
#include "chameleon.h"
#include "base/image.h"
#include "base/group.h"
namespace base {
	using namespace std;
	class drawnObject {
		friend class boost::serialization::access;
		public:
			drawnObject(vector<int> *_coords);
			virtual drawnObject *clone() {return this;}
			virtual string getType() {return "drawnObject";}
			void draw(int scale=1);
			virtual void update(base::group<drawnObject> *allSprites) {}
			vector<int> getCoords() {return *coords;}
			int getWidth() {return width;}
			int getHeight() {return height;}
			string getImgname() {return imgname;}
			void setImgname(string _imgname) {imgname = _imgname;}
			string getData(string key) {return (*data)[key];}
			void setData(string key, string val) {(*data)[key] = val;}
		protected:
			map<string, string> *data;
			vector<int> *coords;
			int width;
			int height;
		private:
			template<class Archive>
			void serialize(Archive &ar, const unsigned int version);
			string imgname;//For loading client-side.
			base::image *image;
	};
}
#endif
