#include "base/player.h"
using namespace std;
base::player::player(vector<int> *_coords, map<string, string> *_data=NULL, chameleon::event::manager *_manager=NULL, int _curLevel=0) : base::entity(_coords, _data, _manager, _curLevel) {
	wasjusthit = 0;
	prev = "up";
}
void base::player::update(base::group *allSprites) {
	entity.update(self, allSprites)
	if (wasjusthit == 2) {
		prev = data["facing"];
		data["facing"] = "red";
		wasjusthit = 1;
		manager->alert("entityMoved", this);
	}
	else if (wasjusthit == 1) {
		data["facing"] = prev;
		wasjusthit = 0;
		manager->alert("entityMoved", this)
	}
	if (data["health"] <= 0) {
		manager->alert("killEntity", this);
		manager->alert("gameOver", this);
	}
}

void base::player::hit(base::entity *hitter) {
	wasjusthit = 2;
	data["health"] -= hitter->getAttr("attack");
}
