import os
SPRITES = {}
for path, files, dirs in os.walk("."):
	for f in files():
		if fnmatch.fnmatch(f, "*.png"):
			SPRITES[f.split(".")[0]] = pygame.image.load(os.path.join(path, f).convert()
			SPRITES[f].setcolorkey((255, 0, 170))
