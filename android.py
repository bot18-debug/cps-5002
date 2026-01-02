from agent import Agent
from config import GRID_SIZE
import random

class Android(Agent):
    def __init__(self, name, env):
        super().__init__(name, env, color="darkblue", initial_health=80, initial_stamina=0)
        self.is_functional = True
        self.known_threats = []
        self.scan_range = 3
        
    def take_turn(self):
        if not self.is_functional or self.health <= 0:
            return
            
        # Android doesn't move unless carried
        # But can scan environment
        self.scan_environment()
        
        # Try to repair if damaged
        if self.health < 50 and random.random() < 0.3:
            self.health += 5
            print(f"🔧 {self.name} performed self-repair.")
    
    def scan_environment(self):
        """Scan nearby cells for threats and update knowledge"""
        threats = []
        for r in range(max(0, self.row - self.scan_range), 
                      min(GRID_SIZE, self.row + self.scan_range + 1)):
            for c in range(max(0, self.col - self.scan_range), 
                          min(GRID_SIZE, self.col + self.scan_range + 1)):
                for agent in self.env.agents:
                    if agent.row == r and agent.col == c and agent is not self:
                        if type(agent).__name__ in ["Monster", "UltimateAdversary", "Wildlife"]:
                            threats.append((agent.name, r, c))
        
        self.known_threats = threats
        
        # Warn Dek if he's nearby
        for agent in self.env.agents:
            if type(agent).__name__ == "Predator" and agent.is_dek:
                distance = abs(agent.row - self.row) + abs(agent.col - self.col)
                if distance <= 2 and threats:
                    print(f"📡 {self.name} warns Dek: Threat detected at {threats[0][1]},{threats[0][2]}")
    
    def get_threat_info(self):
        """Return formatted threat information"""
        if not self.known_threats:
            return "No immediate threats detected."
        
        info = "Threats detected:\n"
        for threat_name, r, c in self.known_threats[:3]:  # Show top 3 threats
            info += f"- {threat_name} at ({r},{c})\n"
        return info