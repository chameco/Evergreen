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
    scripts=["evg_client", "evg_server"],
    package_dir={"src" : "src"},
    package_data={"src.server" : ["server.ini"], "src.client" : ["client.ini"], "src.client.spritepacks.default" : ["*.png"]},
    data_files=["entity.db"],
    install_requires=["pygame>=1.9"],
    dependency_links=["http://www.pygame.org/download.shtml"]
)
