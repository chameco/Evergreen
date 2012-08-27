#ifndef IMAGE_H
#define IMAGE_H
//LIBRARY INCLUDES:
#include <string>
#include <vector>
#include "SDL/SDL.h"
#include "SDL/SDL_opengl.h"
//USER INCLUDES:
namespace base {
	using namespace std;
	class image {
		public:
			image(string name);
			void draw(vector<int> *coords, int scale = 1);
		private:
			GLuint texture;
			int width;
			int height;
	};
}
#endif
