import pygame
import random

from materials import *
import settings

w_width = settings.w_width
w_height = settings.w_height
square_size = settings.square_size

def world_builder(x,y):
    r = random.random()
    circle = (x - w_width//2)**2 + (y - w_height//2)**2

    if (r < 0.01):
        return Lava(x,y)
    if (circle < r * 150**2):
        return Square(x,y)
    if (circle < r * 300**2):
        return Grass(x,y)
    else:
        return Water(x,y)

def check_neighbours(x,y,array,types):
    '''
    FIX THIS
    '''
    directions = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
    for direction in directions:
        dx, dy = direction
        n_x = x+dx
        n_y = x+dy
        if (n_x < 0 or n_y < 0):
            continue
        elif (n_x >= w_width//square_size or n_y >= w_height//square_size):
            continue
        else:
            if array[n_x][n_y].type in types:
                types.remove(array[n_x][n_y].type)
        if len(types) == 0: return True
    return False



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
    
    def rules(self,x,y):
        cell = self.cells[x][y]
        if cell.type == "Grass":
            if cell.life == 0:
                self.cells[x][y] = Soil(x*square_size,y*square_size)
        elif cell.type == "Soil":
            if check_neighbours(x,y,self.cells, ["Grass", "Water"]):
                self.cells[x][y] = Water(x*square_size, y*square_size)
        elif cell.type == "Water":
            if check_neighbours(x,y,self.cells, ["Lava"]):
                self.cells[x][y] = Square(x*square_size, y*square_size)
        elif cell.type == "Lava":
            if check_neighbours(x,y,self.cells, ["Water", "Water", "Water"]):
                self.cells[x][y] = Water(x*square_size, y*square_size)


    def run(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.cells[i][j].run()
                #if (random.random() < 0.01):
                #self.rules(i,j)
    
    def draw(self,screen):
        for i in self.cells:
            for c in i:
                c.draw(screen)

    def get_cell(self,x,y):
        # Convert the world position into cell position 
        x = x//square_size
        y = y//square_size

        s = self.cells[x][y]
        return s 

    def set_cell(self,x,y,life):
        x = x//square_size
        y = y//square_size

        s = self.cells[x][y]
        s.life -= life;
        self.cells[x][y].r = 255