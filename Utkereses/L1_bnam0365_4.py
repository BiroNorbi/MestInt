import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def heatmap_3d(matrix, path, name):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    x_size, y_size = len(matrix), len(matrix[0])

    X, Y = np.meshgrid(range(y_size), range(x_size))
    Z = np.array([[node.z for node in row] for row in matrix])

    ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8)

    for i in range(x_size):
        for j in range(y_size):
            if matrix[i][j].barrier:
                ax.scatter(j, i, Z[i, j], color="black", marker="x", s=10)

    if path:
        path_x = [p.y for p in path]
        path_y = [p.x for p in path]
        path_z = [matrix[p.x][p.y].z for p in path]
        ax.plot(path_x, path_y, path_z, 'b-', linewidth=3, label="Path")

        ax.scatter(path_x[0], path_y[0], path_z[0], c='r', marker='o', s=80, label="Start")
        ax.scatter(path_x[-1], path_y[-1], path_z[-1], c='g', marker='o', s=80, label="End")

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Value')
    ax.set_title("3D Heatmap with Path")
    ax.legend()
    plt.savefig(f"{name}-3d-heatmap.png")
    plt.show()


def heatmap_2d(matrix, path, name):
    plt.figure()
    heatmap = np.array([[node.z for node in row] for row in matrix])
    ax = sns.heatmap(heatmap, cmap="coolwarm", linewidth=0.5, linecolor="gray")

    if path:
        path_x = [p.y for p in path]
        path_y = [p.x for p in path]
        plt.plot(path_x, path_y, 'b-', linewidth=2, label="Path")

        plt.scatter(path_x[0], path_y[0], c='r', marker='o', s=80, label="Start")
        plt.scatter(path_x[-1], path_y[-1], c='g', marker='o', s=80, label="End")

    plt.title("2D Heatmap with Path")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.savefig(f"{name}-2d-heatmap.png")
    plt.show()


def plot_3d(matrix, path, name):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    barriers = [node for row in matrix for node in row if node.barrier == 1]
    passable = [node for row in matrix for node in row if node.barrier == 0]

    if passable:
        passable_coords = np.array([(b.x, b.y, b.z) for b in passable])

        if passable_coords.size > 0:
            ax.scatter(passable_coords[:, 0], passable_coords[:, 1], passable_coords[:, 2],
                       c='g', marker='s', s=3, alpha=0.2, label='Passable')

    if barriers:
        barriers_coords = np.array([(b.x, b.y, b.z) for b in barriers])

        if barriers_coords.size > 0:
            ax.scatter(barriers_coords[:, 0], barriers_coords[:, 1], barriers_coords[:, 2],
                       c='k', marker='x', s=10, label='Barriers', alpha=0.3)

    if path:
        paths = np.zeros((len(path), 3))

        for i, p in enumerate(path):
            paths[i] = (p.x, p.y, p.z)

        ax.plot(paths[:, 0], paths[:, 1], paths[:, 2], 'b-', linewidth=3, label='Path', alpha=1)

        start, end = path[0], path[-1]
        ax.scatter(start.x, start.y, start.z, c='r', marker='o', s=50, label='Start')
        ax.scatter(end.x, end.y, end.z, c='b', marker='o', s=50, label='End')

    ax.view_init(elev=30, azim=45)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(f"Ut koltsege: {path[-1].g}")
    ax.legend()
    plt.ion()
    plt.savefig(f"{name}-3d-plot.png")
    plt.show(block=True)


def plot_2d(matrix, path, name):
    plt.figure()

    if path:
        paths = np.zeros((len(path), 2))

        for i, p in enumerate(path):
            paths[i] = (p.x, p.y)

        plt.plot(paths[:, 1], paths[:, 0], 'r-', linewidth=3, label='Path')

        start, end = path[0], path[-1]
        plt.plot(start.y, start.x, 'ro', markersize=8, label='Start')
        plt.plot(end.y, end.x, 'bo', markersize=8, label='End')

    plt.grid(True)
    plt.legend(fontsize=12)
    plt.title(f"Ut koltsege: {path[-1].g}")
    plt.savefig(f"{name}-2d-plot.png")
    plt.show()


def visualize(matrix, path, name):
    heatmap_3d(matrix, path, name)
    heatmap_2d(matrix, path, name)
    plot_2d(matrix, path, name)
    plot_3d(matrix, path, name)
