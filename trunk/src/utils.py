import errors
import os
import pygame
pygame.init()
def serializable(cls):
	try:
		if callable(cls.__dict__["serialize"]) and isinstance(cls.__dict__["load"], staticmethod):
			return cls
		else:
			raise errors.coreError("Methods serialize and load improperly defined.")
	except KeyError as e:
		raise errors.coreError("Methods serialize and load undefined.")
def loadLevelPack(name, manager):
	ns = {}
	exec("from levels." + name + " import *", ns, ns)
	print ns
	return [value.lvl(manager) for value in ns.values()]
def loadImage(pathname):
	i = pygame.image.load(os.path.join(os.path.abspath("."), pathname))
	i.set_colorkey((255, 0, 170))
	i.convert()
	return i