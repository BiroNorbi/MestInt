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

    for x, y in adjacency:
        adjacency[x, y][0].pheromone = random.random() * 1.5 + 1e-3

    return start_point, end_point


def remove_loops(path):
    visited = {}
    new_path = []

    for i, node in enumerate(path):
        if node in visited:
            new_path = new_path[:visited[node] + 1]
        else:
            visited[node] = len(new_path)
            new_path.append(node)

    return new_path


def daemonize_path(paths, best_path):
    new_paths = []
    b_path = remove_loops(best_path)
    for path in paths:
        new_paths.append(remove_loops(path))

    return new_paths, b_path


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
                d_t = distance(last_node_visited.x, last_node_visited.y, last_node_visited.z, end_point.x, end_point.y,
                               end_point.z)
                if 0 < energy < minimal_energy:
                    d, minimal_energy, best_path = d_t, energy, path

        paths, best_path = daemonize_path(paths, best_path)
        update_pheromones(adjacency, paths, energies, best_path, end_point)
        if i % 10 == 0:
            visualize(adjacency, start_point, end_point, best_path, "pheromone")
    return best_path, minimal_energy, d


def construct_ant_path(adjacency, start_point, end_point):
    used_energy, iteration = 0, 0
    path = [start_point]
    visited = {start_point: True}

    while path[-1] != end_point and iteration < 10000:
        current = path[-1]
        visited[current] = True
        next_node, p, e = get_next_node(adjacency, current, end_point, visited)

        path.append(next_node)
        used_energy += e

        if next_node not in visited:
            if next_node.bonus == 1:
                used_energy -= 5
            elif next_node.bonus == -1:
                used_energy += 10

        iteration += 1

        if next_node == end_point:
            print("Ant reach the goal")

    return path, used_energy


def get_next_node(adjacency, current, end_point, visited):
    neighbors = adjacency[current.x, current.y][1]
    probabilities, denominator = [], 0
    data = {}

    for neighbor in neighbors:
        pheromone, heuristic, energy = get_pheromone_and_heuristic_and_energy(adjacency, current, neighbor, end_point)
        data[neighbor] = (pheromone, heuristic, energy)
        denominator += pheromone * heuristic

    for neighbor in neighbors:
        neighbor_data = data[neighbor]
        probability = (neighbor_data[0] * neighbor_data[1]) / denominator
        probabilities.append((neighbor, probability, neighbor_data[2]))

    if sum(p[1] for p in probabilities) == 0:
        return None, 0, float('inf')

    return choose_next_node(probabilities, visited)


def choose_next_node(probabilities, visited):
    unvisited = [prob for prob in probabilities if prob[0] not in visited]

    if len(unvisited) > 0:
        if random.random() < 0.05:
            return max(unvisited, key=lambda p: p[1])
        else:
            nodes = [node[0] for node in unvisited]
            selected_node = np.random.choice(nodes)

            return next((t for t in unvisited if t[0] == selected_node), None)
    else:
        nodes = [node[0] for node in probabilities]
        selected_node = np.random.choice(nodes)
        return next((t for t in probabilities if t[0] == selected_node), None)


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
    heuristic = (1 / (1e-9 + energy + energy_to_goal)) ** params.get_heuristic_influence()

    return pheromone, heuristic, energy


def update_pheromones(adjacency, paths, energies, best_path, end_point):
    q = AOCParameters().get_pheromone_deposit_factor()
    evaporation_rate = AOCParameters().get_pheromone_evaporation()

    for x, y in adjacency:
        adjacency[x, y][0].pheromone *= (1 - evaporation_rate)

    for path, energy in zip(paths, energies):
        if path:
            if path[-1] == end_point:
                for node in path:
                    adjacency[node.x, node.y][0].pheromone += (q / energy) + 0.3
            else:
                for node in path:
                    adjacency[node.x, node.y][0].pheromone += (q / energy)

def calculate_path_energy(path):
    total_energy = 0

    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]
        distance_value = distance(node1.x, node1.y, node1.z, node2.x, node2.y, node2.z)
        energy = calculate_energy(distance_value, node1.z, node2.z, node2.bonus)

        if node2.bonus == 1:
            energy -= 5
        elif node2.bonus == -1:
            energy += 10

        total_energy += energy

    return total_energy


def main():
    adjacency = read_surface("aco_points_512x512.txt")
    start_point, end_point = read_end_points("aco_start_end_512x512.txt", adjacency)

    path, energy, d = aco_algorithm(adjacency, start_point, end_point)
    energy = calculate_path_energy(path)
    print(f"Best energy: {energy}")
    print(f"Distance from the destination: {d}")

    visualize(adjacency, start_point, end_point, path, "pheromone")


if __name__ == '__main__':
    main()
