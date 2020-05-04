import pygame
import numpy as np
import random
import neat
import os

import settings
from np_grid import Grid
from agent import Agent
from player_agent import Player
import neat_agent

# Get the NEAT config file
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config-feedforward.txt")
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)

def main(genomes, config):
    pygame.init()
    w_width = settings.w_width
    w_height = settings.w_height
    screen = pygame.display.set_mode((w_width, w_height))
    done = False
    draw = True


    # Making our world
    grid = Grid(w_width, w_height, screen)
    grid.draw(screen)

    # # Make a population of genetic agents
    genetic_agents = neat_agent.Population(grid, screen, genomes, config)

    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
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

            # Run the genetic agents
            done = genetic_agents.run(draw)

            if (draw): pygame.display.flip()

# Create a population
p = neat.Population(config)

# Stats reporter
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)

winner = p.run(main,500)
# Display the winning genome.
print('\nBest genome:\n{!s}'.format(winner))
