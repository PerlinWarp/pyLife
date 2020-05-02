import pygame
from agent2 import Agent2
import numpy as np

class Player2(Agent2):
    def __init__(self,x,y):
        super().__init__(x,y)
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
        if (pressed[pygame.K_UP] or pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]):
            if pressed[pygame.K_UP]: self.action = "forward"
            if pressed[pygame.K_LEFT]: self.action = "left"
            if pressed[pygame.K_RIGHT]: self.action = "right"
        else:
            super().move(self.action)
            self.action = None