import pygame
import numpy as np
import random
import neat
import os

import settings
from np_grid import Grid
from player_agent import Player


pygame.init()
w_width = settings.w_width
w_height = settings.w_height
square_size = settings.square_size
screen = pygame.display.set_mode((w_width, w_height))
done = False
draw = True

# Making our world
grid = Grid(w_width, w_height, screen)
grid.draw(screen)

# Making an agent
x = w_width//2 + random.randint(1,w_width//square_size//3) * square_size
y = w_height//2 + random.randint(1,w_height//square_size//3) * square_size

player = Player(x,y, grid)
agents = [player]

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if draw:
                            draw = False
                            print("Rendering disabled...")
                        else:
                            print("Rendering enabled...")
                            draw = True

        # Run the world
        grid.run()
        if (draw): grid.draw(screen)

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
                    if (draw): agent.draw(screen)


        pygame.display.flip()