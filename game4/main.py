import sys
import pygame
from pygame import *
pygame.init()
texture = pygame.image.load("texture.png")
screen = pygame.display.set_mode(texture.get_rect().size)
bg = (255, 255, 255)
screen.fill(bg)

screen.blit(texture, texture.get_rect())
rect = texture.get_rect()
row = 3
col = 5
width, height = rect.size[0] // col, rect.size[1] // row
black = (0, 0, 0)
grey = (100, 100, 100, 2)
for j in range(col):
    pygame.draw.line(screen, black, (j * width, 0), (j* width, rect.height), 1)
for i in range(row):
    pygame.draw.line(screen, black, (0, i * height), (rect.width, i * height), 1)
pygame.display.flip()
cur = Rect(0, 0, width, height)
rect_surf = pygame.Surface(texture.get_rect().size).convert_alpha()
rect_surf.fill((255, 255, 255, 0))
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    pos = pygame.mouse.get_pos()
    curcol = pos[0] // width
    currow = pos[1] // height
    cur.top = currow * height
    cur.left = curcol * width
    rect_surf.fill(grey, cur)
    screen.blit(rect_surf, rect_surf.get_rect())
    pygame.display.flip()