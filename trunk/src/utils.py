from . import errors
import os
import sys
import pygame
pygame.init()
LOGNAME = sys.argv[0] + ".log"
PREVLOG = []
INDENTLEVEL = 0
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
    t = pygame.image.load(path).convert()
    t.set_colorkey((255, 0, 170))
    return t
def log(string):
    global INDENTLEVEL
    if string not in PREVLOG:
        PREVLOG.append(string)
        log = open(LOGNAME, "w")
        log.write(("=" * INDENTLEVEL) + string + "\n")
        log.close()
        if string.split(" ")[0] == "enter":
            INDENTLEVEL += 1
        else:
            INDENTLEVEL -= 1
def sponge(*args):
    pass
