class Node:
    def __init__(self, x, y, z, bonus):
        self.x = x
        self.y = y
        self.z = z
        self.bonus = bonus
        self.pheromone = 0.001

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.z}, {self.bonus})"