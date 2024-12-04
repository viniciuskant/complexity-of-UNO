import networkx as nx
import json
import matplotlib.pyplot as plt

def gerar_grafo_com_json_e_salvar_sequencia(json_file, output_file):
    with open(json_file, 'r') as f:
        grafo_json = json.load(f)
    
    G = nx.Graph()
    
    n_vertices = grafo_json["n_vertices"]
    adjacencia = grafo_json["adjacencia"]
    
    cor_dict = {0: 'r', 1: 'g', 2: 'b', 3: 'y'}
    
    sequencia = []
    
    for vertice, vizinhos in adjacencia.items():
        vertice_key = eval(vertice)
        cor_idx = vertice_key[0] % 4
        cor = cor_dict[cor_idx]
        label = (vertice_key[1][0] + vertice_key[1][1]) % 9
        
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

json_file = 'grafo_transformado.json'
output_file = 'sequencia_grafo.txt'
gerar_grafo_com_json_e_salvar_sequencia(json_file, output_file)
