from pygame import *
from gloss import *
import chameleon
class glGame(GlossGame, chameleon.manager, chameleon.listener):
    def __init__(self):
        GlossGame.__init__(self, "Evergreen")
        chameleon.manager.__init__(self)
        chameleon.listener.__init__(self)
        self.setResponse("distBlockState", self.ev_distBlockState)
        self.setResponse("distEntityPos", self.ev_distEntityPos)
        self.reg("distBlockState", self)
        self.reg("distEntityPos", self)
        self.blockState = []
        self.floorState = []
        self.char = None
        self.entityState = []
    def load_content(self):
        import
    def ev_distBlockState(self, data):
        print "diststate"
        if self.blockState is not None: #This whole section is only called upon level switch, so it's not performance critical.
            print "new blockstate"
            if self.entityState:
                self.entityState = [] #Keep entityState from being blit in ev_update.
        self.blockState = []
        self.floorState = []
        blockState = data[0]
        floorState = data[1]
        for sprite in blockState.sprites():
            self.blockState.append(Sprite(spritepack.getImage(sprite.imgname), position=sprite.topleft))
        for sprite in self.floorState.sprites():
            self.blockState.append(Sprite(spritepack.getImage(sprite.imgname), position=sprite.topleft))
        #self.blockState.draw(self.surfBuf) #We need to perform an initial draw here so we don't need extra logic in ev_update for whether or not to call self.state.clear().
        #self.floorState.draw(self.surfBuf)
    def ev_distEntityPos(self, data):
        self.entityState = None
        entityState = data
        self.char = [char for char in entityState.sprites() if char.data["name"] == CONFIG["playername"]][0]
        entityState.remove(self.char)
        if spritepack.hasEntityImage(sprite.imgname):
            sprite.images = spritepack.getEntityImage(sprite.imgname)
        else:
            sprite.images = spritepack.getEntityImage("entity")
        self.char = Sprite(self.char.images[self.char.data["facing"]][0], position=self.char.topleft)
        for sprite in entityState.sprites():
            if spritepack.hasEntityImage(sprite.imgname):
                sprite.images = spritepack.getEntityImage(sprite.imgname)
            else:
                sprite.images = spritepack.getEntityImage("entity")
            self.entityState.append(Sprite(sprite.images[sprite.data["facing"]][0], position=sprite.topleft))
        #self.chargroup.add(self.char)
        #self.entityState.draw(self.surfBuf)
        #self.chargroup.draw(self.surfBuf)
    def draw(self):
        if self.entityState:
            glTranslatef(self.char.rect.x, self.char.rect.y, 0)
            Gloss.clear()
            for block in self.blockState:
                block.draw() #Unneeded
            for floor in self.floorState:
                floor.draw()
            for entity in self.entityState:
                entity.draw()
            self.char.draw()
            glLoadIdentity()
