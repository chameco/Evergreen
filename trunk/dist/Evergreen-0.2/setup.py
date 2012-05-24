from distutils.core import setup
from os.path import join
import os
os.chdir("src")
os.system("bjam")
os.chdir("..")
setup(
	name="Evergreen",
	version="0.2",
	packages=["src", "src.server", "src.server.levels", "src.server.levels.test", "src.server.plugins", "src.client", "src.client.spritepacks", "src.client.spritepacks.default"],
	scripts=["runserver.py", "runclient.py"],
	package_dir={"src" : "src"},
	package_data={"src" : ["chameleon.so"], "src.server" : ["server.ini"], "src.client.spritepacks.default" : ["*.png"]},
	data_files=["entity.db"]
)
