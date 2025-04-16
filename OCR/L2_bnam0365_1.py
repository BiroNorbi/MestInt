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

def display_number(data, title="generated_number.png"):
    heatmap = np.full((8, 8), np.nan)

    for i in range(0,64):
        x = i // 8
        y = i % 8
        heatmap[x,y] = data[i]

    ax = sns.heatmap(
        heatmap, cmap="gray", mask=np.isnan(heatmap), vmin=0, vmax=10,
        cbar_kws={"extend": "both"})
    ax.invert_yaxis()
    plt.savefig(title)
    plt.title("title")
    plt.gca().invert_yaxis()
    plt.show()

def display_euclidean_distance(data, title="euclidean_distance_from_centroid.png"):
    heatmap = np.full((10, len(data)), np.nan)

    for i in range(0,len(data)):
        for j in range(0,10):
            heatmap[j,i] = data[i][j]

    ax = sns.heatmap(
        heatmap, cmap="cividis", mask=np.isnan(heatmap), vmin=0)
    ax.invert_yaxis()
    plt.savefig(title)
    plt.title("Distance from centroid")
    plt.show()

def display_data_cosine_similarity(data, title="cosine_similarity.png"):
    heatmap = np.full((len(data), len(data)), np.nan)

    for i in range(0,len(data)):
        for j in range(0,len(data)):
            heatmap[i,j] = data[i][j]

    ax = sns.heatmap(
        heatmap, cmap="cividis", mask=np.isnan(heatmap),cbar_kws={"extend": "both"})
    ax.invert_yaxis()
    plt.savefig(title)
    plt.title("Cosine Similarity")
    plt.show()