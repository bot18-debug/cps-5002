from agent import Agent

class Monster(Agent):
    def __init__(self, name, env):
        super().__init__(name, env, color="red")
