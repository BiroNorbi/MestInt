"""
K-Nearest Neighbors (KNN) Classifier
"""

import heapq
from queue import PriorityQueue

from L2_bnam0365_2 import euclidean_distance, cosine_similarity
from L2_bnam0365_4 import CharacterRepresentation
from OCR.L2_bnam0365_1 import read_input


class KNN:
    def __init__(self):
        self.data = []

    def train(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                self.data.append(CharacterRepresentation(int(parts[-1]), list(map(int, parts[:-1]))))

    def classify(self, data, k=5, distance=euclidean_distance):
        priority_queue = PriorityQueue()

        for character_representation in self.data:
            dist = distance(data, character_representation.representation)
            priority_queue.put((dist, character_representation.character))

        neighbors = []

        for i in range(k):
            neighbors.append(priority_queue.get())

        return max(n[1] for n in neighbors)

    def test(self, filename, distance=euclidean_distance):
        with open(filename, 'r') as file:
            lines = file.readlines()
            ok = 0
            all = 0

            for line in lines:
                parts = line.strip().split(",")
                character = int(parts[-1])
                representation = list(map(int, parts[:-1]))
                all += 1
                num = self.classify(representation, distance=distance)
                if num == character:
                    ok += 1

        return ok / all * 100


def main():
    knn = KNN()
    knn.train("optdigits.tra")

    test = knn.test("optdigits.tes")
    print(f"Test accuracy with euclidean distance: {test:.2f}%")

    training = knn.test("optdigits.tra")
    print(f"Training accuracy with euclidean distance: {training:.2f}%")

    test = knn.test("optdigits.tes", distance=cosine_similarity)
    print(f"Test accuracy with cosinus similarity: {test:.2f}%")

    training = knn.test("optdigits.tra", distance=cosine_similarity)
    print(f"Training accuracy with cosinus similarity: {training:.2f}%")


if __name__ == '__main__':
    main()
