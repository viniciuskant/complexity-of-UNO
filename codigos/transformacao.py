import networkx as nx
import matplotlib.pyplot as plt
import json

def plotar_grafo(grafo):
    nx.draw(grafo, with_labels=True, node_size=500, node_color='lightblue', font_size=4, font_weight='bold', edge_color='gray')
    plt.show()

def carregar_grafo_de_json(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return json.load(f)

def transformar_grafo_cubico(grafo_json):
    n_vertices = grafo_json["n_vertices"]
    adjacencia = grafo_json["adjacencia"]
    
    grafo_primeiro = {}
    novo_vertices = {}
    novo_arestas = []

    # Criar vértices (v, e) para cada aresta incidente em v
    for v, vizinhos in adjacencia.items():
        v = int(v)
        
        for y in vizinhos:
            e = tuple(sorted([v, y]))
            novo_vértice = (v, e)
            if novo_vértice not in novo_vertices:
                novo_vertices[novo_vértice] = []

    # Adicionar arestas entre os triângulos
    for v, vizinhos in adjacencia.items():
        v = int(v)
        arestas_incidentes = [(v, tuple(sorted([v, y]))) for y in vizinhos]
        for i in range(len(arestas_incidentes)):
            for j in range(i + 1, len(arestas_incidentes)):
                novo_arestas.append((arestas_incidentes[i], arestas_incidentes[j]))

    for v1 in novo_vertices:
        for v2 in novo_vertices:
            if v1[1] == v2[1] and v1[0] != v2[0]:  # Verifica se os dois vértices são parte do mesmo triângulo
                novo_arestas.append((v1, v2))  # Conectar vértices de triângulos

    # Criar o grafo transformado
    grafo_transformado = nx.Graph()
    
    # Adicionar os vértices e as arestas no grafo
    for vertice in novo_vertices:
        grafo_transformado.add_node(vertice)
    
    for aresta in novo_arestas:
        grafo_transformado.add_edge(aresta[0], aresta[1])

    return grafo_transformado

def salvar_grafo_em_arquivo_json(grafo, nome_arquivo):
    n_vertices = len(grafo.nodes)
    n_arestas = len(grafo.edges)
    adjacencia = {str(v): list(map(str, list(grafo.neighbors(v)))) for v in grafo.nodes}
    
    grafo_json = {
        "n_vertices": n_vertices,
        "n_arestas": n_arestas,
        "adjacencia": adjacencia
    }
    
    with open(nome_arquivo, 'w') as f:
        json.dump(grafo_json, f, indent=4)
    print(f"Grafo salvo em {nome_arquivo}")

# Exemplo de uso
grafo_json = carregar_grafo_de_json('grafo_cubico.json')
grafo_transformado = transformar_grafo_cubico(grafo_json)
plotar_grafo(grafo_transformado)
salvar_grafo_em_arquivo_json(grafo_transformado, 'grafo_transformado.json')
