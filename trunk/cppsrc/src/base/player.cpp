#include "base/player.h"
using namespace std;
base::player::player(vector<int> *_coords, map<string, string> *_data, chameleon::event::manager *_manager, int _curLevel) : base::entity(_coords, _data, _manager, _curLevel) {
	wasjusthit = 0;
	prev = "up";
}
void base::player::update(base::group<base::physicalObject> *allSprites) {
	base::entity::update(allSprites);
	if (wasjusthit == 2) {
		prev = (*data)["facing"];
		(*data)["facing"] = "red";
		wasjusthit = 1;
		manager->alert("entityMoved", this);
	}
	else if (wasjusthit == 1) {
		(*data)["facing"] = prev;
		wasjusthit = 0;
		manager->alert("entityMoved", this);
	}
	if (boost::lexical_cast<int>((*data)["health"]) <= 0) {
		manager->alert("killEntity", this);
		manager->alert("gameOver", this);
	}
}

void base::player::hit(base::physicalObject *hitter) {
	wasjusthit = 2;
	(*data)["health"] = boost::lexical_cast<string>(boost::lexical_cast<int>((*data)["health"]) - boost::lexical_cast<int>(dynamic_cast<base::entity *>(hitter)->getAttr("attack")));
}
