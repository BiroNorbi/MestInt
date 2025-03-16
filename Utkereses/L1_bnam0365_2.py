from math import sqrt


def distance(x1, y1, z1, x2, y2, z2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def heuristic_function_distance(p1, p2):
    return distance(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z)


def heuristic_function_minimal_step(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) +  abs(p1.z - p2.z)


def minimal_step(x1, y1, z1, x2, y2, z2):
    return max(abs(x1 - x2), abs(y1 - y2))
