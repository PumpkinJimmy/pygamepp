import sys
import pygame
from pygame.locals import *

pygame.init()

resolution = (800, 600)
flag = 0
bg_color = (255, 255, 255)
screen = pygame.display.set_mode(resolution, flag, 32)
screen.fill(bg_color)

img_ball = pygame.image.load("ball.png").convert_alpha()
rect_ball = img_ball.get_rect()
rect_ball.topleft = (50, 50)
screen.blit(img_ball, rect_ball)
pygame.display.flip()
clock = pygame.time.Clock()
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
