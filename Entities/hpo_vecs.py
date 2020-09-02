import os
import numpy as np

class HpoVecs():
    def __init__(self, exp_id): #filename='_data/emb/hp-obo.emb'
        self.filename = '_data/emb/hp-obo_'+exp_id+'.emb'
        self.vecs = self.__load_vectors(self.filename)

    def __load_vectors(self, fn):
        vectors = {}
        with open(fn, 'r') as file:
            line = file.readline()
            vocab_size, vector_size = (int(x) for x in line.split())
            for line_no in range(vocab_size):
                line = file.readline()
                if line == b'':
                    raise EOFError("unexpected end of input; is count incorrect or file otherwise damaged?")
                parts = line.rstrip().split(" ")
                if len(parts) != vector_size + 1:
                    raise ValueError("invalid vector on line %s (is this really the text format?)" % line_no)
                word, weights = int(parts[0]), np.array([np.float32(x) for x in parts[1:]])
                vectors[word] = weights
        return vectors

    def cosine_similarities(self, vector_1, vectors_all):
        norm = np.linalg.norm(vector_1)
        all_norms = np.linalg.norm(vectors_all, axis=1)
        dot_products = np.dot(vectors_all, vector_1)
        similarities = dot_products / (norm * all_norms)
        return similarities

    def distances(self, id, ids=()):
        input_vector = self.vecs[id]
        other_vectors = np.array([self.vecs[ix] for ix in ids])
        return 1 - self.cosine_similarities(input_vector, other_vectors)

    def calc_score(self, ids1, ids2):
        score = 0.0
        for n in range(len(ids1)):
            score += min(self.distances(ids1[n], ids2))
        return score
