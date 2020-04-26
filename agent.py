import pygame
import random

import settings

w_width = settings.w_width
w_height = settings.w_height
square_size = settings.square_size
agent_size = square_size
max_life = 100

class Agent:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.life = max_life
        self.alive_time = 0

        self.type = "Agent"
        self.c = (255,0,255)

    def eat(self, grid):
        c = grid.get_cell(self.x,self.y) 
        if (c.type == "Grass"):
            if (c.life > 10):
                c.life -= 10
                self.life += 10
                return 10
            return 0
        elif (c.type == "Water"):
            self.life -= 1
            return -1
        elif (c.type == "Lava"):
            self.life -= 10
            return -10
        elif (c.type == "Square"):
            return 0

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

        # Sanity checks
        if(self.x <= 0):
            self.x = w_width - agent_size
        if(self.y <= 0):
            self.y = w_height - agent_size
        if (self.x + agent_size > w_width):
            self.x = 0
        if (self.y + agent_size > w_height):
            self.y = 0

    def live(self, grid, reward):
        # The brains of the agent
        c = grid.get_cell(self.x,self.y)

        # Calculate delta_x and delta_y
        delta_x = 0
        delta_y = 0
        if(random.random() < 0.01):
            delta_x = agent_size
        if(random.random() < 0.02):
            delta_x = -agent_size
        if(random.random() < 0.03):
            delta_y = agent_size
        if(random.random() < 0.04):
            delta_y = -agent_size
        self.move(delta_x,delta_y)

    def run(self, grid):
        self.life -= 1
        self.alive_time += 1
        if (self.life > max_life):
            self.life = max_life

        reward = self.eat(grid)
        self.live(grid, reward)

    def draw(self,screen):
        pygame.draw.circle(screen, self.c, (self.x, self.y), agent_size//2)