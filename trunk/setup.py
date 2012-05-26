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
    packages=["src", "src.server", "src.server.levels", "src.server.levels.test", "src.server.plugins", "src.client", "src.client.spritepacks", "src.client.spritepacks.default"],
    scripts=["runserver.py", "runclient.py"],
    package_dir={"src" : "src"},
    package_data={"src.server" : ["server.ini"], "src.client.spritepacks.default" : ["*.png"]},
    ext_modules = [Extension("src.chameleon", [join("src", "wrapper.cpp")], libraries=["boost_python-py27"])],
    data_files=["entity.db"],
    requires=["pygame"]
)
