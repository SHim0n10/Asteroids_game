from constants import *
from Classes.SpaceObject import *
from functions import *
import Classes.Shield as Shield
import Classes.Laser as Laser
import math as math
import pyglet
class Spaceship(SpaceObject):

    "Konśtruktor"
    def __init__(self, sprite, x ,y):
        super().__init__(sprite,x,y)
        self.fire = -1
        self.shield = True
        self.get_shield()

        flame_sprite = pyglet.image.load('Assetss\PNG\Effects\\fire08.png')
        set_anchor_of_image_to_center(flame_sprite)
        self.flame = pyglet.sprite.Sprite(flame_sprite,batch=batch)
        self.flame.visible = False

        self.snd_laser = pyglet.media.load('Assetss\Bonus\sfx_laser1.ogg', streaming=False)
        self.snd_shield_up = pyglet.media.load('Assetss\Bonus\sfx_shieldUp.ogg', streaming=False)
        self.snd_shield_down = pyglet.media.load('Assetss\Bonus\sfx_shieldDown.ogg', streaming=False)
        

    "SHIELD"
    def get_shield(self):
        global lifes
        self.shield = True
        img = pyglet.image.load('Assetss\PNG\Effects\shield1.png')
        set_anchor_of_image_to_center(img)
        stit = Shield(img, self.sprite.x, self.sprite.y)
        stit.rotation = self.rotation
        game_objects.append(stit)
        pyglet.clock.schedule_once(self.shield_loose, SHIELD)
        self.snd_shield_up = pyglet.media.load('Assetss\Bonus\sfx_shieldUp.ogg', streaming=False)
        my_Player.queue(self.snd_shield_up)

        if lifes <= 0:
            my_Player.delete()
        my_Player.play()

         #PREMENNÁ PRE DELAY streľby
    def shield_loose(self, time):
        self.shield = False
        my_Player.queue(self.snd_shield_down)
        my_Player.play()
    """
    Metóda zodpovedná za vystrelenie laseru
    """
    def shoot(self):
        # Todo: Vytvor nový objekt typu Laser a nastav parameter fire na hodnotu delayu
        sprite = pyglet.image.load('Assetss/PNG/Lasers/laserBlue06.png')
        set_anchor_of_image_to_center(sprite)
        position_x = self.sprite.x
        position_y = self.sprite.y
        
        laser = Laser(sprite, position_x, position_y)
        laser.rotation = self.rotation
        game_objects.append(laser)
        
        
    def get_position(self):
        global pozicia_x,pozicia_y,rotacia
        pozicia_x = self.sprite.x
        pozicia_y = self.sprite.y
        rotacia = self.rotation

    """
    Každý frame sa vykoná táto metóda to znamená v našom prípade:
    60 simkov * za sekundu
    Mechanic of spaceship - rotation, movement, controls
    """
    def tick(self, dt):
        super().tick(dt)
        

        "Zrýchlenie po kliknutí klávesy W. Výpočet novej rýchlosti"
        if 'W' in pressed_keyboards:
            self.x_speed = self.x_speed + dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed = self.y_speed + dt * ACCELERATION * math.sin(self.rotation)

            #FLAME
            self.flame.x = self.sprite.x - math.cos(self.rotation) * self.radius
            self.flame.y = self.sprite.y - math.sin(self.rotation) * self.radius
            self.flame.rotation = self.sprite.rotation
            self.flame.visible = True
        else:
            self.flame.visible = False

        "Spomalenie/spätný chod po kliknutí klávesy S"
        if 'S' in pressed_keyboards:
            self.x_speed = self.x_speed - dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed = self.y_speed - dt * ACCELERATION * math.sin(self.rotation)

        "Otočenie doľava - A"
        if 'A' in pressed_keyboards:
            self.rotation += ROTATION_SPEED

        "Otočenie doprava - D"
        if 'D' in pressed_keyboards:
            self.rotation -= ROTATION_SPEED

        "Ručná brzda - SHIFT"
        if 'SHIFT' in pressed_keyboards:
            self.x_speed = 0
            self.y_speed = 0

        # Todo: pridaj akciu po stlačení tlačítka SPACE = shoot
        #self.fire -= dt # Todo: Je treba odčítať delay z fire
        if 'SPACE' in pressed_keyboards:
            if self.fire <= 0:
                self.shoot()
                my_Player.delete()
                my_Player.queue(self.snd_laser)
                my_Player.play()
                self.fire = DELAY
            self.fire -= dt
        
        #Ak je shield aktívny
        if self.shield:
            self.get_position()
            
        "VYBERIE VŠETKY OSTATNE OBJEKTY OKREM SEBA SAMA"
        for obj in [o for o in game_objects if o != self]:
            # d = distance medzi objektami
            d = self.distance(obj)
            if d < self.radius + obj.radius:
                obj.hit_by_spaceship(self)
                break

    "Metóda zodpovedná za reset pozície rakety"
    def reset(self):
        self.sprite.x = WIDTH // 2
        self.sprite.y = HEIGHT // 2
        self.rotation = 1.57  # radiany -> smeruje hore
        self.x_speed = 0
        self.y_speed = 0