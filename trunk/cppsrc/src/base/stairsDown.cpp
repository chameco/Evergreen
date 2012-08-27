#include "base/stairsDown.h"
using namespace std;
base::stairsDown::stairsDown(vector<int> *_coords) : base::block(_coords) {
	setImgname("stairsDown");
}
void base::stairsDown::hit(base::entity *hitter) {
	hitter->setCurLevel(hitter->getCurLevel() + 1);
	hitter->getManager()->alert("switchLevel", hitter);//Might need to cast this to void *
}
