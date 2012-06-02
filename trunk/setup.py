#Copyright 2011 Samuel Breese. Distributed under the terms of the GNU General Public License.
#This file is part of Evergreen.
#
#    Evergreen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Evergreen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Evergreen.  If not, see <http://www.gnu.org/licenses/>.
from setuptools import setup, Extension
from os.path import join
import os
setup(
    name="Evergreen",
    version="0.2",
    description="An event-driven 2D game engine written in Python and C++.",
    author="Samuel Breese",
    author_email="sbreese@xitol.net",
    url="https://github.com/chameco/Evergreen",
    license="GNU General Public License",
    packages=["src", "src.server", "src.server.levels", "src.server.levels.test", "src.server.plugins", "src.client", "src.client.spritepacks", "src.client.spritepacks.default"],
    scripts=["runserver.py", "runclient.py"],
    package_dir={"src" : "src"},
    package_data={"src.server" : ["server.ini"], "src.client.spritepacks.default" : ["*.png"]},
    #ext_modules = [Extension("src.chameleon", [join("src", "wrapper.cpp")], libraries=["boost_python-py27"])],
    data_files=["entity.db"],
    install_requires=["pygame>=1.9", "ev-chameleon>=1.0"],
    dependency_links=["http://www.pygame.org/download.shtml"]
)
