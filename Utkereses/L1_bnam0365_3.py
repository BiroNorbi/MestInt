class Node:
    def __init__(self, x, y, z, barrier):
        self.x = x
        self.y = y
        self.z = z
        self.barrier = barrier
        self.parent = None
        self.f = 0
        self.g = float('inf')
        self.h = float(0)

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z}, {self.barrier})"
