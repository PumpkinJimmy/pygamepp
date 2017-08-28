import sys
import pygame
from toolkit.animation import AnimateSprite
from pygame import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
texture = pygame.image.load("texture.png").convert_alpha()
bg = (255, 255, 255)
screen.fill(bg)
rect = texture.get_rect()
row = 3
col = 5
width, height = rect.size[0] // col, rect.size[1] // row
black = (0, 0, 0)
grey = (100, 100, 100, 2)
images = [texture.subsurface(Rect(j * width, i * height, width, height)) \
          for i in range(row) for j in range(col)][:6]
images2 = [texture.subsurface(Rect(j * width, i * height, width, height)) \
           for i in range(row) for j in range(col)][6:13]
sprite = AnimateSprite.create_with_images(images)
sprite2 = AnimateSprite.create_with_images(images2)
sprite2.rect.centery = 300
pygame.display.flip()
clock = pygame.time.Clock()
while 1:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    sprite.update()
    sprite2.update()
    screen.fill(bg)
    sprite.draw(screen)
    sprite2.draw(screen)
    pygame.display.flip()
