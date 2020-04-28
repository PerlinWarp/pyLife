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

grid = np.zeros((rows, cols, 5), dtype=np.uint8)


        #   "Type":  [Type, R.G,B, Life]
elements = {"Rock":  [0, 128,128,128, 0], 
            "Water": [1,   0,  0,120, 0],
            "Soil":  [2,  97, 63, 16, 0],
            "Grass": [3,  20,100, 20, 100],
            "Lava":  [4, 255,160,  0, 0]
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

        self.cells = [[0 for i in range(self.rows)] for j in range(self.cols)]

        for i in range(0, self.cols):
            for j in range(0, self.rows):
                x = i*square_size
                y = j*square_size
                self.cells[i][j] = world_builder(x,y)

    def run(self):
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                cell = self.cells[x][y]
                if (types[cell[0]] == "Grass"):
                    p = random.random()
                    if (p < 0.4):
                        self.cells[x][y][4] -= 1
                    elif (p < 0.8):
                        self.cells[x][y][4] -= 1
                    # Sanity checks
                    if(cell[4] <= 0):
                        # Convert it to soil
                        self.cells[x][y] = elements["Soil"]
                    elif(cell[4] > 100):
                        self.cells[x][y][4] = 100

        #if (random.random() < 0.01):
        #self.rules(i,j)

    def draw(self,screen):
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                cell = self.cells[x][y]
                c = cell[1:4]
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
        grid.run()
        grid.draw(screen)

        pygame.display.flip()