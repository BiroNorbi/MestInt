import random

import numpy as np

from ACO.P1_bnam0365_4 import visualize
from P1_bnam0365_1 import *
from P1_bnam0365_3 import *


def read_surface(filename):
    f = open(filename, "r")
    adjacency = {}
    bonuses = 0

    neighbors_direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for line in f:
        lines = line.strip().split(" ")
        x = int(float(lines[0]))
        y = int(float(lines[1]))
        z = float(lines[2])
        bonus = int(lines[3])

        if bonus == 1:
            bonuses += 5
        elif bonus == -1:
            bonuses -= 10

        point = Node(x, y, z, bonus)
        neighbors = []

        for x_t, y_t in neighbors_direction:
            try:
                neighbor = adjacency[(x + x_t, y + y_t)]
                neighbors.append(neighbor[0])
                neighbor[1].append(point)
            except KeyError:
                continue
        adjacency[(x, y)] = (point, neighbors)

    f.close()

    return adjacency, bonuses


def read_end_points(filename, adjacency):
    f = open(filename, "r")

    line = f.readline().strip().split(" ")
    x = int(float(line[0]))
    y = int(float(line[1]))
    start_point = adjacency[(x, y)][0]

    line = f.readline().strip().split(" ")
    x = int(float(line[0]))
    y = int(float(line[1]))
    end_point = adjacency[(x, y)][0]

    f.close()

    return start_point, end_point


def aco_algorithm(adjacency, start_point, end_point, bonuses):
    best_path = None
    minimal_energy = float("inf")
    d = float('inf')
    parameters = AOCParameters()

    for i in range(parameters.get_number_of_iterations()):
        paths = []
        energies = []

        for _ in range(parameters.get_number_of_ants()):
            path, energy = construct_ant_path(adjacency, start_point, end_point, bonuses)

            if path:
                paths.append(path)
                energies.append(energy)
                last_node_visited = path[-1]
                d_t = distance(last_node_visited.x, last_node_visited.y, last_node_visited.z, end_point.x, end_point.y,end_point.z)
                if d_t < d:
                    d = d_t
                    minimal_energy = energy
                    best_path = path
        update_pheromones(adjacency, paths, energies, best_path, end_point)
        # print(f"{i + 1}. iteracio, eddigi legkisebb energia: {minimal_energy}")

    return best_path, minimal_energy


def construct_ant_path(adjacency, start_point, end_point, bonuses):
    path = [start_point]
    visited = set(path)

    energy = abs(bonuses) % 10
    used_energy = 0
    iteration = 0

    while path[-1] != end_point and energy > 0 and iteration < 10000:
        current = path[-1]
        next_node, p, e = get_next_node(adjacency, current, visited)
        if next_node is None:
            return None, float('inf')

        energy -= e
        used_energy += e

        path.append(next_node)
        visited.add(next_node)
        iteration += 1

    # energy = calculate_path_energy(adjacency, path)
    return path, used_energy


def calculate_path_energy(adjacency, path):
    energy = 0
    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]
        d = distance(node1.x, node1.y, node1.z, node2.x, node2.y, node2.z)
        energy += calculate_energy(d, node1.z, node2.z)

    return energy


def get_next_node(adjacency, current, visited):
    neighbors = adjacency[current.x, current.y][1]
    probabilities = []
    total_probability = 0
    denominator = 0

    for neighbor in neighbors:
        pheromone_t, heuristic_t, energy_t = get_pheromone_and_heuristic_and_energy(adjacency, current, neighbor,
                                                                                    visited)
        denominator += pheromone_t * heuristic_t

    for next_node in neighbors:
        pheromone, heuristic, energy = get_pheromone_and_heuristic_and_energy(adjacency, current, next_node, visited)
        probability = (pheromone * heuristic) / denominator
        probabilities.append((next_node, probability, energy))
        total_probability += probability

    if total_probability == 0:
        print("Hiba")
        return None, float(0), float('inf')

    return choose_next_node(probabilities)


def choose_next_node(probabilities):
    if random.random() < 0.3:
        return max(probabilities, key=lambda x: x[1])
    else:
        return roulette_wheel_selection(probabilities)


def roulette_wheel_selection(probabilities):
    nodes = [node for (node, _, _) in probabilities]
    probs = [prob for (_, prob, _) in probabilities]

    probs = np.array(probs)

    # probs /= probs.sum()
    # print(probs, probs.sum())
    selected_node = np.random.choice(nodes, p=probs)

    selected_tuple = next((t for t in probabilities if t[0] == selected_node), None)
    return selected_tuple


def get_pheromone_and_heuristic_and_energy(adjacency, node1, node2, visited):
    parameters = AOCParameters()

    pheromone = adjacency[node1.x, node1.y][0].pheromone ** parameters.get_pheromone_influence()
    d = distance(node1.x, node1.y, node1.z, node2.x, node2.y, node2.z)
    energy = calculate_energy(d, node1.z, node2.z)
    heuristic = (1 / energy) ** parameters.get_heuristic_influence()

    return pheromone, heuristic, energy


def update_pheromones(adjacency, paths, energies, best_path, end_point):
    q = AOCParameters().get_pheromone_deposit_factor()
    evaporation_rate = AOCParameters().get_pheromone_evaporation()

    # if best_path is not None:
    #     for node in best_path:
    #         adjacency[node.x, node.y][0].pheromone = (1 - evaporation_rate) * adjacency[node.x, node.y][
    #             0].pheromone + evaporation_rate + 20

    for path, energy in zip(paths, energies):
        for i in range(len(path)):
            node = path[i]

            adjacency[node.x, node.y][0].pheromone = (
                    (1 - evaporation_rate) * adjacency[node.x, node.y][0].pheromone
                    + evaporation_rate * (q / energy)
                    + (1000 / distance(node.x, node.y, node.z, end_point.x, end_point.y, end_point.z))
            )
            #print((10 / distance(node.x, node.y, node.z, end_point.x, end_point.y, end_point.z)))


def main():
    adjacency, bonuses = read_surface("aco_points_512x512.txt")
    start_point, end_point = read_end_points("aco_start_end_512x512.txt", adjacency)

    print(start_point, end_point)
    path, energy = aco_algorithm(adjacency, start_point, end_point, bonuses)
    print(f"Best-energy: {energy}")
    print(path)

    visualize(adjacency, start_point, end_point, path, "pheromone")


if __name__ == '__main__':
    main()
