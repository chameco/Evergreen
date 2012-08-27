#include <boost/python.hpp>
#include <string>
#include <vector>
#include "base/drawnObject.h"
#include "base/physicalObject.h"
#include "base/block.h"
#include "base/stone.h"
#include "base/stairsUp.h"
#include "base/stairsDown.h"
#include "base/stairsWarp.h"
#include "base/floor.h"
#include "base/woodFloor.h"
#include "base/image.h"
#include "base/group.h"
#include "base/rect.h"
using namespace std;
using namespace boost::python;
BOOST_PYTHON_MODULE(chameleon) {
	class_<base::drawnObject>("drawnObject", init<vector<int> *>())
		.def("draw", &base::drawnObject::draw)
		.def("update", &base::drawnObject::update)
		.add_property("coords", &base::drawnObject::getCoords)
		.add_property("width", &base::drawnObject::getWidth)
		.add_property("height", &base::drawnObject::getHeight)
		.add_property("imgname", &base::drawnObject::getImgname, &base::drawnObject::setImgname)
		.def("getData", &base::drawnObject::getData)
		.def("setData", &base::drawnObject::setData)
	;
	class_<base::physicalObject, bases<base::drawnObject> >("physicalObject", init<vector<int> *>())
		.def("hit", &base::physicalObject::hit)
		.def("bump", &base::physicalObject::bump)
	;
	class_<base::block, bases<base::physicalObject> >("block", init<vector<int> *>())
	;
	class_<base::stone, bases<base::block> >("stone", init<vector<int> *>())
	;
	class_<base::stairsUp, bases<base::block> >("stairsUp", init<vector<int> *>())
		.def("hit", &base::stairsUp::hit)
	;
	class_<base::stairsDown, bases<base::block> >("stairsDown", init<vector<int> *>())
		.def("hit", &base::stairsDown::hit)
	;
	class_<base::stairsWarp, bases<base::block> >("stairsWarp", init<vector<int> *, int>())
		.def("hit", &base::stairsWarp::hit)
	;
	class_<base::floor, bases<base::drawnObject> >("floor", init<vector<int> *>())
	;
	class_<base::woodFloor, bases<base::floor> >("woodFloor", init<vector<int> *>())
	;
}
