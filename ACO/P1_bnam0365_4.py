import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def heatmap_2d(adjacency, start, end, path, name):
    min_x = min(x for x, y in adjacency)
    max_x = max(x for x, y in adjacency)
    min_y = min(y for x, y in adjacency)
    max_y = max(y for x, y in adjacency)

    offset_x = -min_x
    offset_y = -min_y

    heatmap = np.full((max_x - min_x + 1, max_y - min_y + 1), np.inf)

    for (x, y) in adjacency:
        heatmap[x + offset_x, y + offset_y] = adjacency[x, y][0].z

    ax = sns.heatmap(
        heatmap.T, cmap="coolwarm", mask=np.isnan(heatmap), cbar_kws={"extend": "both"})

    if path:
        path_x = [p.x + offset_x for p in path]
        path_y = [p.y + offset_y for p in path]
        plt.plot(path_x, path_y, 'b-', linewidth=2, label="Path")

        plt.scatter(start.x, start.y, c='r', marker='o', s=10, label="Start")
        plt.scatter(end.x, end.y, c='g', marker='o', s=10, label="End")

    plt.title("2D Heatmap with Path")
    plt.legend(loc="upper right")
    plt.gca().invert_yaxis()
    plt.show()


def pheromones(adjacency, name):
    min_x = min(x for x, y in adjacency)
    max_x = max(x for x, y in adjacency)
    min_y = min(y for x, y in adjacency)
    max_y = max(y for x, y in adjacency)

    offset_x = -min_x
    offset_y = -min_y

    heatmap = np.full((max_x - min_x + 1, max_y - min_y + 1), np.nan)

    for (x, y) in adjacency:
        heatmap[x + offset_x, y + offset_y] = adjacency[x, y][0].pheromone

    ax = sns.heatmap(
        heatmap.T, cmap=sns.cubehelix_palette(as_cmap=True), mask=np.isnan(heatmap), vmin=0, vmax=10, cbar_kws={"extend": "both"})

    plt.title("Pheromones")
    plt.gca().invert_yaxis()
    plt.show()


def visualize(matrix, start, end, path, name):
    heatmap_2d(matrix, start, end, path, name)
    pheromones(matrix, name)
