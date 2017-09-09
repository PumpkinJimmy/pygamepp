from framework.node import Node
from framework.layer import Layer
from framework.director import Director
from framework.event import listen
from pygame.locals import *
from player import Player
from puzzle import Maze
import pygame
import sys


class StartUp(Layer):
    def init(self):
        super(StartUp, self).init()
        director = Director.instance()
        self.image = director.font.render(
            "Press Enter to start",
            1,
            (255, 255, 255)
        )
        self.rect.center = director.rect.center
        self.listen(KEYDOWN, self.replace)
    def replace(self, event):
        if event.key == K_RETURN:
            Director.instance().replace_scene(Level().create_scene())

    # def handle(self, event):
    #     # super(StartUp, self).handle()
    #     if event.type == KEYDOWN:
    #         if event.key == K_RETURN:
    #             Director.instance().replace_scene(Level().create_scene())
                # Application.instance().replace_scene(GameOver())


class Level(Layer):
    def init(self):
        super(Level, self).init()
        director = Director.instance()
        self.image = pygame.Surface(director.resolution)
        self.image.fill((0, 0, 0))
        self.maze = Maze()
        self.add_child(self.maze)
        self.player = Player()
        self.player.maze = self.maze
        self.add_child(self.player)
        self.schedule_update()

    def update(self, dt):
        tiles = self.player.cover_tile(self.player.sprite.rect)
        if self.maze.end in tiles:
            Director.instance().replace_scene(GameOver().create_scene())


class GameOver(Layer):
    def init(self):
        super(GameOver, self).init()
        director = Director.instance()
        self.image = pygame.Surface(director.resolution)
        self.image.fill((0, 0, 0))
        # app.screen.fill((0, 0, 0))
        text = director.font.render(
            "Game Over",
            1,
            (255, 255, 255)
        )
        # self.rect.center = app.screen.get_rect().center
        rect = text.get_rect()
        rect.center = director.rect.center
        self.image.blit(text, rect)
        self.listen(KEYDOWN, self.end)

    def end(self, event):
        if event.key == K_RETURN:
            sys.exit()
