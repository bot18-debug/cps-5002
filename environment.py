import tkinter as tk 
import random

CELL_SIZE = 30 
GRID_SIZE = 20 
EMPTY = 0
ROCK = 1


class Environment :
    def __init__(self):
        self.agents = []
        self.window = tk.Tk()
        self.window.title("predator-prey simulation")
        self.canvas = tk.Canvas(self.window, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE)
        self.canvas.pack()
        self.grid_data = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        self.populate_initial_map()
    def populate_initial_map(self, rock_density=0.1):
        """Randomly places rocks on the map."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if random.random() < rock_density:
                    self.grid_data[r][c] = ROCK

    def is_valid_move(self, r, c):
        # A move is valid if the cell is within bounds and not a rock
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            return self.grid_data[r][c] != ROCK
        return False
    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)
   




    def add_agent(self, agent):
            self.agents.append(agent)
    def draw_grid(self):
            self.canvas.delete("all")
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    x1 = col * CELL_SIZE
                    y1 = row * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    cell_type = self.grid_data[row][col]
                    fill_color = "#E5E5E5" # Default ash white for EMPTY
                    
                    if cell_type == ROCK:
                        fill_color = "#606060" # Grey for rock/obstacle
                    
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=fill_color,
                        outline="gray",
                        width=5
                    )
            
            for agent in self.agents:
                agent.draw(self.canvas)




    def start(self):
            self.update()
            self.window.mainloop()

    def update(self):
            for agent in list(self.agents):
                agent.take_turn()
            self.draw_grid()
            self.window.after(500, self.update)
