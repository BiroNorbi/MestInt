from OCR.L2_bnam0365_2 import euclidean_distance, cosine_similarity
from OCR.L2_bnam0365_4 import CharacterRepresentation


class Centroid:
    def __init__(self):
        self.data = []
        self.centroids = {}

        for i in range(0, 10):
            self.centroids[i] = ([], [])

    def train(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                character = int(parts[-1])
                representation = list(map(int, parts[:-1]))
                self.data.append(CharacterRepresentation(character, representation))
                self.centroids[character][0].append(representation)

        for i in range(0, 10):
            vectors = self.centroids[i][0]
            representation = vectors[0]

            for j in range(1, len(vectors)):
                representation = [x + y for x, y in zip(representation, vectors[j])]

            representation = [x / len(vectors) for x in representation]

            self.centroids[i] = self.centroids[i][0], representation

    def classify(self, data, distance=euclidean_distance):
        min_distance, i = float("inf"), -1

        for j in range(0, 10):
            dist = distance(data, self.centroids[j][1])
            if dist < min_distance:
                min_distance = dist
                i = j

        return i

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
                num = self.classify(representation, distance)
                if num == character:
                    ok += 1

            return ok / all * 100


def main():
    centroid = Centroid()
    centroid.train("optdigits.tra")

    test = centroid.test("optdigits.tes")
    print(f"Test accuracy with euclidean distance: {test:.2f}%")

    training = centroid.test("optdigits.tra")
    print(f"Training accuracy with euclidean distance: {training:.2f}%")

    test = centroid.test("optdigits.tes", distance=cosine_similarity)
    print(f"Test accuracy with cosinus similarity: {test:.2f}%")

    training = centroid.test("optdigits.tra", distance=cosine_similarity)
    print(f"Training accuracy with cosinus similarity: {training:.2f}%")


if __name__ == '__main__':
    main()
