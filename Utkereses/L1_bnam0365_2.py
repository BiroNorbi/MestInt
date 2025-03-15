from math import sqrt


def distance(x1, y1, z1, x2, y2, z2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def manhattan(x1, y1, z1, x2, y2, z2):
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def heuristic_function_distance(p1, p2):
    return distance(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z)


def heuristic_function_manhattan(p1, p2):
    return manhattan(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z)

def minimal_step(x1,y1,z1,x2,y2,z2):
    if abs(x1 - x2) < 2 and abs(y1- y2) < 2:
        return 1
    return 0