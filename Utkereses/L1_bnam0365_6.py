import time

from L1_bnam0365_1 import read_surface, read_end_points, a_star, write_to_output
from L1_bnam0365_2 import heuristic_function_minimal_step, distance, minimal_step
from L1_bnam0365_4 import visualize


def main():
    #adjacency = read_surface("points_1025.txt")
    adjacency = read_surface("surface_100x100.txt")
    #start_point, end_point = read_end_points("start_end_1025.txt", adjacency)
    start_point, end_point = read_end_points("surface_100x100.end_points.txt", adjacency)
    start = time.time()
    path = a_star(adjacency, start_point, end_point, heuristic=heuristic_function_minimal_step, cost_function=minimal_step)
    write_to_output("output_b.txt", path)
    end = time.time()
    print(f"A* ido: {end - start}")

    start = time.time()
    write_to_output("output_a.txt", path)
    visualize(adjacency, path, "a")
    end = time.time()

    print(f"Render ido: {end - start}")

if __name__ == "__main__":
    main()