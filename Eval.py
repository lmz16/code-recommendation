import numpy as np
import heapq
import pickle

def travel(nodes, ind, start, end):
    tempstart = start
    tempend = end
    if(nodes[ind][1]):
        if((tempstart == -1) or (tempstart > nodes[ind][1])):
            tempstart = nodes[ind][1]
        if((tempend == -1) or (tempend < nodes[ind][1])):
            tempend = nodes[ind][1]
        return tempstart, tempend
    for subnode in nodes[ind][2]:
        if(subnode):
            newstart, newend = travel(nodes, subnode, tempstart, tempend)
            if((tempend == -1) or (newend > tempend)):
                tempend = newend
            if((tempstart == -1) or (newstart < tempstart)):
                tempstart = newstart
    return tempstart, tempend


def print_tokens(nodes, ind, tmap, t):
    start, end = travel(nodes, ind, -1, -1)
    #print(start, end, tmap[start], tmap[end])
    for i in range(tmap[start], tmap[end] + 1):
        print(t[i], end='')
    print()


def recommend(tempvector, targetfilenames, k=10):
    candidates = [[-1, -1, -1] for _ in range(k)]
    for i in range(len(targetfilenames)):
        vectors = np.load(targetfilenames[i] + '.npy')
        similarity = np.matmul(vectors[:, 1:], tempvector.T)
        topkind = heapq.nlargest(k, range(similarity.shape[0]), similarity.take)
        candidates += [[i, int(vectors[j][0]), similarity[j]] for j in topkind]
        newtopkind = heapq.nlargest(k, range(2*k), lambda s: candidates[s][2])
        candidates = [candidates[c] for c in newtopkind]
    return candidates


if __name__ == '__main__':
    nonterminal_vectors = np.load('inline.npy')
    target = 838
    for i in range(nonterminal_vectors.shape[0]):
        if int(nonterminal_vectors[i, 0] == target):
            nodes = [x[1] for x in recommend(nonterminal_vectors[i, 1:], ['inline']) if x[1] != target]
            break
    with open('inline.pkl', 'rb') as f:
        data = pickle.load(f)
    print_tokens(data['astnodes'], target, data['tokens_map'], data['tokens'])
    for node in nodes:
        print('*'*48)
        print_tokens(data['astnodes'], node, data['tokens_map'], data['tokens'])