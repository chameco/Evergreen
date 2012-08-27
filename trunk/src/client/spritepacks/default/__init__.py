from .... import utils
from ...gloss import *
import os
import pygame
IMAGES = {}
ENTITYIMAGES = {}
PATH = "src/client/spritepacks/default"
def loadImages():
    pygame.init()
    global IMAGES
    global ENTITYIMAGES
    IMAGES = {
    "red" : textureLoad("red.png"),
    "up" : textureLoad("up.png"),
    "down" : textureLoad("down.png"),
    "warp" : textureLoad("warp.png"),
    "stone" : textureLoad("stone.png"),
    "woodFloor" : textureLoad("woodfloor.png"),
    "pitwall" : textureLoad("pitwall.png"),
    }
    ENTITYIMAGES = {
    "entity" : ((textureLoad("playerb.png"), textureLoad("playerba.png")), (textureLoad("playerf.png"), textureLoad("playerfa.png")), (textureLoad("playerl.png"), textureLoad("playerla.png")), (textureLoad("playerr.png"), textureLoad("playerra.png")), (textureLoad("red.png"), textureLoad("red.png"))),
    "pittooth" : ((textureLoad("pittooth.png"), None), (None, None), (None, None), (None, None), (textureLoad("red.png"), None)),
    }
def getImage(name):
    return IMAGES[name]
def getEntityImage(name):
    return ENTITYIMAGES[name]
def hasEntityImage(name):
    return name in ENTITYIMAGES
def textureLoad(name):
    image = utils.loadImage(os.path.join(PATH, name))
    return Texture(image)
