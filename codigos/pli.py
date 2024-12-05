from pulp import *
import json
from itertools import combinations

def sai(variaveis, adjacencia, u):
    ''' Retorna lista com as arestas (variaveis) que saem de u '''
    return [variaveis[u][v] for v in adjacencia[u]]

def entra(variaveis, adjacencia, u):
    ''' Retorna lista com as arestas (variaveis) que entram em u '''
    arestas_saem = []
    for u in adjacencia:
        if u in adjacencia[u]:
            arestas_saem.append(variaveis[u][u])
    return arestas_saem

def ham_path(vertices, S, T, adjacencia):
    ''' Resolve o problema do caminho hamiltoniano '''
    # matriz de variaveis p/ cada par de vertices
    variaveis = []
    for u in vertices:
        variaveis.append([LpVariable(f"x_{u}{v}", lowBound=0, upBound=1, cat="Integer") for v in vertices])

    # lista com as variaveis referentes as arestas
    arestas = []
    for u in adjacencia:
        for v in adjacencia[u]:
            arestas.append(variaveis[u][v])

    problema = LpProblem("HamPath", LpMaximize)

    problema += lpSum(arestas), 'objetivo'

    # apenas um sai de S, apenas um sai de T
    problema += lpSum(sai(variaveis, adjacencia, S)) == 1, "sai_de_s"
    problema += lpSum(entra(variaveis, adjacencia, T)) == 1, "entra_em_t"

    # condicoes com S e T ja foram satisfeitas, podem ser removidos
    vertices.remove(S)
    vertices.remove(T)

    # garante que apenas uma aresta entra e uma sai de cada vertice
    for v in vertices:
        problema += lpSum(entra(variaveis, adjacencia, v)) == 1, f"entra_em_{v}"
        problema += lpSum(sai(variaveis, adjacencia, v)) == 1, f"sai_de_{v}"

    # gera todos os subconjuntos de V com tamanho >= 2
    combinacoes = []
    for i in range(2, len(vertices)):
        combinacoes.extend(list(combinations(vertices, i)))

    # garante aciclidade
    for conj in combinacoes:
        arestas = []
        for i in range(len(conj)):
            u = conj[i]
            for j in range(i, len(conj)):
                v = conj[j]
                if v in adjacencia[u]:
                    arestas.append(variaveis[u][v])
                    arestas.append(variaveis[v][u])
        if arestas:
            # num. de arestas selecionadas devem ser no maximo o tamanho do subconjunto menos um
            problema += lpSum(arestas) <= len(conj) - 1, f"subconjunto_{'_'.join([str(i) for i in conj])}"

    print(problema)

    problema.solve(GUROBI(msg=0))
    print('Valor otimo:', value(problema.objective))
    print('Solucao otima:')
    for variavel in problema.variables():
        # printar apenas arestas selecionadas
        if (variavel.varValue > 0):
            print(f'  {variavel.name} = {variavel.varValue}')

def main():
    # leitura do grafo
    with open("grafo_cubico.json", "r") as file:
        grafo = json.load(file)
    n_vertices = grafo["n_vertices"]
    n_arestas = grafo["n_arestas"]
    adjacencia = {int(key): value for key, value in grafo["adjacencia"].items()}

    # criacao dos vertices S e T
    S = len(adjacencia)
    T = len(adjacencia) + 1

    # S incide em todos os vertices originais, e todos incidem em T
    for key in adjacencia.keys():
        adjacencia[key].append(T)
    adjacencia[S] = [i for i in range(n_vertices)]

    # chamada do PL
    vertices = list(range(n_vertices + 2))
    ham_path(vertices, S, T, adjacencia)

if __name__ == '__main__':
    main()  