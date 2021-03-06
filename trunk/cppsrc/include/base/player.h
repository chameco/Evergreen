#ifndef PLAYER_H
#define PLAYER_H
//LIBRARY INCLUDES:
#include <string>
#include <boost/lexical_cast.hpp>
//USER INCLUDES:
#include "chameleon.h"
#include "base/entity.h"
#include "base/physicalObject.h"
#include "base/drawnObject.h"
namespace base {
	using namespace std;
	class player : public entity {
		public:
			player(vector<int> *_coords, map<string, string> *_data=NULL, chameleon::event::manager *_manager=NULL, int _curLevel=0);
			virtual base::drawnObject *clone() {return this;}
			virtual string getType() {return "player";}
			void update(base::group<base::physicalObject> *allSprites);
			void hit(base::physicalObject *hitter);
		private:
			int wasjusthit;
			string prev;
	};
}
#endif
