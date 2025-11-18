from environment import Environment
from predator import Predator
from android import Android
from monster import Monster 
import time 
def main():
    env = Environment()

    dek = Predator("Dek", env)
    thia = Android("Thia", env)
    beast = Monster("Beast", env)

    env.add_agent(dek)
    env.add_agent(thia)
    env.add_agent(beast)

    env.start()
    

if __name__ == "__main__":
    main()

