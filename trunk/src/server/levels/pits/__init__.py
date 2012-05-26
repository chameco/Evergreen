from .... import chameleon
from .... import level
from .... import base
from . import floor1, floor2
class levelManager(level.levelManager):
    def __init__(self, manager):
        level.levelManager.__init__(self, manager)
        self.levels = [floor1.lvl(), floor2.lvl()]
