import pickle
import numpy as np

def structure_relations(inpfile, maxlim=100, minlim=5):
    with open(inpfile, 'rb') as f:
        nodes = pickle.load(f)['astnodes']
    relations = []
    for i in range(len(nodes)):
        if nodes[i][2] != []:
            temp = [i]
            for j in nodes[i][2]:
                if nodes[j][1] == None:
                    temp.append(j)
            if (len(temp) > minlim - 1) and (len(temp) < maxlim + 1):
                relations.append(temp)
    return relations


def call_relations(inpfile):
    with open(inpfile, 'rb') as f:
        data = pickle.load(f)
    functions = {}
    relations = []
    for i in range(len(data['astnodes'])):
        if data['astnodes'][i][0] == 7:
            for j in data['astnodes'][i][2]:
                if data['astnodes'][j][0] == 1:
                    if data['tokens'][data['tokens_map'][data['astnodes'][j][1]]] == '(':
                        funcname = data['tokens'][data['tokens_map'][data['astnodes'][j][1]-1]]
                        functions[funcname] = i
    for i in range(len(data['astnodes'])):
        relation = [i]
        for j in data['astnodes'][i][2]:
            if data['astnodes'][j][0] == 1:
                if data['tokens'][data['tokens_map'][data['astnodes'][j][1]]] in functions:
                    func = functions[data['tokens'][data['tokens_map'][data['astnodes'][j][1]]]]
                    if func != i:
                        relation.append(func)  
        if len(relation) > 1:
            relations.append(relation)
    return relations
                    

if __name__ == '__main__':
    relations = structure_relations('inline.pkl') + call_relations('inline.pkl')
    with open('inline_r.pkl', 'wb') as f:
        pickle.dump(relations, f)