import heapq

import numpy as np

from L1_bnam0365_2 import distance, heuristic_function_distance
from L1_bnam0365_3 import *
from queue import PriorityQueue

def write_to_output(filename, path):
    f = open(filename, "w")

    f.write(f"{path[-1].g}\n")

    for p in path:
        f.write(f"{p.x} {p.y}\n")

    f.close()


def read_surface(filename):
    f = open(filename, "r")
    adjacency = {}

    neighbors_direction = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for line in f:
        lines = line.strip().split(" ")
        x = int(float(lines[0]))
        y = int(float(lines[1]))
        z = float(lines[2])
        barrier = int(lines[3])
        point = Node(x,y,z,barrier)
        neighbors = []

        for x_t, y_t in neighbors_direction:
            try:
                neighbor = adjacency[(x + x_t,y + y_t)]
                neighbors.append(neighbor[0])
                neighbor[1].append(point)
            except KeyError:
                continue
        adjacency[(x,y)] = (point,neighbors)

    f.close()

    return adjacency


def read_end_points(filename, adjacency):
    f = open(filename, "r")

    line = f.readline().strip().split(" ")
    x = int(float(line[0]))
    y = int(float(line[1]))
    start_point = adjacency[(x,y)][0]

    line = f.readline().strip().split(" ")
    x = int(float(line[0]))
    y = int(float(line[1]))
    end_point = adjacency[(x,y)][0]

    f.close()

    return start_point, end_point


def reconstruct_path(current):
    path = []

    while current is not None:
        path.append(current)
        current = current.parent

    return path[::-1]


def a_star(adjacency, start_point, end_point, heuristic=heuristic_function_distance, cost_function=distance):
    open_queue = [start_point]
    open_dict = {start_point: True}
    closed_set = {}


    start_point.g = 0
    start_point.h = heuristic(start_point, end_point)
    start_point.f = start_point.g + start_point.h
    start_point.parent = None

    while open_dict:
        current = heapq.heappop(open_queue)
        if current == end_point:
            return reconstruct_path(current)

        closed_set[current] = True

        neighbors = adjacency[(current.x, current.y)][1]

        for neighbor in neighbors:
            if neighbor in closed_set or neighbor.barrier == 1:
                continue

            g = current.g + cost_function(current.x, current.y, current.z, neighbor.x, neighbor.y, neighbor.z)

            if neighbor not in open_dict:
                neighbor.parent = current
                neighbor.g = g
                neighbor.h = heuristic(neighbor, end_point)
                neighbor.f = neighbor.g + neighbor.h

                heapq.heappush(open_queue, neighbor)
                open_dict[neighbor] = True
            elif g < neighbor.g:
                neighbor.parent = current
                neighbor.g = g
                neighbor.f = g + neighbor.h
                heapq.heapify(open_queue)

    return []
