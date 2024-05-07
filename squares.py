import random

import pygame

from pygame import Vector2
from settings import *


class Squares:
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.speed = SPEED
        self.image = pygame.Surface(Vector2(CELL_SIZE, CELL_SIZE))
        self.image.fill(pygame.Color("blue"))
        self.rect = self.image.get_rect(center=self.pos)

        self.inputs = []
        self.weights_change = []
        self.weights = []
        self.bias_change = []
        self.bias = []
        self.outputs = []

        self.num_of_weights = 0
        self.num_of_bias = 0
        self.vector = Vector2(0, 0)
        self.catched = True
        self.time_alive = 0
        self.should_delete = False
        self.initializer()

    def initializer(self):
        self.inputs.append(self.pos.x)
        self.inputs.append(self.pos.y)

        for i in range(2):
            self.outputs.append(0)

        self.num_of_weights = len(self.inputs) * len(self.outputs)
        self.num_of_bias = len(self.outputs)

        for i in range(self.num_of_weights):
            self.weights.append(random.uniform(-1, 1))
            self.weights_change.append(random.uniform(-0.1, 0.1))

        for i in range(self.num_of_bias):
            self.bias.append(random.uniform(-1, 1))
            self.bias_change.append(random.uniform(-0.1, 0.1))

    def randomize_values(self):
        for i in range(self.num_of_weights):
            self.weights[i] = random.uniform(-1, 1)
            #print("Weight " + str(i) + ": " + str(self.weights[i]))

        for i in range(self.num_of_bias):
            self.bias[i] = random.uniform(-1, 1)
            #print("Bias " + str(i) + ": " + str(self.bias[i]))

    def update(self):
        self.time_alive += self.game.delta_time
        self.rect.center = self.pos
        self.game.screen.blit(self.image, self.rect)
        self.get_vector()
        self.NeuralNetwork()

    def up(self):
        if (self.pos.y + self.speed) > HEIGHT:
            self.off_screen()
        self.pos.y += self.speed

    def down(self):
        if (self.pos.y - self.speed) < 0:
            self.off_screen()
        self.pos.y -= self.speed

    def right(self):
        if (self.pos.x + self.speed) > WIDTH:
            self.off_screen()
        self.pos.x += self.speed

    def left(self):
        if (self.pos.x - self.speed) < 0:
            self.off_screen()
        self.pos.x -= self.speed

    def off_screen(self):
        #self.pos = Vector2(SPAWN)
        #self.randomize_values()
        #self.reward -= 20

        self.should_delete = True

    def NeuralNetwork(self):
        self.inputs[0] = self.vector.x
        self.inputs[1] = self.vector.y

        for output in range(len(self.outputs)):
            self.outputs[output] = 0
            for input in range(len(self.inputs)):
                for i in range(self.num_of_weights):
                    self.outputs[output] += self.inputs[input] * self.weights[i] + self.bias[output]

        if self.outputs[0] > 0.5:
            self.right()
        elif self.outputs[0] < -0.5:
            self.left()

        if self.outputs[1] > 0.5:
            self.up()
        elif self.outputs[1] < -0.5:
            self.down()

        if self.vector.length() <= REWARD_SIZE+CELL_SIZE:
            #self.reward += 5
            self.time_alive = 0
            #self.game.reward.new_pos()
        if self.time_alive > 10:
            self.off_screen()

    def get_vector(self):
        self.vector = Vector2(self.game.reward.pos - self.pos)


class Reward:
    def __init__(self, game):
        self.game = game
        self.pos = Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.time_alive = 0

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color("green"), self.pos, REWARD_SIZE)
        self.time_alive += self.game.delta_time
        if self.time_alive > 5:
            self.new_pos()
            self.time_alive = 0

    def new_pos(self):
        self.pos = Vector2(random.randint(REWARD_SIZE, WIDTH - REWARD_SIZE), random.randint(REWARD_SIZE, HEIGHT - REWARD_SIZE))
