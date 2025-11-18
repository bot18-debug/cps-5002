from agent import Agent

class Predator(Agent):
    def __init__(self, name, env):
        super().__init__(name, env, color="green")
