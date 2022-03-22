import pygame as pg
import sys
import random

### МУЗЫКА
#pg.mixer.music.load("asd.mp3")
#pg.mixer.music.play(-1)
#pg.mixer.music.set_volume(0.05)
###

### КОНСТАНТЫ
W = 1024
H = 768
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0, 0, 255)
speed = 8
x = 100
y = 100
dy = 0.0
h = 400
score = 0
player_w = 50
restart = 'R'
FPS = 100
clock=pg.time.Clock()
allbullets = []
game_over = False
done = False
###

### ДИСПЛЕЙ
display = pg.display.set_mode((1024, 768))
pg.display.set_caption("Mshke Jump")
fon = pg.image.load("fon.jpg").convert()
player = pg.image.load("BigBobych.png").convert_alpha()
player = pg.transform.scale(player, (player.get_width()//5, player.get_height()//5))
player = pg.transform.flip(player, True, False)
platform = pg.image.load("platform.png").convert_alpha()
platform = pg.transform.scale(platform, (platform.get_width()//20, platform.get_height()//23))
platform2 = pg.image.load("platform2.png").convert_alpha()
platform2 = pg.transform.scale(platform2, (platform2.get_width()//15, platform2.get_height()//15))
pg.font.init()
score_display = pg.font.SysFont("comicsans", 30)
bullet_img = pg.image.load("bullet.png").convert_alpha()
bullet_img = pg.transform.scale(bullet_img, (40, 40))
###

### ПЛАТФОРМЫ
class plat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class plat2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

platforms = [plat(random.randrange(0, W), random.randrange(0, H)) for i in range(19)]
platforms2 = [plat2(random.randrange(0, W), random.randrange(0, H)) for i in range(2)]
###


### СТРЕЛЬБА
class Bullet:
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.speed = 5
    def move_bullet(self):
        self.y -= self.speed
        if self.y >= 0:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else: 
            return False
###

pg.mixer.pre_init(44100, -16, 2, 1024)
pg.mixer.init()

### ГЛАВНЫЙ ЦИКЛ
while not done:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            done = True

    display.blit(fon, (0, 0))

### GAME OVER (Quit & Restart)
    if y > 750:
        text = score_display.render("GAME OVER! R -> Restart  Q -> Quit", True, RED)
        text_rect = text.get_rect()
        text_x = display.get_width() / 2 - text_rect.width / 2
        text_y = display.get_height() / 2 - text_rect.height / 2
        stop=display.blit(text, [text_x, text_y])
    if y>760:
        game_over = True
        score = 0
    keys = pg.key.get_pressed()
    if keys[pg.K_r]:
        game_over = False
    if keys[pg.K_q]:
        done = True
###

    for plat in platforms:
        display.blit(platform, (plat.x, plat.y))
    for plat2 in platforms2:
        display.blit(platform2, (plat2.x, plat2.y))

### GAME LOGIC
    keys = pg.key.get_pressed()
    if not game_over:
        if keys[pg.K_a] and x > 0:
            x -= speed
            player = pg.image.load("BigBobych.png")
            player = pg.transform.scale(player, (player.get_width()//5, player.get_height()//5))
            player = pg.transform.flip(player, True, False)
        if keys[pg.K_d] and x + player_w < W:
            x += speed
            player = pg.image.load("BigBobych.png")
            player = pg.transform.scale(player, (player.get_width()//5, player.get_height()//5))
            player = pg.transform.flip(player, True, False)

        if keys[pg.K_SPACE]:
            if len(allbullets) < 1:
                allbullets.append(Bullet(x-20, y))
                pg.mixer.music.load("bullet.wav")
                pg.mixer.music.play(1)
                pg.mixer.music.set_volume(1)

        for bullet in allbullets:
            if not bullet.move_bullet():
                allbullets.remove(bullet)

        if y < h:
            y = h
            for plat in platforms:
                plat.y = plat.y - dy
                if plat.y > H:
                    plat.y = 0
                    plat.x = random.randrange(0, W)
                    score += random.randint(0,70)

            for plat2 in platforms2:
                plat2.y = plat2.y - dy
                if plat2.y > H:
                    plat2.y = 0
                    plat2.x = random.randrange(0, W)

        dy += 0.2
        y += dy
        if y > H:
            dy = -10
        for plat in platforms:
            if (x + 50 > plat.x) and (x + 20 < plat.x + 68) and (y + 70 > plat.y) and (y + 70 < plat.y + 14) and dy > 0:
                dy = -10

        text = score_display.render("score: " + str(score), 1, (255,0,0))
        display.blit(text, (W - 10 - text.get_width(),10))
        display.blit(player, (x, y))
        clock.tick(FPS)
        pg.display.update()
###

