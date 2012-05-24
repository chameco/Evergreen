from .... import utils
import os
import pygame
pygame.init()
pygame.display.set_mode()
PATH = "src/client/spritepacks/default"
IMAGES = {
"red" : utils.loadImage(os.path.join(PATH, "red.png")),
"stone" : utils.loadImage(os.path.join(PATH, "stone.png")),
}
ENTITYIMAGES = {
"entity" : ((utils.loadImage(os.path.join(PATH, "playerb.png")), utils.loadImage(os.path.join(PATH, "playerba.png"))), (utils.loadImage(os.path.join(PATH, "playerf.png")), utils.loadImage(os.path.join(PATH, "playerfa.png"))), (utils.loadImage(os.path.join(PATH, "playerl.png")), utils.loadImage(os.path.join(PATH, "playerla.png"))), (utils.loadImage(os.path.join(PATH, "playerr.png")), utils.loadImage(os.path.join(PATH, "playerra.png")))),
"Scarecrow" : ((utils.loadImage(os.path.join(PATH, "Scarecrow.png")),), None, None, None, (utils.loadImage(os.path.join(PATH, "red.png")),)),
}
def getImage(name):
    return IMAGES[name]
def getEntityImage(name):
    return ENTITYIMAGES[name]
def hasEntityImage(name):
    return name in ENTITYIMAGES
