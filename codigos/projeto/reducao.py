import matplotlib.pyplot as plt
import networkx as nx
import json

def read_HPC():
    '''
    Função para leitura do grafo cúbico com caminho hamiltoniano.
    '''

    with open('1.json', 'r') as file:
        data = json.load(file)

        print(data)

        v = data["vertices"]
        a = data["arestas"]
        adj = data["adj"]

        print(v, a, adj)

        G = nx.Graph()
        for i in range(1, v + 1):
            G.add_node(i)
        for i in adj.keys():
            v = int(i)
            adj_v = adj[i]
            for u in adj_v:
                G.add_edge(v, u)
        nx.draw(G, with_labels=True)
        plt.show()
    
read_HPC()