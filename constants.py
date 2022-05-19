import pyglet
"---------Globalne konštanty a premenne----------"

"Window constants"
WIDTH = 1200
HEIGHT = 800

"Game constants"
ACCELERATION = 120              #Zrýchlenie rakety
ROTATION_SPEED = 0.05           #Rýchlosť otáčania rakety

game_objects = []
batch = pyglet.graphics.Batch() #ZOZNAM SPRITOV PRE ZJEDNODUŠENÉ VYKRESLENIE
pressed_keyboards = set()       #MNOŽINA ZMAČKNUTÝCH KLÁVES

# Todo: Pridaj KONŠTANTY pre delay na strelbu, laserlifetime, laserspeed
"Laser"
DELAY = 0.3
LASERLIFETIME = 1.5
LASERSPEED = 300



SHIELD = 5
pozicia_x = 0
pozicia_y = 0
rotacia = 0
lifes = 3

"Score"
score = 0
scoreLabel = pyglet.text.Label(text=str(score), font_size=40,x = 1150, y = 760, anchor_x='right', anchor_y='center')


my_Player = pyglet.media.Player()

