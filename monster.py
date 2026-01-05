from agent import Agent
from config import COLORS
class Monster(Agent):
    def __init__(self, name, env):
        super().__init__(name, env,  color=COLORS["MONSTER"], initial_health=70, initial_stamina=10)
