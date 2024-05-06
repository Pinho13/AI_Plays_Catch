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
        self.reward = Reward()
        self.runner = []
        self.delta_time = 0

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


if __name__ == "__main__":
    game = Game()
    game.run()
