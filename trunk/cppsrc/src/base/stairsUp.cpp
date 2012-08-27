#include "base/stairsUp.h"
using namespace std;
base::stairsUp::stairsUp(vector<int> *_coords) : base::block(_coords) {
	setImgname("stairsUp");
}
void base::stairsUp::hit(base::entity *hitter) {
	hitter->setCurLevel(hitter->getCurLevel() - 1); //Visualize the list of levels as extending downward, starting at 0
	hitter->getManager()->alert("switchLevel", hitter);//Might need to cast this to void *
}
