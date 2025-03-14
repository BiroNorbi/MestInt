from math import sqrt, pow


def distance(x1, y1, z1, x2, y2, z2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2))