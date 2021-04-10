from random import randint
import pygame as pg
import sys

pg.init()
pg.mixer.init()
pg.time.set_timer(pg.USEREVENT, 3000)

score = 0
lives = 3
W = 1300
H = 1000
WHITE = (255, 255, 255)
GRAY = (247, 247, 247)
CARS = ('red.png', 'blue.png', 'pl.png')
# для хранения готовых машин-поверхностей
CARS_SURF = []
explosion_sound = pg.mixer.Sound('explosion.mp3')
explosion_sound.set_volume(0.1)
#ball_image = pg.image.load('ball.png').convert_alpha()


# надо установить видео режим
# до вызова image.load()
sc = pg.display.set_mode((W, H))

for i in range(len(CARS)):
    CARS_SURF.append(
        pg.image.load(CARS[i]).convert_alpha())
    CARS_SURF[i].set_colorkey(GRAY)

class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, color, image, group):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.mask.invert()
        self.color = color
        self.add(group)
        self.speed_x = randint(-5, 5)
        self.speed_y = randint(-5, 5)
        # pg.draw.ellipse()
        self.life = 500
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.life -= 1
        if self.life <= 0:
            self.kill()
        if self.rect.x <= 0 or self.rect.x >= W - 50:
            self.speed_x *= -1
        if self.rect.y <= 0 or self.rect.y >= H - 50:
            self.speed_y *= -1

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, surf):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(
            center=(x, y))

    def update(self, position):
        self.rect.x = position[0] - 15
        self.rect.y = position[1] - 25

#CARS_SURF[2].set_colorkey(GRAY)
pl = Player(W // 2, H // 2, CARS_SURF[2])
mask = pg.mask.from_surface(CARS_SURF[2])
mask.invert()

# pl.image = mask.to_surface(CARS_SURF[2])

pls = pg.sprite.Group()
pls.add(pl)
balls = pg.sprite.Group()
Ball(W // 2, H // 2, 'red', CARS_SURF[0], balls)
Ball(W // 2, H // 2, 'blue', CARS_SURF[1], balls)

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        elif i.type == pg.USEREVENT:
            Ball(W // 2, H // 2, 'red', CARS_SURF[0], balls)
            Ball(W // 2, H // 2, 'blue', CARS_SURF[1], balls)

    sc.fill(WHITE)

    pos = pg.mouse.get_pos()
    pl.update(pos)
    balls.update()
    balls.draw(sc)
    sc.blit(pl.image, pl.rect)

    if pg.sprite.spritecollideany(pl, balls):
        for b in balls:
            if pg.sprite.spritecollideany(b, pls):
                offset = (pl.rect.x - b.rect.x), (pl.rect.y - b.rect.y)
                overlap = mask.overlap(b.mask, offset)
                if overlap:
                    if b.color == 'blue':
                        score += 1
                    else:
                        lives -= 1
                        explosion_sound.play()
                    b.kill()
                    print(f'Score: {score}, Lives: {lives}')
    if lives <= 0:
        print('WASTED')
        pg.quit()
        sys.exit()
    pg.display.update()
    pg.time.delay(20)

# TODO: придумать принцип смены уровней сложности
# отметить характеристики (переменные), которые будут изменяться с возрастанием сложности
