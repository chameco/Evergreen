#include "base/stairsDown.h"
using namespace std;
base::stairsDown::stairsDown(vector<int> *_coords) : base::block(_coords) {
	imgname = "stairsUp";
}
void base::stairsDown::hit(base::entity *hitter) {
	hitter->curLevel += 1;
	hitter->getManager()->alert("switchLevel", hitter);//Might need to cast this to void *
}
