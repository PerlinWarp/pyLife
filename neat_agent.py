import neat 
from agent2 import *
import numpy as np

class NEAT_agent(Agent2):
    '''
    An agent which uses a LookUpTable as a brain 
    Inputs are RGB of the cell they are on. 
    Ouput is one of, Up, Down, Left or Right 
    '''
    def __init__(self,x,y,grid,brain,ge):
        super().__init__(x,y)
        self.type = "NEAT Agent"
        self.c = (random.randint(0,255),random.randint(0,255),255)

        self.brain = brain
        self.ge = ge

        # Get an inital input
        c = grid.get_cell(self.x,self.y)
        c_n = grid.get_cell(self.infront_x,self.infront_y)
        senses = (self.degrees, c.r, c.g, c.b, c_n.r, c_n.g, c_n.b)
        self.input = senses
        self.last_action = "forward"

    def live(self, grid, reward):
        self.ge.fitness += reward

        last_input = self.input
        # Get our new input 
        c = grid.get_cell(self.x,self.y)
        c_n = grid.get_cell(self.infront_x,self.infront_y)
        self.input = (self.degrees, c.r, c.g, c.b, c_n.r, c_n.g, c_n.b)

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

class Population():
    def __init__(self, grid, screen, genomes, config):
        self.grid = grid
        self.screen = screen
        self.agents = []

        for _, g in genomes:
            net = neat.nn.RecurrentNetwork.create(g, config)
            g.fitness = 0
            x = random.randint(0,w_width-100)
            y = random.randint(0,w_height-100)
            self.agents.append(NEAT_agent(x,y,grid,net,g))


    def run(self):
        if (len(self.agents) > 0):
            for x,agent in enumerate(self.agents):
                if (agent.life < 1):
                    agent.ge.fitness -= 1
                    self.agents.pop(x)
                else:
                    agent.run(self.grid)
                    agent.draw(self.screen) 
            return False 
        else:
            return True              