#define PYTHON_BUILD
#include <boost/python.hpp>
#include "cham.h"
#include <string>
using namespace boost::python;
using namespace cham::event;
BOOST_PYTHON_MODULE(chameleon)
{
	class_<event>("event", init<std::string, boost::python::object>())
		.add_property("name", &event::getName, &event::setName)
		.add_property("data", &event::getData, &event::setData)
	;
	class_<python_manager>("manager", init<>())
		.def("alert", &python_manager::alert)
		.def("reg", &python_manager::reg)
		.def("cleanreg", &python_manager::cleanreg)
		.def("unregister", &python_manager::unregister)
	;
	class_<python_listener>("listener", init<>())
//		.def("alert", &python_listener::alert)
		.def("setResponse", &python_listener::setResponse)
		.def("setManager", &python_listener::setManager)
	;
}
