from .... import level
class lvl(level.level):
	def __init__(self, manager):
		level.level.__init__(self, manager)
		self.levelimp = """
##########
#        #
#        #
#        #
#        #
#        #
##########
"""
		self.loadLevel()
