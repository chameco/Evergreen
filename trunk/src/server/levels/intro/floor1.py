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
#       www#
#          #
#  ?    >  #
#          #
#          #
#          #
#    C     #
#          #
#          #
#          #
############"""
        self.messageBox = base.messageBox((3 * 32, 3 * 32), self.index)
        self.messageBox.msg = """\
Welcome to Evergreen!
You probably already know the controls if you managed
to hit the block, but here goes nothing:
WASD - Move
Space - Attack/Interact
And that's it. This is really the most redundant help
message ever, as in order to see it you need the information
that it contains. Maybe later we can have nicer things.
Anyway, try walking over to the down portal (the red portal
orb thing) and interacting with it."""
        self.blockState.add(self.messageBox)
        self.loadLevel()
