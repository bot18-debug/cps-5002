from environment import Environment
from predator import Predator
from android import Android
from monster import Monster 
import time 

from wildlife import Wildlife
from ultimate_adversary import UltimateAdversary
import random



def main():

    print("Starting Predator: Badlands Simulation...")


    env = Environment()

    dek = Predator("Dek", env)
    thia = Android("Thia", env)
    beast = Monster("Beast", env)
    boss = UltimateAdversary("Kraken", env)

    father = Predator("Father", env, is_dek=False)
    brother = Predator("Brother", env, is_dek=False)
    monsters = []
    for i in range(3):
        monster = Monster(f"Monster_{i+1}", env)
        monsters.append(monster)
    for i in range(3):
        wildlife = Wildlife(f"Wildlife_{i+1}", env)
        env.add_agent(wildlife)




    env.add_agent(dek)
    env.add_agent(thia)
    env.add_agent(beast)
    env.add_agent(boss)
    env.add_agent(father)
    env.add_agent(brother)

    for monster in monsters:
        env.add_agent(monster)

    print("\nSimulation starting...")
    print("Dek's Goal: Defeat the Ultimate Adversary")
    print("=" * 50)

    env.start()




    env.start()
    

if __name__ == "__main__":
    main()

