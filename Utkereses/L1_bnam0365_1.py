import numpy as np
from numpy.ma.core import minimum

from L1_bnam0365_2 import distance
from L1_bnam0365_3 import *

def heuristic_function(p1, p2):
    return distance(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z)

def read_surface(filename, width, height):
    f = open(filename, "r")
    matrix = np.full((width, height), Node(0, 0, 0, 0), dtype=object)

    for line in f:
        lines = line.strip().split(" ")
        x = int(lines[0])
        y = int(lines[1])
        z = float(lines[2])
        barrier = int(lines[3])
        matrix[x][y] = Node(x, y, z, barrier)

    f.close()

    return matrix

def read_end_points(filename, matrix):
    f = open(filename, "r")

    line = f.readline().strip().split(" ")
    x = int(line[0])
    y = int(line[1])
    start_point = matrix[x][y]

    line = f.readline().strip().split(" ")
    x = int(line[0])
    y = int(line[1])
    end_point = matrix[x][y]

    f.close()

    return start_point, end_point

def reconstruct_path(current):
    path = []

    while current is not None:
        path.append(current)
        current = current.parent

    return path.reverse()

def get_lowest_f_value(open_list):
    node = open_list[0]

    for i in range(1, len(open_list)):
        if open_list[i].f < node.f:
            node = open_list[i]

    return node

def get_neighbors(matrix, node):
    neighbors = []

    for i in range(node.x - 1, node.x + 2):
        for j in range(node.y - 1, node.y + 2):
            if i >= 0 and j >= 0:

                try:
                    neighbor = matrix[i][j]
                    if neighbor != node:
                        neighbors.append(neighbor)
                except IndexError:
                    continue

    return neighbors


def a_star(matrix, start_point, end_point, heuristic=heuristic_function):
    open_list = [start_point]
    closed_list = []

    start_point.g = 0
    start_point.h = heuristic(start_point, end_point)
    start_point.f = start_point.g + start_point.h
    start_point.parent = None

    while open_list:
        current = get_lowest_f_value(open_list)

        if current == end_point:
            return reconstruct_path(current)

        open_list.remove(current)
        closed_list.append(current)

        neighbors = get_neighbors(matrix, current)

        for neighbor in neighbors:
            if neighbor not in closed_list:
                g = current.g + distance(current.x, current.y, current.z, neighbor.x, neighbor.y, neighbor.z)

                if neighbor not in open_list:
                    open_list.append(neighbor)
                elif g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = g
                    neighbor.h = heuristic(neighbor, end_point)
                    neighbor.f = neighbor.g + neighbor.h
    return []

def main():
    matrix = read_surface("surface_100x100.txt", 100, 100)
    start_point, end_point = read_end_points("surface_100x100.end_points.txt", matrix)

    path = a_star(matrix, start_point, end_point)
    print(path)

if __name__ == "__main__":
    main()
