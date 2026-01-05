import tkinter as tk 
import random
from config import GRID_SIZE, CELL_SIZE, EMPTY, ROCK, STATUS_HEIGHT,COLORS


class Environment :
    
    def __init__(self):

        self.agents = []  
        self.traps = []    
        self.turn_count = 0
        
        # Main frame for grid
        self.window = tk.Tk() 
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack()
        self.grid_data = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Canvas for the grid
        self.canvas = tk.Canvas(self.main_frame, 
                               width=CELL_SIZE*GRID_SIZE, 
                               height=CELL_SIZE*GRID_SIZE)
        self.canvas.pack()
        
        # Status bar frame at the bottom
        self.status_frame = tk.Frame(self.window, height=STATUS_HEIGHT, 
                                     relief=tk.RAISED, borderwidth=2)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status labels
        self.status_label = tk.Label(self.status_frame, 
                                     text="Simulation Started", 
                                     font=("Arial", 12, "bold"))
        self.status_label.pack(pady=5)
        
        # Agent info frame
        self.agent_info_frame = tk.Frame(self.status_frame)
        self.agent_info_frame.pack(fill=tk.X, padx=10)
        
        # Create labels for each agent
        self.agent_labels = {}
        
        # Turn counter
        self.turn_counter = 0
        self.turn_label = tk.Label(self.status_frame, 
                                   text=f"Turn: {self.turn_counter}", 
                                   font=("Arial", 10))
        self.turn_label.pack(side=tk.LEFT, padx=20)
        
        # Alive agents counter
        self.alive_label = tk.Label(self.status_frame, 
                                    text="Alive: 0", 
                                    font=("Arial", 10))
        self.alive_label.pack(side=tk.RIGHT, padx=20)

        self.populate_initial_map()
        self.create_traps() 
    def update_status_bar(self):
        # Update turn counter
        self.turn_counter += 1
        self.turn_label.config(text=f"Turn: {self.turn_counter}")
        
        # Update alive agents counter
        alive_count = len([a for a in self.agents if a.health > 0])
        self.alive_label.config(text=f"Alive: {alive_count}")
        
        # Update individual agent labels
        for agent in self.agents:
            if agent.name in self.agent_labels:
                 status_color = "red" if agent.health <= 20 else "black"
                 label_text = f"{agent.name}: H:{agent.health} S:{agent.stamina}"
                 if agent.health <= 0:
                    label_text += " [DEAD]"
                
                 self.agent_labels[agent.name].config(
                     text=label_text,
                    fg=status_color
                )

    def create_traps(self):
         print("Creating traps...")
         for _ in range(10):
            while True:
                r = random.randint(0, GRID_SIZE - 1)
                c = random.randint(0, GRID_SIZE - 1)
                # Only place in empty cells, not on rocks or where agents start
                if self.grid_data[r][c] == EMPTY:
                    self.traps.append((r, c))
                    break

    def check_trap(self, agent):
         for trap in self.traps:
            if agent.row == trap[0] and agent.col == trap[1]:
                # Trigger trap
                damage = random.randint(10, 20)
                agent.health -= damage
                agent.stamina -= 5
                print(f"⚠️  {agent.name} stepped on a trap! Lost {damage} health.")
                self.traps.remove(trap)  # Trap is now triggered
                return True
            return False
                status_color = "red" if agent.health <= 20 else "black"
                label_text = f"{agent.name}: H:{agent.health} S:{agent.stamina}"
                if agent.health <= 0:
                    label_text += " [DEAD]"
                
                self.agent_labels[agent.name].config(
                    text=label_text,
                    fg=status_color
                )
        
        # Update overall status
        if alive_count == 0:
            self.status_label.config(text="GAME OVER - All agents are dead", fg="red")
        elif alive_count == 1:
            survivor = [a for a in self.agents if a.health > 0][0]
            self.status_label.config(text=f"Last survivor: {survivor.name}", fg="orange")
        else:
            self.status_label.config(text=f"Simulation running... {alive_count} agents alive", fg="green")
    def populate_initial_map(self, rock_density=0.1):
        """Randomly places rocks on the map."""
        print(f"Creating terrain with {rock_density*100}% rocks...")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if random.random() < rock_density:
                    self.grid_data[r][c] = ROCK

    def is_valid_move(self, r, c):
        # A move is valid if the cell is within bounds and not a rock
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            return self.grid_data[r][c] != ROCK
        return False
    

    def remove_dead_agents(self):
        dead_agents = [agent for agent in self.agents if agent.health <= 0]
        for agent in dead_agents:
                if agent in self.agents:
                    self.agents.remove(agent)
                    print(f"Removed dead agent: {agent.name}")

    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)
            self.update_status_bar()
   
    def create_terrain(self):
      
          self.populate_initial_map()



    def add_agent(self, agent):
        self.agents.append(agent)
        # Create a label for this agent
        label = tk.Label(self.agent_info_frame, 
                        text=f"{agent.name}: H:{agent.health} S:{agent.stamina}",
                        font=("Arial", 8),
                        bg=agent.color if agent.color != "green" else "#90EE90")  # Light green for predator
        label.pack(side=tk.LEFT, padx=10)
        self.agent_labels[agent.name] = label
        self.update_status_bar()
    def draw_grid(self):
            self.canvas.delete("all")
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    x1 = col * CELL_SIZE
                    y1 = row * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    cell_type = self.grid_data[row][col]
                    fill_color = "#E5E5E5" # ash white for EMPTY
                    
                    if cell_type == ROCK:
                        fill_color = "#606060" # Grey for rock/obstacle
                    
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=fill_color,
                        outline="gray",
                        width=1
                    )
            
            for agent in self.agents:
                agent.draw(self.canvas)

            for trap in self.traps:
                r, c = trap
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                      #Draw Red-Black triangle for trap
                self.canvas.create_polygon(
                x1 + 5, y2 - 5,  # Bottom-left
                x1 + 15, y1 + 5,  # Top-middle
                x2 - 5, y2 - 5,   # Bottom-right
                fill=COLORS["TRAP"],
                outline="black"
            )



    def start(self):
            self.update()
            self.window.mainloop()

    def update(self):
            
            self.remove_dead_agents()


            for agent in list(self.agents):

                if agent.is_alive and agent.health > 0:
                    agent.take_turn()
            self.draw_grid()
            self.update_status_bar()
            self.window.after(500, self.update)
            
           


    
