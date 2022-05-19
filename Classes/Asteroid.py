from constants import *
from Classes.SpaceObject import *
from functions import *
import Classes.Shield as Shield
import Classes.Laser as Laser
import math as math
import pyglet
class Asteroid(SpaceObject):
    "Metóda ktorá sa vykoná ak dôjde ku kolízii lode a asteroidu"
    def hit_by_spaceship(self, ship):
        global lifes
        if ship.shield == False:
            pressed_keyboards.clear()
            ship.reset()
            lifes -= 1
            if lifes <= 0:
                my_Player.delete()
            else:
                ship.get_shield()
            
        self.delete()

    "Metóda ktorá sa vykoná ak dôjde ku kolízii a asteroidu"
    def hit_by_laser(self, laser):
        global score, scoreLabel
        laser.delete()
        
        scoreLabel = pyglet.text.Label(text=str(score), font_size=40,x = 1150, y = 760, anchor_x='right', anchor_y='center')
        score += 10
        self.delete()
        pass