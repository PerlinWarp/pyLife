import pygame
import numpy as np
import copy
from enum import Enum

import settings
from np_grid import type_to_num

w_width = settings.w_width
w_height = settings.w_height
square_size = settings.square_size
agent_size = square_size
max_life = 100

class State(Enum):
    ALIVE = 0
    ON_FIRE = 1

class Agent():
    def __init__(self,x,y, grid):
        self.x = x
        self.y = y
        self.life = max_life
        self.alive_time = 0

        self.type = "Agent"
        self.c = (255,0,255)
        self.actions = ["left", "right", "forward"]
        self.degrees = 0
        self.infront_x = self.x 
        self.infront_y = self.y + 10 

        self.cell = grid.get_cell(self.x,self.y)
        self.cell_infront = grid.get_cell(self.infront_x, self.infront_y)
        self.spike_extended = False
        self.state = State.ALIVE


    def eat(self):
        # What should happen when you decide to eat the cell infront of you.
        if (self.spike_extended == False):
            return 0
        c = self.cell_infront

        if (c['type'] == type_to_num["Grass"]):
            # Eat the grass
            if (c['life'] > 10):
                c['life'] -= 10
                self.life += 10
                return 10
            return 0 

        elif (c['type'] == type_to_num["Agent"]):
            # Find the agent we just attacked
            if self.life > c['life']:
                # Eat the other agent
                self.life += 20
                return 20
            else:
                # Get attacked
                self.life -= 20
                return -20         
        return 0

    def interact(self):
        # What should happen when you step on a cell of a certain type
        c = self.cell 

        if (c['type'] == type_to_num["Grass"]):
            return 0

        elif (c['type'] == type_to_num["Water"]):
            self.life -= 2
            if self.state == State.ON_FIRE:
                self.state = State.ALIVE
                return 50

            return -2

        elif (c['type'] == type_to_num["Lava"]):
            self.life -= 10

            if self.state == State.ALIVE:
                # You just set yourself on fire
                self.state = State.ON_FIRE
                return -50
            else:
                return -10

        elif (c['type'] == type_to_num["Rock"] or c['type'] == type_to_num["Soil"]):
            return 0
        elif (c['type'] == type_to_num["Agent"]):
            # Find the agent we just stepped on
            if self.life > c['life']:
                # Eat the other agent
                self.life += 20
                return 20
            else:
                # Get eaten
                self.life -= 20
                return -20 
        else:
            raise ValueError("Unknown cell type", c['type'])

    def live(self, grid, reward):
        if random.random() < 0.5:
            self.spike_extended = not self.spike_extended

        action = random.choice(self.actions)
        self.move(action)

    def run(self, grid):
        # Percieve the world 
        self.cell = copy.deepcopy(grid.get_cell(self.x,self.y))
        old_x, old_y = self.x, self.y
        grid.cells[self.y//square_size][self.x//square_size]['type'] = type_to_num['Agent']
        grid.cells[self.y//square_size][self.x//square_size]['life'] = self.life

        self.cell_infront = grid.get_cell(self.infront_x, self.infront_y)

        # Age 
        self.life -= 1
        self.alive_time += 1
        if (self.life > max_life):
            self.life = max_life

        # Percive our current state and get the reward from the last action 
        reward = self.interact() + self.eat()

        # Decide and make our new action
        self.live(grid, reward)

        # Set the grid back
        grid.cells[old_y//square_size][old_x//square_size] = self.cell

    def move(self, action):
        if (action):
            if (action == "right"):
                self.degrees = (self.degrees + 90) % 360
            elif (action == "left"):
                self.degrees = (self.degrees - 90) % 360
            elif (action == "forward"):
                if (self.degrees == 0):
                    # Move up
                    self.y += agent_size
                elif (self.degrees == 90):
                    # Move right
                    self.x += agent_size
                elif (self.degrees == 180):
                    # Move down
                    self.y -= agent_size
                elif (self.degrees == 270):
                    # Move left
                    self.x -= agent_size

            # Sanity checks
            if(self.x < agent_size//2):
                self.x = w_width - agent_size//2
            elif (self.x + agent_size//2 > w_width):
                self.x = agent_size//2
            if(self.y < agent_size//2):
                self.y = w_height - agent_size//2
            elif (self.y + agent_size//2 > w_height + 1):
                self.y = agent_size//2
                
            # Rotate the end point 
            end_point = np.array([self.x ,self.y])
            r = np.array([[0,-1],
                          [1, 0]])
            n = np.array([0,10])
            for i in range(4-self.degrees//90):
                n = np.dot(r,n)
            end_point += n
            end_vector = end_point.tolist()
            self.infront_x = end_vector[0] % w_width
            self.infront_y = end_vector[1] % w_height

    def draw(self,screen):
        if (self.spike_extended):
            if (abs(self.infront_x - self.x) == agent_size or abs(self.infront_y - self.y) == agent_size ):
                # Dont draw the line if would cut across the screen
                pygame.draw.line(screen, (255,255,255), [self.x, self.y], [self.infront_x, self.infront_y])
        
        if self.state == State.ON_FIRE:
            pygame.draw.circle(screen, (255,0,0), (self.x, self.y), agent_size//2)
        else:
            pygame.draw.circle(screen, self.c, (self.x, self.y), agent_size//2)
