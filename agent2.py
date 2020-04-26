from agent import *
import settings
import numpy as np

w_width = settings.w_width
w_height = settings.w_height
square_size = settings.square_size
agent_size = square_size

class Agent2(Agent):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.type = "Agent2"
        self.actions = ["left", "right", "forward"]
        self.degrees = 0
        self.infront_x = self.x 
        self.infront_y = self.y + 10

    def live(self, grid, reward):
        action = random.choice(self.actions)
        self.move(action)

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
        if (abs(self.infront_x - self.x) == agent_size or abs(self.infront_y - self.y) == agent_size ):
            # Dont draw the line if would cut across the screen
            pygame.draw.line(screen, (255,255,255), [self.x, self.y], [self.infront_x, self.infront_y])
        pygame.draw.circle(screen, self.c, (self.x, self.y), agent_size//2)
