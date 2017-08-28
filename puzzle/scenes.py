from framework.node import Node
from framework.app import Application
from pygame.locals import *
from player import Player
from puzzle import Maze
import pygame
import sys


class StartUp(Node):
    def init(self):
        app = Application.instance()
        self.image = app.font.render(
            "Press Enter to start",
            1,
            (255, 255, 255)
        )
        self.rect.center = app.screen.get_rect().center

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                Application.instance().replace_scene(Level())
                # Application.instance().replace_scene(GameOver())


class Level(Node):
    def init(self):
        app = Application.instance()
        self.image = pygame.Surface(app.resolution)
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
            Application.instance().replace_scene(GameOver())


class GameOver(Node):
    def init(self):
        app = Application.instance()
        self.image = pygame.Surface(app.resolution)
        self.image.fill((0, 0, 0))
        # app.screen.fill((0, 0, 0))
        text = app.font.render(
            "Game Over",
            1,
            (255, 255, 255)
        )
        # self.rect.center = app.screen.get_rect().center
        rect = text.get_rect()
        rect.center = app.screen.get_rect().center
        self.image.blit(text, rect)

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                sys.exit()
