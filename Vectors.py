import pickle
import numpy as np

def initialize_vectors(inpfile, outfile=None, dim=16, method='normal', mean=0, std=0.1):
    with open(inpfile, 'rb') as f:
        data = pickle.load(f)
    nonterminals = 0
    nonterminal_ids = []
    for i in range(len(data['astnodes'])):
        if data['astnodes'][i][0] not in [1]:
            nonterminals += 1
            nonterminal_ids.append(i)
    nonterminal_ids = np.array([nonterminal_ids]).T
    if method == 'random':
        nonterminal_vectors = np.random.random_sample((nonterminals, 1 + dim))
    elif method == 'normal':
        nonterminal_vectors = np.random.normal(mean, std, (nonterminals, 1 + dim))
    nonterminal_vectors[:, [0]] = nonterminal_ids
    np.save(outfile, nonterminal_vectors)


def update_vectors(relationfile, vectorfile, lr=0.01, epochs=15, method='normal', mean=0, std=0.1):
    nonterminal_vectors = np.load(vectorfile)
    dim = nonterminal_vectors.shape[1] - 1
    with open(relationfile, 'rb') as f:
        relations = pickle.load(f)
    if method == 'random':
        relation_vectors = np.random.random_sample((len(relations), dim))
    elif method == 'normal':
        relation_vectors = np.random.normal(mean, std, (len(relations), dim))
    for _ in epochs:
        for i in range(len(relations)):
            for j in range(nonterminal_vectors.shape[0]):
                rating = 1 if int(nonterminal_vectors[j][0]) in relations[i] else 0
                error = rating - np.dot(relation_vectors[i, :], nonterminal_vectors[j, 1:])
                temp = relation_vectors[i, :]
                relation_vectors[i, :] += lr * error * nonterminal_vectors[j, 1:]
                nonterminal_vectors[j, 1:] += lr * error * temp 
    np.save(vectorfile, nonterminal_vectors)



if __name__ == '__main__':
    initialize_vectors('inline.pkl', 'inline.npy')
    # update_vectors('inline_r.pkl', 'inline.npy')