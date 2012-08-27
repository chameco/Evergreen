from . import pit
from .... import level
from .... import base
class lvl(level.level):
    def __init__(self, manager, index):
        level.level.__init__(self, manager, index)
        self.blocks["#"] = base.stone
        self.blocks["^"] = pit.pittooth
        self.blocks[">"] = base.stairsDown
        self.blocks["<"] = base.stairsUp
        self.blocks["w"] = base.woodFloor
        self.levelimp = """\
##########
#^^^^^^^^#
#^C     ^#
#^      ^#
#^  >^  ^#
#^      ^#
#^      ^#
#^      ^#
#^      ^#
#^      ^#
#^^^^^^^^#
##########"""
        self.loadLevel()
