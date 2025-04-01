from math import sqrt

def calculate_energy(d, z1, z2,is_barrier):
    energy = 0.2 * d + 0.1 * (z2 - z1)

    if is_barrier == 1:
        energy -= 5
    elif is_barrier == -1:
        energy += 10

    return energy

def distance(x1, y1, z1, x2, y2, z2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

class AOCParameters:
    def __init__(self):
        self.pheromone_influence = 10
        self.heuristic_influence = 5
        self.pheromone_evaporation = 0.1
        self.pheromone_deposit_factor = 250
        self.number_of_ants = 30
        self.number_of_iterations = 300

    def get_all_parameters(self):
        return self.pheromone_influence, self.heuristic_influence, self.pheromone_evaporation, self.pheromone_deposit_factor, self.number_of_ants, self.number_of_iterations

    def get_pheromone_influence(self):
        return self.pheromone_influence

    def get_heuristic_influence(self):
        return self.heuristic_influence

    def get_pheromone_evaporation(self):
        return self.pheromone_evaporation

    def get_pheromone_deposit_factor(self):
        return self.pheromone_deposit_factor

    def get_number_of_ants(self):
        return self.number_of_ants

    def get_number_of_iterations(self):
        return self.number_of_iterations

    energy = staticmethod(calculate_energy)