from framework.node import Node
from toolkit.animation import AnimateSprite
import pygame
from pygame.locals import *


class PlayerSprite(Node):
    def init(self):
        image = pygame.image.load("player.png").convert_alpha()
        self.direct = 0
        self.side_sprites = []
        size = image.get_size()
        width = size[0] // 4
        height = size[1] // 4
        for row in range(4):
            side = []
            for col in range(4):
                side.append(image.subsurface(Rect(col * width, row * height, width, height)))
            sprite = AnimateSprite.create_with_images(side)
            # sprite.rect.top = row * height
            sprite._update = sprite.update
            sprite._handle = lambda x: None
            sprite._draw = sprite.draw
            # self.add_child(sprite)
            self.side_sprites.append(sprite)
        self.add_child(self.side_sprites[0])
        self.rect.size = self.children[0].rect.size
        self.schedule_update()

    def goside(self, direct):
        if self.direct == direct:
            return
        self.remove_child(self.side_sprites[self.direct])
        self.direct = direct
        self.add_child(self.side_sprites[self.direct])

    def update(self, dt):
        self.children[0].update(dt)
        self.children[0].rect.topleft = self.rect.topleft

class Player(Node):
    def init(self):
        self.sprite = PlayerSprite()
        self.sprite.rect.topleft = (75, 75)
        self.speed = 5
        self.add_child(self.sprite)
        pygame.key.set_repeat(50, 30)
        self.listen(KEYDOWN, self.handle)

    def cover_tile(self, rect):
        startx = rect.left // 75
        endx = rect.right // 75
        starty = rect.top // 75
        endy = rect.bottom // 75
        tiles = [(row, col) for row in range(starty, endy + 1) for col in range(startx, endx + 1)]
        return tiles
    def cover_solid(self, rect):
        tiles = self.cover_tile(rect)
        for tile in tiles:
            if self.maze.data[tile[0] * self.maze.maze_size[1] + tile[1]]:
                return True
        return False
    def move_x(self, x):
        new_rect = self.sprite.rect.copy()
        new_rect.left += x
        if not self.cover_solid(new_rect):
            self.sprite.rect = new_rect
    def move_y(self, y):
        new_rect = self.sprite.rect.copy()
        new_rect.top += y
        if not self.cover_solid(new_rect):
            self.sprite.rect = new_rect
    def handle(self, event):
        if event.key == K_LEFT:
            self.move_x(-self.speed)
            self.sprite.goside(1)
        elif event.key == K_RIGHT:
            self.move_x(self.speed)
            self.sprite.goside(2)
        elif event.key == K_UP:
            self.move_y(-self.speed)
            self.sprite.goside(3)
        elif event.key == K_DOWN:
            self.move_y(self.speed)
            self.sprite.goside(0)
