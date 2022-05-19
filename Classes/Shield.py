from Classes.SpaceObject import SpaceObject
from constants import *
class Shield(SpaceObject):
    def __init__(self, sprite, x, y):
        super().__init__(sprite, x, y)
        self.shieldtime = SHIELD
    
    def change_position(self):
        global pozicia_x,pozicia_y,rotacia
        self.sprite.x = pozicia_x
        self.sprite.y = pozicia_y
        self.rotation = rotacia
    def tick(self, dt):
        super().tick(dt)
        if self.shieldtime <= 0:
            self.delete()
        self.shieldtime -= dt
        self.change_position()