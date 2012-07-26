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
from . import errors
import os
import sys
import chameleon
import pygame
import random
def serializable(cls):
    try:
        if callable(cls.__dict__["serialize"]) and isinstance(cls.__dict__["load"], staticmethod):
            return cls
        else:
            raise errors.coreError("Methods serialize and load improperly defined.")
    except KeyError as e:
        raise errors.coreError("Methods serialize and load undefined.")
def trace(func):
    if __debug__:
        def new(*args, **kwargs):
            log("enter " + func.__name__)
            func(*args, **kwargs)
            log("exit " + func.__name__)
        return new
    return func
def loadLevelPack(name, manager):
    ns = {}
    exec("from levels." + name + " import *", ns, ns)
    print ns
    return [value.lvl(manager) for value in ns.values()]
def loadImage(path):
    return pygame.image.load(path)
def sponge(*args):
    pass
class netEvent():
	def __init__(self, event):
		self.name = event.name
		self.data = event.data
	def __init__(self, name, data):
		self.name = name
		self.data = data
	def cham(self):
		return chameleon.event(self.name, self.data)
