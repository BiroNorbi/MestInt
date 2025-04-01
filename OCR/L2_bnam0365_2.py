def dot_product(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")

    return sum(a * b for a, b in zip(vector1, vector2))

def euclidean_norm(vector):
    return sum(x ** 2 for x in vector) ** 0.5

def euclidean_distance(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")

    return euclidean_norm((a - b) for a, b in zip(vector1, vector2))

def cosine_similarity(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")

    return -dot_product(vector1, vector2) / (euclidean_norm(vector1) * euclidean_norm(vector2))