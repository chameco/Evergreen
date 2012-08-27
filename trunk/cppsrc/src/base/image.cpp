#include "base/image.h"
using namespace std;
base::image::image(string name) {
	SDL_Surface *surface;	// This surface will tell us the details of the image
	GLenum texture_format;
	GLint nOfColors;
 
	if ((surface = SDL_LoadBMP(name.c_str()))) { 

		// Check that the image's width is a power of 2
		if ((surface->w & (surface->w - 1)) != 0) {
			printf("warning: %s's width is not a power of 2\n", name.c_str());
		}

		// Also check if the height is a power of 2
		if ((surface->h & (surface->h - 1)) != 0) {
			printf("warning: %s's height is not a power of 2\n", name.c_str());
		}

		width = surface->w;
		height = surface->h;

	    // get the number of channels in the SDL surface
		nOfColors = surface->format->BytesPerPixel;
		if (nOfColors == 4) {
			if (surface->format->Rmask == 0x000000ff)
				texture_format = GL_RGBA;
			else
				texture_format = GL_BGRA;
		}
		else if (nOfColors == 3) {
			if (surface->format->Rmask == 0x000000ff) {
				texture_format = GL_RGB;
			}
			else {
				texture_format = GL_BGR;
			}
        }
		else {
			printf("warning: the image is not truecolor..  this will probably break\n");
			// this error should not go unhandled
		}

		// Have OpenGL generate a texture object handle for us
		glGenTextures(1, &texture);

		// Bind the texture object
		glBindTexture(GL_TEXTURE_2D, texture);

		// Set the texture's stretching properties
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

		// Edit the texture object's image data using the information SDL_Surface gives us
		glTexImage2D(GL_TEXTURE_2D, 0, nOfColors, surface->w, surface->h, 0,
						texture_format, GL_UNSIGNED_BYTE, surface->pixels);
	}
	else {
		printf("SDL could not load image.bmp: %s\n", SDL_GetError());
		SDL_Quit();
		exit(1);
	}

	// Free the SDL_Surface only if it was successfully created
	if (surface) { 
		SDL_FreeSurface(surface);
	}
}
void base::image::draw(vector<int> *coords, int scale) {
	int texwidth = width * scale;
	int texheight = height * scale;
	glBindTexture(GL_TEXTURE_2D, texture);
	glBegin(GL_QUADS);
		glTexCoord2i(0, 0);
		glVertex3f(coords->at(0), coords->at(1), 0);
		glTexCoord2i(1, 0);
		glVertex3f(coords->at(0) + texwidth, coords->at(1), 0);
		glTexCoord2i(1, 1);
		glVertex3f(coords->at(0) + texwidth, coords->at(1) + texheight, 0);
		glTexCoord2i(0, 1);
		glVertex3f(coords->at(0), coords->at(1) + texheight, 0);
	glEnd();
}
