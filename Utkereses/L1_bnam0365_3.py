class Node:
    def __init__(self, x, y, z, barrier):
        self.x = x
        self.y = y
        self.z = z
        self.barrier = barrier
        self.parent = None
        self.g = float('inf')
        self.h = float(0)
        self.f = self.g + self.h

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.z}, {self.barrier}, {self.f}, {self.g}, {self.h})"

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __ne__(self, other):
        return self.f != other.f

    def __le__(self, other):
        return self.f <= other.f

    def __ge__(self, other):
        return self.f >= other.f

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.z))