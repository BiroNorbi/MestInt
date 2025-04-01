import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from OCR.L2_bnam0365_4 import CharacterRepresentation

def read_input(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        data = []
        for line in lines:
            parts = line.strip().split(",")
            data.append(CharacterRepresentation(int(parts[-1]), list(map(int, parts[:-1]))))
    return data

def display_number(data):
    heatmap = np.full((8, 8), np.nan)

    for i in range(0,64):
        x = i // 8
        y = i % 8
        heatmap[x,y] = data[i]

    ax = sns.heatmap(
        heatmap, cmap="gray", mask=np.isnan(heatmap), vmin=0, vmax=10,
        cbar_kws={"extend": "both"})
    ax.invert_yaxis()
    plt.title("Pheromones")
    plt.gca().invert_yaxis()
    plt.show()