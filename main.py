import pygame
import sys
import random

from random import randint
from pygame import Vector2
from settings import *
from squares import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Catch")
        self.clock = pygame.Clock()
        self.events = pygame.event.get()
        self.reward = Reward(self)
        self.runner = []
        self.delta_time = 0
        self.spawn()

    def spawn(self):
        self.reward.time_alive = 0
        for i in range(NUMBER_OF_SQUARES):
            self.runner.append(Squares(self, Vector2(SPAWN)))

    def check_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.delta_time = self.clock.tick(FPS) / 1000
        self.draw()
        for runner in self.runner:
            if isinstance(runner, Squares):
                runner.update()
                if runner.should_delete:
                    self.runner.remove(runner)
        if len(self.runner) <= 0:
            self.spawn()
        pygame.display.update()
        pygame.display.set_caption("Catch - " + str(int(self.clock.get_fps())))

    def draw(self):
        self.screen.fill(pygame.Color("white"))
        self.reward.draw(self.screen)

    def debug(self):
        print("Runner: y =" + str(self.runner.pos))

    def run(self):
        while True:
            self.check_events()
            self.update()


class Text(pygame.sprite.Sprite):
    def __init__(self, pos, size, text):
        super().__init__()

        self.pos = pos
        self.text = text
        self.text_font = pygame.font.SysFont(None, int(size))# noqa
        self.image = self.text_font.render(text , True, (0, 0, 0))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.image = self.text_font.render(self.text, True, (0, 0, 0))


if __name__ == "__main__":
    game = Game()
    game.run()
