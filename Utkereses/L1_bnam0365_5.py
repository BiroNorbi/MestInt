import time

from L1_bnam0365_1 import read_surface, read_end_points, a_star, write_to_output
from L1_bnam0365_4 import visualize


def main():
    adjacency = read_surface("points_1025.txt")
    #adjacency = read_surface("surface_100x100.txt")
    start_point, end_point = read_end_points("start_end_1025.txt", adjacency)
    #start_point, end_point = read_end_points("surface_100x100.end_points.txt", adjacency)

    start = time.time()
    path = a_star(adjacency, start_point, end_point)
    end = time.time()
    print(f"A* ido: {end - start}")
    paths = [(p.x,p.y) for p in path]
    print(paths)

    start = time.time()
    write_to_output("output_a.txt", path)
    visualize(adjacency, path, "a")
    end = time.time()

    print(f"Render ido: {end - start}")


if __name__ == "__main__":
    main()
