from py2neo import Node, Relationship, Graph

class Makegraph:
    def __init__(self):
        self.graph = Graph("http://localhost:7474",auth=("neo4j","Lmz2016011053@"))
        self.graph.delete_all()
        self.input_nodes = []
        self.graph_nodes = []
    

    def get_nodes(self, nodes):
        self.input_nodes = nodes


    def makegraph_nonterminal(self):
        for i in range(len(self.input_nodes)):
            self.graph_nodes.append(Node(str(self.input_nodes[i][0]), node_id=str(i)))
        for i in range(len(self.input_nodes)):
            if(self.input_nodes[i][1] == None):
                self.graph.create(self.graph_nodes[i])
            for j in self.input_nodes[i][2]:
                if(self.input_nodes[j][1] == None):
                    self.graph.create(self.graph_nodes[j])
                    print(i, j)
                    self.graph.create(Relationship(self.graph_nodes[i], self.graph_nodes[j]))