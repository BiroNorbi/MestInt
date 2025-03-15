import random

import numpy as np

from P1_bnam0365_4 import visualize
from P1_bnam0365_1 import *
from P1_bnam0365_3 import *

def read_surface(filename, width, height):
    f = open(filename, "r")
    matrix = np.full((width, height), Node(0, 0, 0, 0), dtype=object)

    for line in f:
        lines = line.strip().split(" ")
        x = int(lines[0])
        y = int(lines[1])
        z = float(lines[2])
        bonus = int(lines[3])
        matrix[x][y] = Node(x, y, z, bonus)

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

def aco_algorithm(matrix, start_point, end_point):
    best_path = None
    minimal_energy = float("inf")
    parameters = AOCParameters()

    for i in range(parameters.get_number_of_iterations()):
        paths = []
        energies = []

        for _ in range(parameters.get_number_of_ants()):
            path, energy = construct_ant_path(matrix, start_point, end_point)

            if path:
                paths.append(path)
                energies.append(energy)

                if energy < minimal_energy:
                    minimal_energy = energy
                    best_path = path
        update_pheromones(matrix, paths, energies)
        #print(f"{i + 1}. iteracio, eddigi legkisebb energia: {minimal_energy}")

    return best_path, minimal_energy

def construct_ant_path(matrix, start_point, end_point):
    path = [start_point]
    visited = set(path)

    iteration = 0

    while path[-1] != end_point and iteration <= 100:
        current = path[-1]
        next_node = get_next_node(matrix, current, visited)

        if next_node is None:
            return None, float('inf')

        path.append(next_node)
        visited.add(next_node)
        iteration += 1

    energy = calculate_path_energy(matrix, path)
    return path, energy

def calculate_path_energy(matrix, path):
    energy = 0
    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]
        d = distance(node1.x,node1.y,node1.z,node2.x,node2.y,node2.z)
        energy += calculate_energy(d, node1.z, node2.z)

    return energy

def get_next_node(matrix, current, visited):
    neighbors = get_neighbors(matrix, current)
    probabilities = []
    total_probability = 0

    for next_node in neighbors:
        if next_node not in visited:
            pheromone, heuristic = get_pheromone_and_heuristic(matrix, current, next_node)
            denominator = 0

            for neighbor in neighbors:
                pheromone_t, heuristic_t = get_pheromone_and_heuristic(matrix, current, neighbor)
                denominator += pheromone_t * heuristic_t

            probability = (pheromone * heuristic) / denominator
            probabilities.append((next_node,probability))
            total_probability += probability

    if total_probability == 0:
        return None

    return choose_next_node(probabilities)

def choose_next_node(probabilities):
    if random.random() < 0.9:
        return max(probabilities, key=lambda x: x[1])[0]
    else:
        return roulette_wheel_selection(probabilities)

def roulette_wheel_selection(probabilities):
    nodes, weights = zip(*probabilities)
    normalized_weights = np.array(weights) / np.sum(weights)
    return np.random.choice(nodes, p=normalized_weights)

def get_pheromone_and_heuristic(matrix, node1, node2):
    parameters = AOCParameters()
    pheromone = matrix[node1.x][node1.y].pheromone ** parameters.get_pheromone_influence()
    d = distance(node1.x, node1.y, node1.z, node2.x, node2.y, node2.z)
    energy = calculate_energy(d, node1.z, node2.z)
    heuristic = (1 / energy) ** parameters.get_heuristic_influence()

    return pheromone, heuristic

def update_pheromones(matrix,paths,energies):
    q = AOCParameters().get_pheromone_deposit_factor()
    evaporation_rate = AOCParameters().get_pheromone_evaporation()

    for path, energy in zip(paths, energies):
        for i in range(len(path)):
            node = path[i]
            matrix[node.x][node.y].pheromone = (1 - evaporation_rate) * matrix[node.x][node.y].pheromone + evaporation_rate * (q / energy)

def main():
    matrix = read_surface("aco_points_512x512.txt", 512, 512)
    start_point, end_point = read_end_points("aco_start_end_512x512.txt", matrix)

    path, energy = aco_algorithm(matrix, start_point, end_point)
    pheromones = [p.pheromone for p in path]
    print(pheromones)
    # visualize(matrix,start_point, end_point ,path, "pheromone")

if __name__ == '__main__':
    main()