from random import randint
import pygame as pg
import sys

pg.time.set_timer(pg.USEREVENT, 3000)

W = 400
H = 400
WHITE = (255, 255, 255)
CARS = ('car1.png', 'car2.png', 'car3.png')
# для хранения готовых машин-поверхностей
CARS_SURF = []


# надо установить видео режим
# до вызова image.load()
sc = pg.display.set_mode((W, H))

for i in range(len(CARS)):
    CARS_SURF.append(
        pg.image.load(CARS[i]).convert_alpha())

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, surf):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(
            center=(x, y))

    def update(self, position):
        self.rect.x = position[0] - 15
        self.rect.y = position[1] - 25

pl = Player(W // 2, H // 2, CARS_SURF[2])

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

    sc.fill(WHITE)

    pos = pg.mouse.get_pos()
    pl.update(pos)
    sc.blit(pl.image, pl.rect)

    pg.display.update()
    pg.time.delay(20)
    
# TODO: класс объектов, от которых будем уклоняться
# им при создании случайную скорость и фиксированные координаты
# прописать отражение от стенок: соответствующая скорость должна менять знак ( vx = vx * (-1))
