import pygame
from agent import Agent
import numpy as np

class Player(Agent):
    def __init__(self,x,y,grid):
        super().__init__(x,y,grid)
        self.type = "Player2"
        self.c = (255,255,255)
        self.action = None

    def live(self, grid, reward):
        # See the square below us:
        #c = grid.get_cell(self.x,self.y)
        #print("We are on", c.type)

        # Get the square infront of us
        #c = grid.get_cell(self.infront_x,self.infront_y)
        #print(c.type)

        # DEBUG: Infinite life
        #self.life += 10
        
        pressed = pygame.key.get_pressed()
        action = None
        spike = True
        if (pressed[pygame.K_UP] or pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]):
            if pressed[pygame.K_UP]: super().move("forward")
            if pressed[pygame.K_LEFT]: self.action = "left"
            if pressed[pygame.K_RIGHT]: self.action = "right"
        
            if pressed[pygame.K_s]: spike = True

        else:
            super().move(self.action)
            self.action = None

            if spike:
                self.spike_extended = not self.spike_extended
            spike = False
