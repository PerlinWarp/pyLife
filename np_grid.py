import random
import numpy as np 
import pygame
import settings

w_width = settings.w_width
w_height = settings.w_height
square_size = settings.square_size

cols = w_width // square_size
rows = w_height // square_size

rows = 4
cols = 3


cells = [[0 for i in range(rows)] for j in range(cols)]

# https://jakevdp.github.io/PythonDataScienceHandbook/02.09-structured-data-numpy.html
grid_dtype = np.dtype({'names':('type', 'r', 'g', 'b', 'life'),
                      'formats':('B', 'B', 'B', 'B', 'B')}
)
print(grid_dtype)
grid = np.zeros((rows, cols), dtype=grid_dtype)

print(grid[0][0]['type'])



        #   "Type":  [Type, R.G,B, Life]
elements = {"Rock":  (0, 128,128,128, 0), 
            "Water": (1,   0,  0,120, 0),
            "Soil":  (2,  97, 63, 16, 0),
            "Grass": (3,  20,100, 20, 100),
            "Lava":  (4, 255,160,  0, 0)
}
types = list(elements.keys())

def world_builder(x,y):
    r = random.random()
    circle = (x - w_width//2)**2 + (y - w_height//2)**2

    if (r < 0.01):
        return elements["Lava"]
    if (circle < r * 150**2):
        return elements["Rock"]
    if (circle < r * 300**2):
        return elements["Grass"]
    else:
        return elements["Water"]

class Grid:
    def __init__(self, w_width, w_height, screen):
        # Draw the grid
        self.cols = w_width // square_size
        self.rows = w_height // square_size

        self.cells = np.zeros((self.rows, self.cols), dtype=grid_dtype)

        for y in range(0, self.rows):
            for x in range(0, self.cols):
                world_x = x*square_size
                world_y = y*square_size
                self.cells[y][x] = world_builder(world_x,world_y)

    def draw(self,screen):
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                cell = self.cells[y][x]
                c = (cell['r'], cell['g'], cell['b'])
                pygame.draw.rect(screen, c, pygame.Rect(x*square_size, y*square_size, square_size, square_size))


pygame.init()
w_width = settings.w_width
w_height = settings.w_height
screen = pygame.display.set_mode((w_width, w_height))
done = False

# Making our world
grid = Grid(w_width, w_height, screen)
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        quit()

        # Run the world
        #grid.run()
        grid.draw(screen)

        pygame.display.flip()