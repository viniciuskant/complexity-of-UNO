'''
Gera um grafo cúbico aleatório com n vértices e salva em um arquivo JSON.
'''

import networkx as nx
import matplotlib.pyplot as plt
import json

def criar_grafo_cubico_aleatorio(n):
    if n % 2 != 0:
        raise ValueError("O número de vértices (n) deve ser par para criar um grafo cúbico")

    grafo = nx.random_regular_graph(3, n)
    return grafo

def plotar_grafo(grafo):
    nx.draw(grafo, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    plt.show()
    plt.savefig("grafo_cubico.png")

def exportar_grafo_para_json(grafo):
    n_vertices = len(grafo.nodes)
    n_arestas = len(grafo.edges)
    adjacencia = {node: list(grafo.neighbors(node)) for node in grafo.nodes}
    grafo_json = {
        "n_vertices": n_vertices,
        "n_arestas": n_arestas,
        "adjacencia": adjacencia
    }
    return grafo_json

def salvar_grafo_em_arquivo_json(grafo_json, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        json.dump(grafo_json, f, indent=4)
    print(f"Grafo salvo em {nome_arquivo}")

n = int(input("Digite o número de vértices: "))
grafo = criar_grafo_cubico_aleatorio(n)

grafo_json = exportar_grafo_para_json(grafo)
salvar_grafo_em_arquivo_json(grafo_json, 'grafo_cubico.json')
plotar_grafo(grafo)
