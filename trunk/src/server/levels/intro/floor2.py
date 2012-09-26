from .... import level
from .... import base
class lvl(level.level):
    def __init__(self, manager, index):
        level.level.__init__(self, manager, index)
        self.blocks["#"] = base.stone
        self.blocks[">"] = base.stairsDown
        self.blocks["<"] = base.stairsUp
        self.blocks["w"] = base.woodFloor
        self.levelimp = """\
############
#          #
#       C  #
#   ?  ><  #
#          #
#          #
#          #
#          #
#          #
#          #
#          #
############"""
        self.messageBox = base.messageBox((3 * 32, 3 * 32), self.index)
        self.messageBox.msg = """\
The green portal moves you up a floor. Go down once more."""
        self.blockState.add(self.messageBox)
        self.loadLevel()
