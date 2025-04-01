import numpy as np

from OCR.L2_bnam0365_2 import euclidean_distance, euclidean_norm
from OCR.L2_bnam0365_4 import CharacterRepresentation


class GradientDescent:
    def __init__(self):
        self.data = []
        self.w = []
        self.X = []
        self.y = [1,7]

    def train(self, filename, y=None):
        self.data = []
        self.w = []
        self.X = []

        if y is None:
            self.y = [1, 7]
        else:
            self.y = y

        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(',')
                label = int(parts[-1])
                representation = list(map(int, parts[:-1]))

                if label in self.y:
                    self.data.append(CharacterRepresentation(label, representation))
                    self.X.append(list(map(int, parts[:-1])) + [1])

        self.w = [0] * (len(self.data[0].representation) + 1)
        gamma = 7 * 1e-6
        x = np.array(self.X)
        t_x = np.array(self.X).T
        y_l = np.array([-1 if ch.character == self.y[0] else 1 for ch in self.data])
        gradient_norm = 51

        while gradient_norm > 40:
            gradient =  2 * np.dot(t_x, (np.dot(x, self.w) - y_l))
            gradient_norm = euclidean_norm(gradient.T)
            self.w = self.w - (gamma * gradient) / gradient_norm

    def classify(self, data):
        b = self.w[-1]
        w = self.w[:-1]

        return -1 if np.dot(np.array(w).T, np.array(data)) + b < 0 else 1

    def test(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            ok = 0
            all = 0

            for line in lines:
                parts = line.strip().split(',')
                character = int(parts[-1])
                representation = list(map(int, parts[:-1]))
                if character in self.y:
                    all += 1
                    num = self.classify(representation)
                    if character == self.y[1] and num == 1:
                        ok += 1
                    elif character == self.y[0] and num == -1:
                        ok += 1

            return ok / all * 100


def main():
    gradient_descent = GradientDescent()
    y = [1, 7]
    gradient_descent.train("optdigits.tra",y=y)
    test = gradient_descent.test("optdigits.tes")
    print(f"Test accuracy: {test:.2f}%")

    gradient_descent.train("optdigits.tra",y=y)
    training = gradient_descent.test("optdigits.tra")
    print(f"Training accuracy: {training:.2f}%")

if __name__ == "__main__":
    main()