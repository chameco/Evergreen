#include "base/entity.h"
using namespace std;
base::entity::entity(vector<int> *_coords, map<string, string> *_data, chameleon::event::manager *_manager, int _curLevel) : base::physicalObject(_coords) {
	data = _data;
	if (data == NULL) {
		data = new map<string, string>();
		data["facing"] = "up";
		data["name"] = getType() + boost::lexical_cast<string>(amountCreated);
	}
	manager =_manager; //Manager is only used serverside.
	curLevel = _curLevel;
	requestx = 0;
	requesty = 0;
	attrs["speed"] = 8;
	attrs["attack"] = 1;
	imgname = "entity";
}
void base::entity::moveup(bool down) {
	if (down) {
		data["facing"] = "up";
		requesty = -1 * attrs["speed"];
	}
	else {
		requesty = (requesty <= -1) ? 0 : requesty;
	}
}
void base::entity::movedown(bool down) {
	if (down) {
		data["facing"] = "down";
		requesty = attrs["speed"];
	}
	else {
		requesty = (requesty >= 1) ? 0 : requesty;
	}
}
void base::entity::moveleft(bool down) {
	if (down) {
		data["facing"] = "left";
		requestx = -1 * attrs["speed"];
	}
	else {
		requestx = (requestx <= -1) ? 0 : requestx;
	}
}
void base::entity::moveright(bool down) {
	if (down) {
		data["facing"] = "right";
		requestx = attrs["speed"];
	}
	else {
		requestx = (requestx >= 1) ? 0 : requestx;
	}
}
void base::entity::attack(base::group *allSprites) {
	base::rect *collider;
	if (data["facing"] == "up") {
		collider = new base::rect(coords[0] + 8, coords[1] - 16, 16, 16);
	}
	else if (data["facing"] == "down") {
		collider = new base::rect(coords[0] + 8, coords[1] + height + 16, 16, 16);
	}
	else if (data["facing"] == "left") {
		collider = new base::rect(coords[0] - 16, coords[1] + 8, 16, 16);
	}
	else if (data["facing"] == "right") {
		collider = new base::rect(coords[0] + width + 16, coords[1] + 8, 16, 16);
	}
	list<base::physicalObject *> *sl = collider->collideGroup(allSprites)
	delete collider;
	for (list<base::physicalObject *>::iterator it = sl->begin(); it != sl->end(); it++) {
		(*it)->hit(this);
	}
	delete sl;
}
void base::entity::update(base::group *allSprites) {
	int temprequestx = requestx;
	int temprequesty = requesty;
	base::group *notMe = new base::group(*allSprites);//Might not work, trying to make a shallow copy.
	notMe->remove(this);
	list<base::physicalObject *> *bumped = new list<base::physicalObject *>();
	base::rect *xcollider = new base::rect(coords[0] + temprequestx, coords[1], width, height);
	list<base::physicalObject *> *x = xcollider->collideGroup(notMe);
	if (x->size()) {
		temprequestx = 0
		bumped->insert(bumped->end(), x->begin(), x->end());
	}
	base::rect *ycollider = new base::rect(coords[0], coords[1] + temprequesty, width, height);
	list<base::physicalObject *> *y = ycollider->collideGroup(notMe);
	if (y->size()) {
		temprequesty = 0
		bumped->insert(bumped->end(), y->begin(), y->end());
	}
	coords[0] += temprequestx;
	coords[1] += temprequesty;
	if (temprequestx || temprequesty) {
		manager->alert("entityMoved", this);
	}
	for (list<base::physicalObject *>::iterator it = bumped->begin(); it != bumped->end(); it++) {
		(*it)->bump(self)
	}
}
