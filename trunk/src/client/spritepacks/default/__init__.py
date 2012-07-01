from .... import utils
import os
import pygame
IMAGES = {}
ENTITYIMAGES = {}
def loadImages():
    pygame.init()
    global IMAGES
    global ENTITYIMAGES
    PATH = "src/client/spritepacks/default"
    IMAGES = {
    "red" : utils.loadImage(os.path.join(PATH, "red.png")),
    "up" : utils.loadImage(os.path.join(PATH, "up.png")),
    "down" : utils.loadImage(os.path.join(PATH, "down.png")),
    "warp" : utils.loadImage(os.path.join(PATH, "warp.png")),
    "stone" : utils.loadImage(os.path.join(PATH, "stone.png")),
    "woodFloor" : utils.loadImage(os.path.join(PATH, "woodfloor.png")),
    "pitwall" : utils.loadImage(os.path.join(PATH, "pitwall.png")),
    }
    ENTITYIMAGES = {
    "entity" : ((utils.loadImage(os.path.join(PATH, "playerb.png")), utils.loadImage(os.path.join(PATH, "playerba.png"))), (utils.loadImage(os.path.join(PATH, "playerf.png")), utils.loadImage(os.path.join(PATH, "playerfa.png"))), (utils.loadImage(os.path.join(PATH, "playerl.png")), utils.loadImage(os.path.join(PATH, "playerla.png"))), (utils.loadImage(os.path.join(PATH, "playerr.png")), utils.loadImage(os.path.join(PATH, "playerra.png")))),
    "pittooth" : ((utils.loadImage(os.path.join(PATH, "pittooth.png")), IMAGES["stone"]), (IMAGES["stone"], IMAGES["stone"]), (IMAGES["stone"], IMAGES["stone"]), (IMAGES["stone"], IMAGES["stone"]), (utils.loadImage(os.path.join(PATH, "red.png")), IMAGES["stone"])),
    }
def getImage(name):
    return IMAGES[name]
def getEntityImage(name):
    return ENTITYIMAGES[name]
def hasEntityImage(name):
    return name in ENTITYIMAGES
