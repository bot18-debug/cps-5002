from agent import Agent

class Predator(Agent):
    def __init__(self, name, env, is_dek=False):
        super().__init__(name, env, color="darkgreen", initial_health=120, initial_stamina=40)
        self.honour = 50 if is_dek else 100  # Dek starts with less honour
        self.is_dek = is_dek
        self.is_carrying = False
        self.trophies = 0
        
    def take_turn(self):
        if self.health <= 0:
            self.is_alive = False
            return
        
        # If Dek is carrying Thia, movement costs more
        movement_cost = 2 if self.is_carrying and self.is_dek else 1
        
        if self.stamina < movement_cost:
            self.rest()
        else:
            if self.move_with_purpose():
                self.stamina -= movement_cost
            self.resolve_interaction()
        
        # Clamp values
        self.stamina = max(0, min(self.stamina, self.max_stamina))
        self.health = max(0, min(self.health, self.max_health))
        
        if self.health <= 0 and self.is_alive:
            self.is_alive = False
            print(f"💀 {self.name} has died.")
            if self.is_dek and self.honour < 30:
                print(f"☠️  {self.name} died in dishonour!")
            self.env.remove_agent(self)
    
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