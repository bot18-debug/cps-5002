import tkinter as tk 
CELL_SIZE = 30 
GRID_SIZE = 20 

class Environment :
    def __init__(self):
        self.agents = []
        self.window = tk.Tk()
        self.window.title("predator-prey simulation")
        self.canvas = tk.Canvas(self.window, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE)
        self.canvas.pack()
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
                    self.canvas.create_rectangle(
    x1, y1, x2, y2,
    fill="#E5E5E5",   # your ashy white
    outline="gray",  # border color
    width=5
)
            for agent in self.agents:
                agent .draw(self.canvas)
    def start(self):
            self.update()
            self.window.mainloop()

    def update(self):
            for agent in self.agents:
                agent.take_turn()
            self.draw_grid()
            self.window.after(500, self.update)
