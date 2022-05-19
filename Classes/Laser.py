from Classes.SpaceObject import SpaceObject
from constants import *
import math
class Laser(SpaceObject):
    def __init__(self, sprite, x, y):
        super().__init__(sprite, x, y)
        self.lifetime = LASERLIFETIME
    #Todo: dorobiť triedu Lasera
    def tick(self, dt):
        super().tick(dt)
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.delete()
        self.x_speed = LASERSPEED * math.cos(self.rotation)
        self.y_speed = LASERSPEED * math.sin(self.rotation)
        for obj in [o for o in game_objects if o != self]:
            # d = distance medzi objektami
            d = self.distance(obj)
            if d < self.radius + obj.radius:
                obj.hit_by_laser(self)
                break