/*
 * Copyright 2011 Samuel Breese. Distributed under the terms of the GNU General Public License.
 * This file is part of Evergreen.
 *
 *    Evergreen is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    Evergreen is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with Evergreen.  If not, see <http://www.gnu.org/licenses/>.
 */
#include <boost/python.hpp>
using namespace boost::python;
int main(int argc, char **argv) {
	try {
		Py_SetProgramName(argv[0]);
		Py_Initialize();
		object main_module = import("__main__");
		object main_namespace = main_module.attr("__dict__");
		exec("import sys; sys.path.append('.');", main_namespace);
		exec("from src.server import server", main_namespace);
		exec("server.run()", main_namespace);
	}
	catch(error_already_set const &) {
		PyErr_Print();
	}
}
