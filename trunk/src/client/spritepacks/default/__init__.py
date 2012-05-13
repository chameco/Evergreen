from .... import utils
import os
import pygame
pygame.init()
pygame.display.set_mode()
PATH = "src/client/spritepacks/default"
IMAGES = {
"stone" : utils.loadImage(os.path.join(PATH, "stone.png")),
}
CHARIMAGES = {}
def getImage(name):
	return IMAGES[name]
def getCharImage(name):
	if name in CHARIMAGES.keys():
		pass
	else:
		CHARIMAGES[name] = ((utils.loadImage(os.path.join(PATH, "playerf.png")), utils.loadImage(os.path.join(PATH, "playerfa.png"))), (utils.loadImage(os.path.join(PATH, "playerb.png")), utils.loadImage(os.path.join(PATH, "playerba.png"))), (utils.loadImage(os.path.join(PATH, "playerl.png")), utils.loadImage(os.path.join(PATH, "playerla.png"))), (utils.loadImage(os.path.join(PATH, "playerr.png")), utils.loadImage(os.path.join(PATH, "playerra.png"))))
	return CHARIMAGES[name]
