#include "base/rect.h"
using namespace std;
base::rect::rect(int _x, int _y, int _w, int _h) {
	x = _x;
	y = _y;
	w = _w;
	h = _h;
}
list<base::physicalObject *> *base::rect::collideGroup(base::group<base::physicalObject> *group) {
	list<base::physicalObject *> *contents = group->getList();
	list<base::physicalObject *> *r = new list<base::physicalObject *>();
	vector<int> coords;
	for (list<base::physicalObject *>::iterator i = contents->begin(); i != contents->end(); i++) {
		coords = (*i)->getCoords();
		base::rect temp = base::rect(coords[0], coords[1], (*i)->getWidth(), (*i)->getHeight());
		if (temp.overlaps(this)) {
			r->push_back(*i);
		}
	}
	delete contents;
	return r;
}
bool base::rect::overlaps(base::rect *other) {
	int ox, oy, ow, oh;
	ox = other->getX();
	oy = other->getY();
	ow = other->getW();
	oh = other->getH();
	if (((ox >= x) && (ox <= x+w)) && ((oy >= y) && (oy <= y+h))) return true;
	if (((ox+ow >= x) && (ox+ow <= x+w)) && ((oy >= y) && (oy <= y+h))) return true;
	if (((ox >= x) && (ox <= x+w)) && ((oy+oh >= y) && (oy+oh <= y+h))) return true;
	if (((ox+ow >= x) && (ox+ow <= x+w)) && ((oy+oh >= y) && (oy+oh <= y+h))) return true;
}
