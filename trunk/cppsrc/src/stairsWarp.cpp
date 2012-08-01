#include "base/stairsWarp.h"
using namespace std;
base::stairsWarp::stairsWarp(vector<int> *_coords, int _warp) : base::block(_coords) {
	imgname = "stairsWarp";
	warp = _warp;
}
void base::stairsWarp::hit(base::entity *hitter) {
	hitter->setCurLevel(warp);
	hitter->getManager()->alert("switchLevel", hitter);//Might need to cast this to void *
}
