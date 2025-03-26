import random
import numpy as np

from ACO.P1_bnam0365_4 import visualize
from P1_bnam0365_1 import *
from P1_bnam0365_3 import *

def read_surface(filename):
    f = open(filename, "r")
    adjacency = {}

    neighbors_direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for line in f:
        lines = line.strip().split(" ")
        x = int(float(lines[0]))
        y = int(float(lines[1]))
        z = float(lines[2])
        bonus = int(lines[3])

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
    return adjacency

def read_end_points(filename, adjacency):
    f = open(filename, "r")
    line = f.readline().strip().split(" ")
    x, y = int(float(line[0])), int(float(line[1]))
    start_point = adjacency[(x, y)][0]

    line = f.readline().strip().split(" ")
    x, y = int(float(line[0])), int(float(line[1]))
    end_point = adjacency[(x, y)][0]
    f.close()

    return start_point, end_point

def aco_algorithm(adjacency, start_point, end_point):
    best_path, minimal_energy, d = None, float("inf"), float("inf")
    parameters = AOCParameters()

    for i in range(parameters.get_number_of_iterations()):
        paths, energies = [], []

        for _ in range(parameters.get_number_of_ants()):
            path, energy = construct_ant_path(adjacency, start_point, end_point)
            if path:
                paths.append(path)
                energies.append(energy)
                last_node_visited = path[-1]
                d_t = distance(last_node_visited.x, last_node_visited.y, last_node_visited.z, end_point.x, end_point.y, end_point.z)
                if 0 < energy < minimal_energy:
                    d, minimal_energy, best_path = d_t, energy, path

        update_pheromones(adjacency, paths, energies, best_path, end_point)
    return best_path, minimal_energy, d

def construct_ant_path(adjacency, start_point, end_point):
    path = [start_point]
    used_energy, iteration = 0, 0

    while path[-1] != end_point and iteration < 2000:
        current = path[-1]
        next_node, p, e = get_next_node(adjacency, current, end_point)
        if next_node is None:
            return None, float('inf')

        used_energy += e
        path.append(next_node)
        iteration += 1

    return path, used_energy

def get_next_node(adjacency, current, end_point):
    neighbors = adjacency[current.x, current.y][1]
    probabilities, denominator = [], 0

    for neighbor in neighbors:
        pheromone, heuristic, energy = get_pheromone_and_heuristic_and_energy(adjacency, current, neighbor, end_point)
        denominator += pheromone * heuristic

    for neighbor in neighbors:
        pheromone, heuristic, energy = get_pheromone_and_heuristic_and_energy(adjacency, current, neighbor, end_point)
        probability = (pheromone * heuristic) / denominator
        probabilities.append((neighbor, probability, energy))

    if sum(p[1] for p in probabilities) == 0:
        return None, 0, float('inf')

    return choose_next_node(probabilities)

def choose_next_node(probabilities):
    if random.random() < 0.6:
        return max(probabilities, key=lambda x: x[1])
    else:
        return roulette_wheel_selection(probabilities)

def roulette_wheel_selection(probabilities):
    nodes, probs = [node for (node, _, _) in probabilities], [prob for (_, prob, _) in probabilities]
    probs = np.array(probs) / sum(probs)
    selected_node = np.random.choice(nodes, p=probs)
    return next((t for t in probabilities if t[0] == selected_node), None)

def get_pheromone_and_heuristic_and_energy(adjacency, node1, node2, end_point):
    params = AOCParameters()
    pheromone = adjacency[node1.x, node1.y][0].pheromone ** params.get_pheromone_influence()
    d = distance(node1.x, node1.y, node1.z, node2.x, node2.y, node2.z)
    energy = calculate_energy(d, node1.z, node2.z, node2.bonus)

    distance_to_goal = distance(node2.x, node2.y, node2.z, end_point.x, end_point.y, end_point.z)
    energy_to_goal = calculate_energy(distance_to_goal, node2.z, end_point.z, end_point.bonus)
    heuristic = (1 / (energy_to_goal + 1e-9)) ** params.get_heuristic_influence()

    return pheromone, heuristic, energy

def update_pheromones(adjacency, paths, energies, best_path, end_point):
    q = AOCParameters().get_pheromone_deposit_factor()
    evaporation_rate = AOCParameters().get_pheromone_evaporation()

    for path, energy in zip(paths, energies):
        for i in range(len(path)):
            node = path[i]

            adjacency[node.x, node.y][0].pheromone = (
                    (1 - evaporation_rate) * adjacency[node.x, node.y][0].pheromone
                    + (q / energy)
                    #+ (10000 / (distance(node.x, node.y, node.z, end_point.x, end_point.y, end_point.z) + 1e-5))
            )

def main():
    adjacency = read_surface("aco_points_512x512.txt")
    start_point, end_point = read_end_points("aco_start_end_512x512.txt", adjacency)

    path, energy, d = aco_algorithm(adjacency, start_point, end_point)
    print(f"Best energy: {energy}")
    print(f"Distance from the destination: {d}")

    visualize(adjacency, start_point, end_point, path, "pheromone")

if __name__ == '__main__':
    main()
