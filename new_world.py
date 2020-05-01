import pygame
import numpy as np
import random
import neat
import os

import settings
from np_grid import Grid
from agent import Agent
from player_agent import Player, Player2
import neat_agent


pygame.init()
w_width = settings.w_width
w_height = settings.w_height
screen = pygame.display.set_mode((w_width, w_height))
done = False

# Making our world
grid = Grid(w_width, w_height, screen)
grid.draw(screen)

# Making an agent
player = Player2(w_width//2, w_height//2)
agents = [player]

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        quit()

        # Run the world
        grid.run()
        grid.draw(screen)


        # Run the agents
        for agent in agents:
            if (agent):
                if (agent.life < 1):
                        print("Agent:", agent.type, "died after: ", agent.alive_time)
                        print(len(agents)-1,"still alive")
                        agents.remove(agent)
                        del agent
                else:
                    agent.run(grid)
                    agent.draw(screen)


        pygame.display.flip()