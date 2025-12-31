import random
from environment import GRID_SIZE

class Agent:
    def __init__(self, name, env, color,initial_health=100,initial_stamina=20):
        self.name = name
        self.env = env
        
        self.color = color
        
        while True:
            self.row = random.randint(0, GRID_SIZE - 1)
            self.col = random.randint(0, GRID_SIZE - 1)
            if env.is_valid_move(self.row, self.col):
                break

        self.health = initial_health
        self.stamina = initial_stamina
        self.max_health = initial_health
        self.max_stamina = initial_stamina
        self.is_alive = True

    def move_random(self):
        move_cost = 1 
        if self.stamina < move_cost:
            return  # Not enough stamina to move
        direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        dr, dc = direction

        # wrap around
        new_row = (self.row + dr) % GRID_SIZE
        new_col = (self.col + dc) % GRID_SIZE

        if self.env.is_valid_move(new_row, new_col):

            self.stamina -= move_cost
            self.row = new_row
            self.col = new_col 
            return True
        return False


    def take_turn(self):
        if self.health <= 0:
            return  # Agent is dead, cannot take a turn
        if self.stamina <= 5 and self.health <100: #rest adn recover
            self.stamina += 2  # Regain stamina when low
            self.health += 1   # Regain health slowly
            print(f"{self.name} is resting to recover stamina and health.")
        else:
          self.move_random()
          self.resolve_interaction()
        self.stamina = max(0, min(self.stamina, self.max_stamina))
        self.health = max(0, min(self.health, self.max_health))
        if self.health <= 0:
            print(f"💀{self.name} has died.")
            self.env.remove_agent(self)
    def attack(self, target):
        damage = random.randint(5, 15)
        target.health -= damage
        self.stamina -= 2

        if type(self).__name__ == "Predator":
            print(f"🏹 {self.name} attacked {target.name} for {damage} damage.")
        else:
            print(f"👹 {self.name} attacked {target.name} for {damage} damage.")
        
        self.health -= 5

    

    def resolve_interaction(self):
            for other_agent in list(self.env.agents):
                    if other_agent is not self and other_agent.row == self.row and other_agent.col == self.col:
                        is_predator = type(self).__name__ == "Predator"
                        is_monster = type(other_agent).__name__ == "Monster"
                        if is_predator and is_monster:
                            damage = random.randint(5, 15)
                            other_agent.health -= damage
                            self.stamina -= 2
                            print(f"💥 {self.name} (Predator) fought {other_agent.name} (Monster) for {damage} dmg.")
                            self.health -= 5

    def draw(self, canvas):
        x1 = self.col * 30
        y1 = self.row * 30
        x2 = x1 + 30
        y2 = y1 + 30

        canvas.create_rectangle(
            x1, y1, x2, y2, 
            fill=self.color
        )
        canvas.create_text(
            x1 + 15, y1 + 15,
            text=f"H:{self.health}\nS:{self.stamina}",
            fill="white" if self.health > 20 else "black",
            font=("Arial", 6," bold")
        )
            
