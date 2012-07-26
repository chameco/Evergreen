#Copyright 2011 Samuel Breese. Distributed under the terms of the GNU General Public License.
#This file is part of Evergreen.
#
#    Evergreen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Evergreen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Evergreen.  If not, see <http://www.gnu.org/licenses/>.
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
#^Cwwwww^#
#^      ^#
#^  <>  ^#
#^      ^#
#^      ^#
#^      ^#
#^      ^#
#^      ^#
#^^^^^^^^#
##########"""
        self.loadLevel()
