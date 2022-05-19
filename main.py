from asyncio import shield
import math
import random

import pyglet
from pyglet import gl
from pyglet.window import key

from constants import *
from Classes.SpaceObject import *
from functions import *
import Classes.Shield as Shield
import Classes.Laser as Laser
import math as math
import Classes.Asteroid as Asteroid
import pyglet

class Game:
    """
    Konstruktor
    """
    def __init__(self):
        self.window = None
        game_objects = []
        space_lifes = pyglet.image.load(r'Assetss\PNG\UI\playerLife1_blue.png')
        set_anchor_of_image_to_center(space_lifes)
        self.ship_lifes = pyglet.sprite.Sprite(space_lifes,batch=batch)
        self.ship_lifes.visible = False
        self.over = False

    """
    Načítanie všetkých spritov
    """
    def load_resources(self):
        self.playerShip_image = pyglet.image.load('Assetss/PNG/playerShip1_blue.png')
        set_anchor_of_image_to_center(self.playerShip_image)
        self.background_image = pyglet.image.load('Assetss/Backgrounds/black.png')
        self.asteroid_images = ['Assetss/PNG/Meteors/meteorGrey_big1.png',
                           'Assetss/PNG/Meteors/meteorGrey_med1.png',
                           'Assetss/PNG/Meteors/meteorGrey_small1.png',
                           'Assetss/PNG/Meteors/meteorGrey_tiny1.png',
                           'Assetss\PNG\Meteors\meteorGrey_big2.png',
                           'Assetss\PNG\Meteors\meteorGrey_med2.png',   
                           'Assetss\PNG\Meteors\meteorGrey_small2.png']
        

    """
    Vytvorenie objektov pre začiatok hry
    """
    def init_objects(self):
        #Vytvorenie lode
        spaceShip = Spaceship(self.playerShip_image, WIDTH // 2, HEIGHT//2)
        game_objects.append(spaceShip)

        #Nastavenie pozadia a prescalovanie
        self.background = pyglet.sprite.Sprite(self.background_image)
        self.background.scale_x = 6
        self.background.scale_y = 4

        #Vytvorenie Meteoritov
        self.create_asteroids(count=7)
        #Pridavanie novych asteroidoch každych 10 sekund
        pyglet.clock.schedule_interval(self.create_asteroids, 5, 1)

    def create_asteroids(self, dt=0, count=1):
        "Vytvorenie X asteroidov"
        for i in range(count):
            # Výber asteroidu náhodne
            img = pyglet.image.load(random.choice(self.asteroid_images))
            set_anchor_of_image_to_center(img)

            # Nastavenie pozície na okraji obrazovky náhodne
            position = [0, 0]
            dimension = [WIDTH, HEIGHT]
            axis = random.choice([0, 1])
            position[axis] = random.uniform(0, dimension[axis])

            # Nastavenie rýchlosti
            tmp_speed_x = random.uniform(-100, 100)
            tmp_speed_y = random.uniform(-100, 100)

            #Temp asteroid object
            asteroid = Asteroid(img, position[0], position[1], tmp_speed_x, tmp_speed_y)
            game_objects.append(asteroid)

    def lifes_draw(self):
        sirka = 20
        for i in range(lifes):
            ship_lifes = pyglet.image.load(r'Assetss\PNG\UI\playerLife1_blue.png')
            ship_life = pyglet.sprite.Sprite(ship_lifes, sirka, 20)
            ship_life.draw()
            sirka += 40

    def load_win(self):
        global score
        self.win_ = pyglet.image.load(r'Assetss\PNG\UI\win.jpg')
        self.background = pyglet.sprite.Sprite(self.win_)
        self.background.scale_x = 0.5
        self.background.scale_y = 0.5
        self.win_text = pyglet.text.Label(text='Game Over!',x=WIDTH//2,y=HEIGHT//2+30,font_size=50,anchor_x='center',anchor_y='center', font_name='Comic Sans MS')
        self.win_text1 = pyglet.text.Label(text=f'Your score:{score}',x=WIDTH//2,y=HEIGHT//2-30,font_size=30,anchor_x='center',anchor_y='center')
        self.snd_win = pyglet.media.load(r'Assetss\Bonus\sfx_lose.ogg', streaming=False)
        my_Player.delete()
        my_Player.queue(self.snd_win)
        my_Player.play()

    def game_stat_control(self):
        if lifes == 0:
            if self.over == False:
                self.over = True
                self.game_over()

    def game_over(self):
        game_objects.clear()
        self.load_win()
        

        
    """
    Event metóda ktorá sa volá na udalosť on_draw stále dookola
    """
    def draw_game(self):
        global score, scoreLabel, lifes
        
        # Vymaže aktualny obsah okna
        self.window.clear()
        # Vykreslenie pozadia
        self.background.draw()
        
        scoreLabel = pyglet.text.Label(text=str(score), font_size=40,x = 1150, y = 760, anchor_x='right', anchor_y='center')
        if self.over:
            self.win_text.draw()
            self.win_text1.draw()
            return
        scoreLabel.draw()
        




        "Vykreslenie koliznych koliečok"
        # for o in game_objects:
            # draw_circle(o.sprite.x, o.sprite.y, o.radius)

        # Táto časť sa stará o to aby bol prechod cez okraje okna plynulý a nie skokový
        for x_offset in (-self.window.width, 0, self.window.width):
            for y_offset in (-self.window.height, 0, self.window.height):
                # Remember the current state
                gl.glPushMatrix()
                # Move everything drawn from now on by (x_offset, y_offset, 0)
                gl.glTranslatef(x_offset, y_offset, 0)

                # Draw !!! -> Toto vykreslí všetky naše sprites
                
                batch.draw()

                # Restore remembered state (this cancels the glTranslatef)
                gl.glPopMatrix()
        
        
        self.lifes_draw()
        self.game_stat_control()

    """
    Event metóda pre spracovanie klávesových vstupov
    """
    def key_press(self, symbol, modifikatory):
        if symbol == key.W:
            pressed_keyboards.add('W')
        if symbol == key.S:
            pressed_keyboards.add('S')
        if symbol == key.A:
            pressed_keyboards.add('A')
        if symbol == key.D:
            pressed_keyboards.add('D')
        if symbol == key.LSHIFT:
            pressed_keyboards.add('SHIFT')
        if symbol == key.SPACE:
            pressed_keyboards.add('SPACE')
        #Todo: SPACE

    """
    Event metóda pre spracovanie klávesových výstupov
    """
    def key_release(self, symbol, modifikatory):
        if symbol == key.W:
            pressed_keyboards.discard('W')
        if symbol == key.S:
            pressed_keyboards.discard('S')
        if symbol == key.A:
            pressed_keyboards.discard('A')
        if symbol == key.D:
            pressed_keyboards.discard('D')
        if symbol == key.LSHIFT:
            pressed_keyboards.discard('SHIFT')
        if symbol == key.SPACE:
            pressed_keyboards.discard('SPACE')
        # Todo: SPACE

    """
    Update metóda
    """
    def update(self, dt):
        for obj in game_objects:
            obj.tick(dt)

    """
    Start game metóda 
    """
    def start(self):
        "Vytvorenie hlavneho okna"
        self.window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

        "Nastavenie udalosti (eventov)"
        self.window.push_handlers(
            on_draw=self.draw_game,
            on_key_press=self.key_press,
            on_key_release=self.key_release
        )

        "Load resources"
        self.load_resources()

        "Inicializacia objektov"
        self.init_objects()

        "Nastavenie timeru pre update metódu v intervale 1./60 = 60FPS"
        pyglet.clock.schedule_interval(self.update, 1. / 60)

        pyglet.app.run()  # all is set, the game can start

"----------- StartGame -----------"
Game().start()