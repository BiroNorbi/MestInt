import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def heatmap_2d(matrix,start, end, path, name):
    plt.figure()
    heatmap = np.array([[node.pheromone for node in row] for row in matrix])
    ax = sns.heatmap(heatmap, cmap="coolwarm", linewidth=0.5, linecolor="gray")

    if path:
        path_x = [p.y for p in path]
        path_y = [p.x for p in path]
        plt.plot(path_x, path_y, 'b-', linewidth=2, label="Path")

        plt.scatter(start.x, start.y, c='r', marker='o', s=80, label="Start")
        plt.scatter(start.x, end.y, c='g', marker='o', s=80, label="End")

    plt.title("2D Heatmap with Path")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.savefig(f"{name}-2d-heatmap.png")
    plt.show()

def visualize(matrix,start, end, path, name):
    heatmap_2d(matrix,start, end , path, name)