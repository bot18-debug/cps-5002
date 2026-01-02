from agent import Agent
from config import GRID_SIZE

class Wildlife(Agent):
    def __init__(self, name, env):
        super().__init__(name, env, color="brown", initial_health=40, initial_stamina=30)
    
    def take_turn(self):
        if self.health <= 0:
            self.is_alive = False
            return
            
        # Wildlife tries to flee from predators
        flee_success = False
        for agent in self.env.agents:
            if type(agent).__name__ == "Predator" and agent.is_alive:
                distance = abs(agent.row - self.row) + abs(agent.col - self.col)
                if distance < 3:  # Predator is close
                    # Move away
                    dr = self.row - agent.row
                    dc = self.col - agent.col
                    
                    new_row = (self.row + (1 if dr > 0 else -1)) % GRID_SIZE
                    new_col = (self.col + (1 if dc > 0 else -1)) % GRID_SIZE
                    
                    if self.env.is_valid_move(new_row, new_col):
                        self.row = new_row
                        self.col = new_col
                        flee_success = True
                        print(f"🐾 {self.name} flees from predator!")
                        break
        
        if not flee_success:
            self.move_random()