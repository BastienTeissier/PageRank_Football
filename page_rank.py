import numpy as np
import json

class PageRank:
    def __init__(self, nodes, vertex):
        self.nodes = nodes
        self.reverse_nodes = {}
        self.build_reverse_nodes()
        self.vertex = vertex
        self.build_graph()
        self.vector = np.ones(len(self.nodes))

    def build_reverse_nodes(self):
        for i in range(len(self.nodes)):
            self.reverse_nodes[self.nodes[i]] = i

    def build_graph(self):
        n = len(self.nodes)
        self.graph = np.zeros((n,n))
        for v in self.vertex:
            self.graph[self.reverse_nodes[v[0]]][self.reverse_nodes[v[1]]]+=1
        self.raw_graph = np.transpose(self.graph)
        self.normalize_graph()

    def normalize_graph(self):
        for l in self.graph:
            temp = 0
            for i in l:
                if i>0:
                    temp+=i
            if temp>0:
                for i in range(len(l)):
                    if l[i]>0:
                        l[i]/=temp
        self.graph = np.transpose(self.graph)

    def iterate(self, iteration):
        for i in range(iteration):
            self.vector = self.graph.dot(self.vector)
        self.score()
        self.classment()
        return self.classment

    def score(self):
        self.score=[]
        for i in range(len(self.vector)):
            self.score.append((self.vector[i],self.nodes[i]))
        #print(self.score)

    def classment(self):
        self.classment = sorted(self.score, key= lambda x: x[0])
        for i in range(len(self.classment)):
            self.classment[i] = (self.classment[i][0], self.classment[i][1], len(self.classment)-i)

    def export_graph(self, url):
        nodes = []
        for c in self.classment:
            nodes.append({"id": c[1], "score": np.asscalar(c[0])*10, "position": c[2]})
        links= []
        for i in range(len(self.raw_graph)):
            for j in range(len(self.graph[i])):
                if self.graph[i][j]>0:
                    links.append({
                        "source": self.nodes[j],
                        "target": self.nodes[i],
                        "value": np.asscalar(self.graph[i][j])
                    })
        ret =  {
            "nodes": nodes,
            "links": links
        }
        with open(url, "w") as f:
            f.write(json.dumps(ret))
