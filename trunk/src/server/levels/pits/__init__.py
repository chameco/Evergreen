from .... import level
from .... import base
from .... import randlev
from . import floor1, floor2
class levelManager(level.levelManager):
    def __init__(self, manager):
        level.levelManager.__init__(self, manager)
        self.levels = [floor1.lvl(manager, 0), floor2.lvl(manager, 1)]
