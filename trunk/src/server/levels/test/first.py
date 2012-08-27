from .... import level
from .... import base
class lvl(level.level):
    def __init__(self):
        level.level.__init__(self)
        self.levelimp = """\
##########        #########
#        #        #       #
#        ##########       #
#                         #
#        ##########       #
#        #        #       #
##########        #########"""
        self.loadLevel()
        #self.entityState.add(Scarecrow(tuple([200, 200])))
