import networkx as nx
import matplotlib.pyplot as plt
import json

def criar_grafo_cubico_aleatorio(n):
    if n % 2 != 0:
        raise ValueError("O número de vértices (n) deve ser par para criar um grafo cúbico")
    grafo = nx.random_regular_graph(3, n)
    return grafo

def plotar_grafo(grafo, n_font_size):
    nx.draw(grafo, with_labels=True, node_size=500, node_color='lightblue', font_size=n_font_size, font_weight='bold', edge_color='gray')
    plt.show()

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
            y = int(y)
            e = tuple(sorted([v, y]))
            novo_vértice = (v, e)
            if novo_vértice not in novo_vertices:
                novo_vertices[novo_vértice] = []

    # Adicionar arestas entre os triângulos
    for v, vizinhos in adjacencia.items():
        v = int(v)
        arestas_incidentes = [(v, tuple(sorted([v, int(y)]))) for y in vizinhos]
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

def gerar_grafo_com_json_e_salvar_sequencia(json_file, output_file):
    with open(json_file, 'r') as f:
        grafo_json = json.load(f)
    
    G = nx.Graph()
    
    n_vertices = grafo_json["n_vertices"]
    adjacencia = grafo_json["adjacencia"]
    
    cor_dict = {0: 'r', 1: 'g', 2: 'b', 3: 'y'}
    
    sequencia = []
    
    for vertice, vizinhos in adjacencia.items():
        vertice_split = vertice.replace("(", "")
        vertice_split = vertice_split.replace(")", "")
        vertice_split = vertice_split.replace(" ", "")
        vertice_split = [int(x) for x in vertice_split.split(",")]
        cor_idx = int(vertice_split[0]) % 4
        cor = cor_dict[cor_idx]
        label = (int(vertice_split[1]) + vertice_split[2]) % 9
        
        G.add_node(vertice, color=cor, label=label)
        
        for vizinho in vizinhos:
            G.add_edge(vertice, vizinho)
        
        sequencia.append(f"{cor}{label}")
    
    with open(output_file, 'w') as f:
        f.write(",".join(sequencia))

    print(f"Sequência salva no arquivo {output_file}")
    
    plt.figure(figsize=(8, 8))
    
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=False, node_size=700, node_color=node_colors, font_size=12, font_weight='bold', edge_color='gray', width=2)
    
    labels = nx.get_node_attributes(G, 'label')
    label_map = {node: str(G.nodes[node]['label']) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=label_map, font_size=12)
    
    plt.title("Grafo com cores e labels", size=15)
    plt.axis('off')
    plt.show()

# Exemplo de uso
n = int(input("Digite o número de vértices: "))
grafo = criar_grafo_cubico_aleatorio(n)

# Salvar grafo inicial
salvar_grafo_em_arquivo_json(grafo, 'grafo_cubico.json')
plotar_grafo(grafo, 10)

# Carregar e transformar o grafo
grafo_json = carregar_grafo_de_json('grafo_cubico.json')
grafo_transformado = transformar_grafo_cubico(grafo_json)
plotar_grafo(grafo_transformado, 10)
salvar_grafo_em_arquivo_json(grafo_transformado, 'grafo_transformado.json')

# Gerar sequência e visualizar
output_file = 'sequencia_grafo.txt'
gerar_grafo_com_json_e_salvar_sequencia('grafo_transformado.json', output_file)
