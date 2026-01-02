from agent import Agent
from config import GRID_SIZE
import random


class Predator(Agent):
    def __init__(self, name, env, is_dek=False):
        if is_dek:
            health = 90
            stamina = 25
        else:
            health = 120
            stamina = 40


        super().__init__(name, env, color="darkgreen", initial_health=health, initial_stamina=stamina)
        self.honour = 30 if is_dek else 80  # lower honour for Dek
        self.is_dek = is_dek
        self.is_carrying = False
        self.trophies = 0
        self.has_met_thia = False
        
    def take_turn(self):
        if self.health <= 0:
            self.is_alive = False
            print(f"💀 {self.name} has died.")
            return
        if self.is_dek:
            self.dek_behavior()
        else:
            self.other_predator_behavior()

        self.handle_interactions()
        self.health = max(0, min(self.health, self.max_health))
        self.stamina = max(0, min(self.stamina, self.max_stamina))
        
    
    def move_with_purpose(self):
        """Dek seeks monsters, others patrol randomly"""
        if self.is_dek:
            # Dek seeks monsters
            for agent in self.env.agents:
                if type(agent).__name__ in ["Monster", "Wildlife", "UltimateAdversary"] and agent.is_alive:
                    dr = agent.row - self.row
                    dc = agent.col - self.col
                    
                    # Move towards monster (simplified)
                    if abs(dr) > abs(dc):
                        new_row = (self.row + (1 if dr > 0 else -1)) % GRID_SIZE
                        new_col = self.col
                    else:
                        new_row = self.row
                        new_col = (self.col + (1 if dc > 0 else -1)) % GRID_SIZE
                    
                    if self.env.is_valid_move(new_row, new_col):
                        self.row = new_row
                        self.col = new_col
                        return True
        
        # Default random movement
        return self.move_random()
    
    def attack(self, target):
        damage = random.randint(8, 20)  # Predators hit harder
        target.health -= damage
        self.stamina -= 3
        
        print(f"🏹 {self.name} hunted {target.name} for {damage} damage.")
        
        # Gain honour for hunting worthy prey
        if target.health <= 0:
            if type(target).__name__ == "UltimateAdversary":
                self.honour += 50
                print(f"🏆 {self.name} gained 50 honour for defeating the Ultimate Adversary!")
            elif type(target).__name__ == "Monster":
                self.honour += 10
                self.trophies += 1
                print(f"⭐ {self.name} gained 10 honour. Trophies: {self.trophies}")
            elif type(target).__name__ == "Wildlife":
                self.honour += 5
                print(f"✨ {self.name} gained 5 honour.")
        
        # Check clan code violations
        if target.health < 20 and type(target).__name__ in ["Monster", "Wildlife"]:
            self.honour -= 5
            print(f"⚠️  {self.name} lost 5 honour for attacking weak prey!")
        
        self.health -= 3  # Less recoil damage for predators
    
    def rest(self):
        self.stamina += 3
        self.health += 2
        print(f"🧘 {self.name} is resting.")
    
    def carry_android(self, android):
        if not self.is_carrying and self.is_dek:
            self.is_carrying = True
            android.row = self.row
            android.col = self.col
            print(f"🤖 {self.name} is carrying {android.name}")
            return True
        return False
    
    def drop_android(self):
        if self.is_carrying:
            self.is_carrying = False
            print(f"🔄 {self.name} stopped carrying.")
            return True
        return False