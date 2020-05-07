import random
import neat 
import numpy as np
from settings import w_width, w_height, square_size
from agent import *

class NEAT_agent(Agent):
    '''
    An agent which uses a LookUpTable as a brain 
    Inputs are RGB of the cell they are on. 
    Ouput is one of, Up, Down, Left or Right 
    '''
    def __init__(self,x,y,grid,brain,ge):
        super().__init__(x,y,grid)
        self.type = "NEAT Agent"
        self.c = (random.randint(0,255),random.randint(0,255),255)

        self.brain = brain
        self.ge = ge

        # Get an inital input
        c = self.cell
        c_n = grid.get_cell(self.infront_x,self.infront_y)
        senses = (self.degrees, c['r'], c['g'], c['b'], c_n['r'], c_n['g'], c_n['b'])
        self.input = senses
        self.last_action = "forward"

    def live(self, grid, reward):
        self.ge.fitness += reward

        last_input = self.input
        # Get our new input 
        c = self.cell
        c_n = grid.get_cell(self.infront_x,self.infront_y)
        self.input = (self.spike_extended, self.degrees, c['r'], c['g'], c['b'], c_n['r'], c_n['g'], c_n['b'])

        output = self.brain.activate(self.input)

        if output[0] > 0.5:
            super().move("forward")
            self.last_action = "forward"
        if output[1] > 0.5:
            super().move("right")
            self.last_action = "right"
        if output[2] > 0.5:
            super().move("left")
            self.last_action = "left"
        if output[3] > 0.5:
            self.spike_extended = True
        else:
            self.spike_extended = False

class Population():
    def __init__(self, grid, screen, genomes, config):
        self.grid = grid
        self.screen = screen
        self.agents = []

        for _, g in genomes:
            net = neat.nn.RecurrentNetwork.create(g, config)
            g.fitness = 0
            x = w_width//2 + random.randint(1,w_width//square_size//3) * square_size
            y = w_height//2 + random.randint(1,w_height//square_size//3) * square_size
            self.agents.append(NEAT_agent(x,y,grid,net,g))


    def run(self, draw):
        if (len(self.agents) > 0):
            for x,agent in enumerate(self.agents):
                if (agent.life < 1):
                    agent.ge.fitness -= 1
                    self.agents.pop(x)
                else:
                    agent.run(self.grid)
                    if(draw): agent.draw(self.screen) 
            return False 
        else:
            return True              