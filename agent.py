import random
from environment import GRID_SIZE

class Agent:
    def __init__(self, name, env, color):
        self.name = name
        self.env = env
        self.row = random.randint(0, GRID_SIZE - 1)
        self.col = random.randint(0, GRID_SIZE - 1)
        self.color = color

    def move_random(self):
        direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        dr, dc = direction

        # wrap around
        self.row = (self.row + dr) % GRID_SIZE
        self.col = (self.col + dc) % GRID_SIZE

    def take_turn(self):
        self.move_random()

    def draw(self, canvas):
        x1 = self.col * 30
        y1 = self.row * 30
        x2 = x1 + 30
        y2 = y1 + 30

        canvas.create_rectangle(
            x1, y1, x2, y2, 
            fill=self.color
        )
