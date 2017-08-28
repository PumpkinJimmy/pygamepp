import pygame
from pygame.locals import *
class Player:
    def __init__(self, sprite=None, speedx=5, speedy=5):
        self.sprite = sprite
        self.speedx = speedx
        self.speedy = speedy
        pygame.key.set_repeat(1, 5)
    @classmethod
    def create_with_filename(cls, filename):
        image = pygame.image.load(filename)
        rect = image.get_rect()
        sprite = pygame.sprite.Sprite()
        sprite.image = image
        sprite.rect = rect
        return cls(sprite)
    def update(self):
        self.sprite.update()

    def draw(self, surf):
        surf.blit(self.sprite.image, self.sprite.rect)

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.move_x(-self.speedx)
            elif event.key == K_RIGHT:
                self.move_x(self.speedx)
            # elif event.key == K_UP:
            #     self.move_y(-self.speedy)
            # elif event.key == K_DOWN:
            #     self.move_y(self.speedy)

    def move_x(self, x):
        self.sprite.rect.left += x

    def move_y(self, y):
        self.sprite.rect.top += y
