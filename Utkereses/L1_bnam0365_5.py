from L1_bnam0365_1 import read_surface, read_end_points, a_star, write_to_output
from L1_bnam0365_4 import visualize


def main():
    matrix = read_surface("surface_100x100.txt", 100, 100)
    start_point, end_point = read_end_points("surface_100x100.end_points.txt", matrix)

    path = a_star(matrix, start_point, end_point)
    write_to_output("output_a.txt", path)
    visualize(matrix, path,"a")

if __name__ == "__main__":
    main()