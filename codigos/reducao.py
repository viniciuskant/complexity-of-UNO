import networkx as nx
import matplotlib.pyplot as plt

def parse_cards(cards):
    """
    Recebe uma lista de cartas no formato cn (c é a cor, n é o número) e
    retorna uma lista de tuplas (cor, número).
    """
    return [(card[0], int(card[1:])) for card in cards]

def create_bipartite_graph(cards):
    """
    Cria o grafo bipartido a partir das cartas fornecidas.
    """
    B = nx.Graph()
    colors = set(card[0] for card in cards)
    numbers = set(card[1] for card in cards)

    # Adiciona vértices das duas partições
    B.add_nodes_from(colors, bipartite=0)  # Partição de cores
    B.add_nodes_from(numbers, bipartite=1)  # Partição de números

    # Adiciona arestas entre cores e números baseadas nas cartas
    for color, number in cards:
        B.add_edge(color, number)

    return B

def create_line_graph(bipartite_graph):
    """
    Cria o grafo linha do grafo bipartido fornecido.
    """
    return nx.line_graph(bipartite_graph)

def plot_graphs_side_by_side(bipartite_graph, line_graph, bipartite_colors, line_colors, bipartite_labels, line_labels):
    """
    Plota o grafo bipartido e o grafo linha lado a lado em subplots.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot do grafo bipartido
    ax = axes[0]
    pos_bipartite = nx.spring_layout(bipartite_graph)
    nx.draw(
        bipartite_graph, pos_bipartite, ax=ax, with_labels=True, labels=bipartite_labels,
        node_color=bipartite_colors, node_size=800, font_color='black'
    )
    ax.set_title("Grafo Bipartido (Cores e Números)")

    # Plot do grafo linha
    ax = axes[1]
    pos_line = nx.spring_layout(line_graph)
    nx.draw(
        line_graph, pos_line, ax=ax, with_labels=True, labels=line_labels,
        node_color=line_colors, node_size=800, font_color='black'
    )
    ax.set_title("Grafo Linha das Cartas")

    plt.tight_layout()
    plt.show()

# Input de cartas
cards_input = input("Digite a sequência de cartas: ").replace(" ", "").split(",")
cards = parse_cards(cards_input)

# Criação do grafo bipartido
bipartite_graph = create_bipartite_graph(cards)

# Criação do grafo linha
line_graph = create_line_graph(bipartite_graph)

# Cores e labels para o grafo bipartido
bipartite_colors = []
bipartite_labels = {}
for node in bipartite_graph.nodes:
    if isinstance(node, int):  # Números
        bipartite_colors.append('gray')
        bipartite_labels[node] = str(node)
    else:  # Cores
        # color_map = {'r': 'black', 'g': 'black', 'b': 'black', 'y': 'black'}
        # bipartite_colors.append(color_map.get(node, 'black'))
        color_map = {'r': 'red', 'g': 'green', 'b': 'blue', 'y': 'yellow'}
        bipartite_colors.append(color_map.get(node, 'black'))
        bipartite_labels[node] = node.upper()

# Cores e labels para o grafo linha
line_colors = []
line_labels = {}
for node in line_graph.nodes:
    color, number = node  # O nó do grafo linha é uma aresta do bipartido
    color_map = {'r': 'red', 'g': 'green', 'b': 'blue', 'y': 'yellow'}
    line_labels[node] = str(number)  # Apenas o número como label
    line_colors.append(color_map.get(color, 'black'))

# Plots lado a lado
plot_graphs_side_by_side(
    bipartite_graph, line_graph, bipartite_colors, line_colors,
    bipartite_labels, line_labels
)
