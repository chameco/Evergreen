#ifndef PLAYER_H
#define PLAYER_H
//LIBRARY INCLUDES:
#include <string>
//USER INCLUDES:
#include "chameleon.h"
#include "base/entity.h"
namespace base {
	using namespace std;
	class player : public entity {
		public:
			player(vector<int> *_coords, map<string, string> *_data=NULL, chameleon::event::manager *_manager=NULL, int _curLevel=0);
			void update(base::group *allSprites);
			void hit(base::physicalObject *hitter);
		private:
			int wasjusthit;
			int prev;
	};
}
#endif
