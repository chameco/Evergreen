from src import level
from src import base
import random
class randLevel(level.level):
    def __init__(self, width, height):
        level.level.__init__(self)
        self.width = width
        self.height = height
        self.blocks["#"] = base.stone
        self.blocks[">"] = base.stairsDown
        self.blocks["<"] = base.stairsUp
        self.blocks["w"] = base.woodFloor
        self.loadLevel()
    def loadLevel(self):
        self.rooms = []
        self.prelim = []
        row = ["#"] * self.width
        for i in range(0, self.height):
            self.prelim.append(list(row))
        for i in range(0, 20):
            self.generateRoom()
        for i in range(0, 100):
            self.joinRoom()
        #print self.prelim
        self.prelim[0] = ["#"] * self.width
        self.prelim[len(self.prelim)-1] = ["#"] * self.width
        for y in self.prelim:
            y[0] = "#"
            y[len(y)-1] = "#"
        while 1:
            x = random.randint(1, len(self.prelim)-2)
            y = random.randint(1, len(self.prelim[0])-2)
            if self.prelim[y][x] == "w":
                self.prelim[y][x] = "C"
                break
        while 1:
            x = random.randint(1, len(self.prelim)-2)
            y = random.randint(1, len(self.prelim[0])-2)
            if self.prelim[y][x] == "w":
                self.prelim[y][x] = ">"
                break
        while 1:
            x = random.randint(1, len(self.prelim)-2)
            y = random.randint(1, len(self.prelim[0])-2)
            if self.prelim[y][x] == "w":
                self.prelim[y][x] = "<"
                break
        self.levelimp = "\n".join(["".join(line) for line in self.prelim])
        level.level.loadLevel(self)
    def generateRoom(self, w=None, h=None):
        width = random.randint(3, 10) if not w else w
        height = random.randint(3, 10) if not h else h
        x = random.randint(0, len(self.prelim)-width-1)
        y = random.randint(0, len(self.prelim[0])-height-1)
        try:
            for yi in range(y, y+height):
                self.prelim[yi][x:x+width] = ["w"] * width
        except IndexError:
            pass
    def joinRoom(self):
        x = random.randint(1, len(self.prelim)-2)
        y = random.randint(1, len(self.prelim[0])-2)
        if (self.prelim[y][x-1] == "w" and self.prelim[y][x+1] == "w") or (self.prelim[y-1][x] == "w" and self.prelim[y+1][x] == "w"):
            self.prelim[y][x] = "w"
        else:
            self.joinRoom()
