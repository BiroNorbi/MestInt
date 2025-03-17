import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def heatmap_3d(adjacency, path, name):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    x_vals = sorted(set(x for x, y in adjacency.keys()))
    y_vals = sorted(set(y for x, y in adjacency.keys()))

    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.full_like(X, np.nan, dtype=np.float64)

    barrier_x, barrier_y, barrier_z = [], [], []

    for (x, y), (node, _) in adjacency.items():
        xi = x_vals.index(x)
        yi = y_vals.index(y)
        Z[yi, xi] = node.z
        if node.barrier == 1:
            barrier_x.append(x)
            barrier_y.append(y)
            barrier_z.append(node.z)

    ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8)

    if barrier_x:
        ax.scatter(barrier_x, barrier_y, barrier_z, color="black", marker="x", s=10, label="Barriers")

    if path:
        path_coords = np.array([(p.x, p.y, p.z) for p in path])
        ax.plot(path_coords[:, 0], path_coords[:, 1], path_coords[:, 2], 'b-', linewidth=3, label="Path")
        ax.scatter(path_coords[0, 0], path_coords[0, 1], path_coords[0, 2], c='r', marker='o', s=80, label="Start")
        ax.scatter(path_coords[-1, 0], path_coords[-1, 1], path_coords[-1, 2], c='g', marker='o', s=80, label="End")

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Value')
    ax.set_title("3D Heatmap with Path")
    ax.legend(loc="upper right")

    plt.savefig(f"{name}-3d-heatmap.png")
    plt.show()


def heatmap_2d(adjacency, path, name):
    min_x = min(x for x, y in adjacency)
    max_x = max(x for x, y in adjacency)
    min_y = min(y for x, y in adjacency)
    max_y = max(y for x, y in adjacency)

    offset_x = -min_x
    offset_y = -min_y

    heatmap = np.full((max_x - min_x + 1, max_y - min_y + 1), 0)

    for (x, y) in adjacency:
        heatmap[x + offset_x, y + offset_y] = adjacency[x, y][0].z

    plt.figure(figsize=(8, 6))

    ax = sns.heatmap(
        heatmap.T, cmap="coolwarm", mask=np.isnan(heatmap), cbar_kws={"extend": "both"}
    )

    if path:
        path_x = [p.x + offset_y for p in path]
        path_y = [p.y + offset_x for p in path]
        plt.plot(path_x, path_y, 'b-', linewidth=2, label="Path")

        plt.scatter(path_x[0], path_y[0], c='r', marker='o', s=80, label="Start")
        plt.scatter(path_x[-1], path_y[-1], c='g', marker='o', s=80, label="End")

    plt.title("2D Heatmap with Path")
    plt.legend(loc="upper right")
    plt.gca().invert_yaxis()
    plt.show()


def plot_3d(adjacency, path, name):
    x_vals = sorted(set(x for x, y in adjacency.keys()))
    y_vals = sorted(set(y for x, y in adjacency.keys()))

    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.full_like(X, np.nan, dtype=np.float64)

    for (x, y), (node, _) in adjacency.items():
        xi = x_vals.index(x)
        yi = y_vals.index(y)
        Z[yi, xi] = node.z

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, Z, cmap='terrain', alpha=0.7, edgecolor='none')

    if path:
        path_coords = np.array([(p.x, p.y, adjacency[p.x, p.y][0].z) for p in path])
        ax.plot(path_coords[:, 0], path_coords[:, 1], path_coords[:, 2], 'b-', linewidth=3, label='Path')
        ax.scatter(path_coords[0, 0], path_coords[0, 1], path_coords[0, 2], c='r', marker='o', s=50, label='Start')
        ax.scatter(path_coords[-1, 0], path_coords[-1, 1], path_coords[-1, 2], c='b', marker='o', s=50, label='End')

    ax.view_init(elev=30, azim=45)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"Path Cost: {path[-1].g if path else 'N/A'}")
    ax.legend(loc="upper right")

    plt.savefig(f"{name}-3d-surface.png")
    plt.show()


def plot_2d(adjacency, path, name):
    plt.figure()

    if path:
        paths = np.zeros((len(path), 2))
        for i, p in enumerate(path):
            paths[i] = (p.x, p.y)

        barriers = np.array([(x, y) for x, y in adjacency if adjacency[x, y][0].barrier == 1])
        plt.plot(barriers[:, 0], barriers[:, 1], 'x', markersize=4, linewidth=1, label="Barriers")
        plt.plot(paths[:, 1], paths[:, 0], 'r-', linewidth=3, label='Path')
        start, end = path[0], path[-1]
        plt.plot(start.y, start.x, 'ro', markersize=8, label='Start')
        plt.plot(end.y, end.x, 'bo', markersize=8, label='End')

    plt.grid(True)
    plt.legend(loc="upper right", fontsize=12)
    plt.title(f"Ut koltsege: {path[-1].g}")
    plt.savefig(f"{name}-2d-plot.png")
    plt.show()


def visualize(adjacency, path, name):
    plot_2d(adjacency, path, name)
    heatmap_2d(adjacency, path, name)
    heatmap_3d(adjacency, path, name)
    plot_3d(adjacency, path, name)
