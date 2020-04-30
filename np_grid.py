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
grid = np.zeros((rows, cols), dtype=grid_dtype)


        #   "Type":  [Type, R.G,B, Life]
elements = {"Rock":  (0, 128,128,128, 255), 
            "Water": (1,   0,  0,120, 0),
            "Soil":  (2,  97, 63, 16, 0),
            "Grass": (3,  20,100, 20, 100),
            "Lava":  (4, 255,100,  0, 255)
}
types = list(elements.keys())
type_to_num = {}
for n, t in enumerate(types):
    type_to_num[t] = n


def world_builder(x,y):
    r = random.random()
    circle = (x - w_width//2)**2 + (y - w_height//2)**2

    if (circle < 300 or r < 0.001):
        return elements["Lava"]
    if (circle < r * 150**2):
        return elements["Rock"]
    if (circle < r * 300**2):
        return elements["Grass"]
    if r < 0.01:
        return elements["Soil"]
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

    def count_neighbours(self, c_type):
        """Game of life step using generator expressions"""
        nbrs_count = sum(np.roll(np.roll(self.cells == c_type , i, 0), j, 1)
                         for i in (-1, 0, 1) for j in (-1, 0, 1)
                         if (i != 0 or j != 0))
        return nbrs_count

    def run(self):
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                cell = self.cells[y][x]
                
                if (types[cell['type']] == "Grass"):
                    # Set the colour 
                    self.cells[y][x]['g'] = self.cells[y][x]['life']

                    p = random.random()
                    if (p < 0.4):
                        self.cells[y][x][4] -= 1
                    elif (p < 0.8):
                        self.cells[y][x][4] += 1
                    elif (p > 0.99999):
                        # Lightning Strikes
                        self.cells[y][x] = elements['Lava']
                        self.cells[y][x]['life'] = 1
                        self.cells[y][x]['b'] = 200
                    # Sanity checks
                    if(cell['life'] <= 0):
                        # Convert it to soil
                        self.cells[y][x] = elements["Soil"]
                    elif(cell['life'] > 100):
                        self.cells[y][x]['life'] = 100

                    # If grass is next to lava, set it on fire
                    if ((x + 2 > self.cols) or (y+2 > self.rows)): continue
                    if ((x - 1 < 0) or (y-1 < 0)): continue
                    lava_sum = (self.cells[y-1:y+2,x-1:x+2]['type'] == 4).sum()
                    if lava_sum.sum() > 0 and random.random() < 0.1:
                        self.cells[y][x] = elements["Lava"]
                        self.cells[y][x]['life'] = 2 

                elif (types[cell['type']] == "Soil"):
                    # If soil has more than 3 grass neighbours, make it grass
                    if ((x + 2 > self.cols) or (y+2 > self.rows)): continue
                    if ((x - 1 < 0) or (y-1 < 0)): continue
                    grass_sum = (self.cells[y-1:y+2,x-1:x+2]['type'] == 3).sum()
                    
                    if grass_sum > 2:
                        self.cells[y][x] = elements["Grass"]
                        self.cells[y][x]['life'] = 20
                    elif grass_sum > 0 and random.random() < 0.2:
                        self.cells[y][x] = elements["Grass"]
                        self.cells[y][x]['life'] = 10
                    elif (random.random() < 0.001):
                        self.cells[y][x] = elements["Grass"]
                        self.cells[y][x]['life'] = 5


                
                elif (types[cell['type']] == "Water"):
                    # If water has more than 3 lava neighbours, make it rock
                    if ((x + 2 > self.cols) or (y+2 > self.rows)): continue
                    if ((x - 1 < 0) or (y-1 < 0)): continue
                    lava_sum = (self.cells[y-1:y+2,x-1:x+2]['type'] == 4).sum()

                    if (lava_sum == 0): continue
                    if lava_sum > 5:
                        self.cells[y][x] = elements["Lava"]
                        self.cells[y][x]['life'] = 10   
                    elif lava_sum > 3:
                        self.cells[y][x] = elements["Rock"]
                
                elif (types[cell['type'] == "Lava"]):
                    if cell['life'] == 0:
                        self.cells[y][x] = elements['Soil']
                    elif cell['life'] < 255:
                        cell['life'] -= 1
                        cell['g'] = 0



    def draw(self,screen):
        s = np.stack([self.cells['r'], self.cells['g'], self.cells['b']]).T
        # Stretch the image out
        s = np.repeat(np.repeat(s,10, axis=0), 10, axis=1)
        surf = pygame.surfarray.make_surface(s)
        screen.blit(surf, (0, 0))

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
        grid.run()
        grid.draw(screen)

        pygame.display.flip()