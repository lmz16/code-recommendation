import json
from Makegraph import Makegraph

with open('result.json', 'r') as f:
    data = json.load(f)

mg = Makegraph()
mg.get_nodes(data['astnodes'])
mg.makegraph_nonterminal()
