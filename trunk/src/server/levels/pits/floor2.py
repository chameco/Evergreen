from . import pit
from .... import level
from .... import base
class lvl(level.level):
    def __init__(self):
        level.level.__init__(self)
        self.startcoords = (250, 150)
        self.blocks["#"] = pit.pitwall
        self.blocks["^"] = pit.pittooth
        self.blocks[">"] = base.stairsDown
        self.blocks["<"] = base.stairsUp
        self.levelimp = """\
##########
#^^^^^^^^#
#^      ^#
#^      ^#
#^  <>  ^#
#^      ^#
#^      ^#
#^      ^#
#^^^^^^^^#
##########"""
        self.loadLevel()
