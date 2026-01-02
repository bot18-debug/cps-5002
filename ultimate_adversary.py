from agent import Agent
import random
from config import GRID_SIZE



class UltimateAdversary(Agent):
    def __init__(self, name, env):
        super().__init__(name, env, color="purple", initial_health=200, initial_stamina=60)
        self.rage = 0
        self.territory_radius = 4
        
    def take_turn(self):
        if self.health <= 0:
            self.is_alive = False
            print(f"🎉 ULTIMATE ADVERSARY DEFEATED!")
            return
            
        # Rage increases as health decreases
        self.rage = 100 - self.health
        
        # Seek nearest agent
        nearest_agent = None
        min_distance = float('inf')
        
        for agent in self.env.agents:
            if agent is not self and agent.is_alive:
                distance = abs(agent.row - self.row) + abs(agent.col - self.col)
                if distance < min_distance:
                    min_distance = distance
                    nearest_agent = agent
        
        # Move toward nearest agent
        if nearest_agent and min_distance > 1:
            dr = nearest_agent.row - self.row
            dc = nearest_agent.col - self.col
            
            # Move in direction of nearest agent
            if abs(dr) > abs(dc):
                new_row = (self.row + (1 if dr > 0 else -1)) % GRID_SIZE
                new_col = self.col
            else:
                new_row = self.row
                new_col = (self.col + (1 if dc > 0 else -1)) % GRID_SIZE
            
            if self.env.is_valid_move(new_row, new_col):
                self.row = new_row
                self.col = new_col
                print(f"👣 {self.name} stalks its prey...")
        
        # Rage attack if in territory
        if self.rage > 50:
            damage_bonus = self.rage // 10
            print(f"😡 {self.name} is enraged! +{damage_bonus} damage bonus")
    
    def attack(self, target):
        base_damage = random.randint(15, 30)
        rage_bonus = self.rage // 10
        total_damage = base_damage + rage_bonus
        
        target.health -= total_damage
        print(f"💢 {self.name} unleashes rage attack on {target.name} for {total_damage} damage!")
        
        # Ultimate adversary doesn't take recoil damage