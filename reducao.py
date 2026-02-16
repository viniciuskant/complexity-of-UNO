import matplotlib.pyplot as plt
import networkx as nx
import json

from typing import Tuple
from pprint import pprint

def verifica_HP(G:nx.Graph, path:list, isHPC:bool) -> None:
    """Verifica se o caminho é hamiltoniano.

    Params:
        G (nx.Graph): Grafo.
        path (list): Caminho hamiltoniano de G.
        isHPC (bool): Se o grafo é cúbico ou não.

    Raises:
        ValueError: Se o caminho não for válido.
    """
    if len(path) != len(G.nodes):
        raise ValueError("Caminho inválido: há vértices que não estão no caminho.")
    
    for v in G.nodes:
        if v not in path:
            raise ValueError("Caminho inválido: há vértices que não estão no caminho.")
        if isHPC and len(G[v]) != 3:
            raise ValueError("Caminho inválido: o vértice {} não tem grau 3.".format(v))
    
    if isHPC:
        print("Grafo HPC: O caminho fornecido é hamiltoniano.")
    else:
        print("Grafo UNO: O caminho fornecido é hamiltoniano.")
    
def read_HPC(nome_arquivo) -> Tuple[nx.Graph, list]:
    """Lê um arquivo JSON com um grafo cúbico e um caminho hamiltoniano.

    Params:
        nome_arquivo (str): Nome do arquivo JSON.

    Returns:
        nx.Graph: Grafo cúbico.
        list: Caminho hamiltoniano.
    
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
    """

    with open(nome_arquivo, 'r') as file:
        data = json.load(file)

        n_vertices = data["vertices"]
        adj = data["adj"]

        G = nx.Graph()

        for i in range(1, n_vertices + 1):
            G.add_node(i)
        for i0 in adj.keys():
            i = int(i0)
            for j in adj[i0]:
                if i != j:
                    G.add_edge(i, j)

        nx.draw(G, with_labels=True, font_color=(0, 0, 0), node_color=(0.7, 0.77, 0.95), node_size=1400, font_size=20)
        plt.show()

        return G, data["caminho"]
    
def reducao(G:nx.Graph, path:list) -> Tuple[nx.Graph, list]:
    """Transforma uma instância de HPC em uma instância de Caminho Hamiltoniano para garfos de linha de garfos bipartidos.
    
    Params:
        G (nx.Graph): Grafo cúbico.
        path (list): Caminho hamiltoniano de G.

    Returns:
        nx.Graph: Novo grafo.
        list: Caminho hamiltoniano do novo grafo. 
    
    """

    new_G = nx.Graph()
    new_path = []

    # Adiciona arestas ao novo grafo
    for x, y in G.edges:
        new_G.add_edge((x, (x, y)), (y, (x, y)))

    # Adiciona arestas entre vértices de mesmo x para formar um clique
    for x0, e0 in new_G.nodes:
        for x1, e1 in new_G.nodes:
            if x0 == x1 and e0 != e1:
                new_G.add_edge((x0, e0), (x1, e1))

    nx.draw(new_G, with_labels=True, font_color=(0, 0, 0), node_color=(0.7, 0.77, 0.95), node_size=1400, font_size=20)
    plt.show()

    # Cria o novo caminho hamiltoniano
    i = 0
    arruma = lambda x0, x1: (x1, x0) if x0 > x1 else (x0, x1)
    for i in range(0, len(path)):
        if i == 0 or i == 1:
            v1 = path[i]
            v2 = path[i + 1]
            adj_v1 = list(G[v1])
            adj_v1.remove(v2)
            e1 = arruma(v1, adj_v1[0])
            e2 = arruma(v1, adj_v1[1])
            v1_v2 = arruma(v1, v2)
            if i == 0:
                new_path += [(v1, e1)]
            new_path += [(v1, e2), (v1, v1_v2), (v2, v1_v2)]
        elif i == len(path) - 2 or i == len(path) - 1:
            vn_m1 = path[i - 1]
            vn = path[i]
            adj_vn = list(G[vn])
            adj_vn.remove(vn_m1)
            e1 = arruma(vn, adj_vn[0])
            e2 = arruma(vn, adj_vn[1])
            vn_vn_m1 = arruma(vn, vn_m1)
            if i == len(path) - 1:
                new_path += [(vn, vn_vn_m1)]
            new_path += [(vn, e1), (vn, e2)]
            if i == len(path) - 1:
                break
        else:
            vj_m1 = path[i - 1]
            vj = path[i]
            vj_p1 = path[i + 1]
            adj_vj = list(G[vj])
            adj_vj.remove(vj_m1)
            adj_vj.remove(vj_p1)
            e1 = arruma(vj_m1, vj)
            e2 = arruma(vj, vj_p1)
            e3 = arruma(vj, adj_vj[0])
            new_path += [(vj, e3), (vj, e2), (vj_p1, e2)]
    
    return new_G, new_path

n_teste = int(input("Digite o número do teste: "))

print("Rodando teste {}.json ...".format(n_teste))
G, path = read_HPC("HPC_examples/{}.json".format(n_teste))
verifica_HP(G, path, isHPC=True)
G_uno, path_uno = reducao(G, path)
verifica_HP(G_uno, path_uno, isHPC=False)
pprint(path_uno)


