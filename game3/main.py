import sys, re, glob
import pygame
from pygame.locals import *
from player import Player
from toolkit.animation import AnimateSprite
pygame.init()
screen = pygame.display.set_mode((800, 600))
bg = (255, 255, 255)
screen.fill(bg)
imgs = []
pat = re.compile(r"resource\\run([0-9]+?)\.png")
paths = glob.glob("resource\\run*.png")
paths.sort(key=lambda p: int(re.search(pat, p).group(1)))
for path in paths:
    img = pygame.image.load(path).convert_alpha()
    imgs.append(img)
sprite = AnimateSprite.create_with_images(imgs)
sprite.rect.centery = 300
myp = Player(sprite)
# myp = Player.create_with_filename("run1.png")
clock = pygame.time.Clock()
while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        myp.handle(event)
    myp.update()
    screen.fill(bg)
    myp.draw(screen)
    pygame.display.flip()