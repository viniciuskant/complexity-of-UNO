# Complexity of UNO

Projeto da disciplina `MC558` sobre a complexidade do problema **UNO-1** (UNO com um jogador), com base no artigo [the complexity of uno](https://www.cs.ubc.ca/~nickhar/papers/Uno/1003.2851v3.pdf).

A ideia central é modelar UNO-1 via grafos e conectar o problema a **Caminho Hamiltoniano**, mostrando a redução a partir de grafos cúbicos.

## Objetivo

O repositório reúne:

- fundamentação teórica da modelagem de UNO-1 como grafo;
- descrição da redução de **HP-C** (Hamiltonian Path em grafos cúbicos) para UNO-1;
- scripts em Python para gerar grafos, aplicar a transformação e testar/visualizar instâncias;
- formulação de PLI para buscar caminho hamiltoniano.

## Estrutura do repositório

- `the complexity of uno.pdf`: artigo de referência.
- `analise_uno.pdf` (link para `.latex_analise_uno/analise_uno.pdf`): relatório do projeto.
- `programas/`: scripts principais para geração, redução e PLI.
- `programas/HPC_examples/`: instâncias de exemplo (JSON) com grafo cúbico + caminho.
- `latex_pli/`: material em LaTeX da formulação de PLI.
- `codigos/`: versões auxiliares/experimentais usadas durante o desenvolvimento.

## Requisitos

- Python 3.10+ (recomendado).
- Dependências mínimas (em `programas/requirements.txt`):
  - `matplotlib`
  - `networkx`
  - `pulp`
  - `gurobi` (necessário para `programas/pli.py`, pois o script chama `GUROBI` no solver)

Instalação rápida:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r programas/requirements.txt
```

Se quiser reproduzir o ambiente completo usado no projeto, existe também `requirements.txt` na raiz.

## Como executar

Os scripts foram escritos para execução a partir da pasta `programas/` (por causa de caminhos relativos como `HPC_examples/*.json`).

```bash
cd programas
```

### 1) Gerar grafo cúbico aleatório

```bash
python grafos_cubicos.py
```

Entrada:
- número par de vértices.

Saídas:
- `grafo_cubico.json`
- visualização do grafo (`matplotlib`) e arquivo `grafo_cubico.png`.

### 2) Rodar redução HP-C -> UNO-1 em instância de exemplo

```bash
python reducao.py
```

Entrada:
- número do teste (`1` ou `2`, por padrão nos arquivos de `HPC_examples/`).

Comportamento:
- lê o grafo cúbico e caminho hamiltoniano;
- verifica a validade do caminho;
- constrói o grafo transformado (instância UNO-1);
- constrói e imprime um caminho correspondente no grafo transformado.

### 3) Pipeline completo (geração + transformação + sequência de cartas)

```bash
python reducao_completa.py
```

Entrada:
- número par de vértices.

Saídas:
- `grafo_cubico.json`
- `grafo_transformado.json`
- `sequencia_grafo.txt` (sequência de cartas codificada como `cor+número`)
- plots dos grafos original e transformado.

### 4) Resolver por PLI

```bash
python pli.py
```

Pré-requisito:
- Gurobi instalado e licenciado no ambiente.

Comportamento:
- lê `grafo_cubico.json`;
- monta e resolve o modelo de caminho hamiltoniano;
- imprime variáveis ativas da solução;
- gera visualização com arestas destacadas em `grafo_cubico_com_destaques.png`.

## Formato das instâncias de exemplo (HPC)

Arquivos em `programas/HPC_examples/*.json` seguem, em geral, este formato:

```json
{
  "vertices": 10,
  "caminho": [1, 4, 3, 2, 5, 8, 9, 10, 6, 7],
  "adj": {
    "1": [4, 5, 6]
  }
}
```

- `vertices`: número de vértices.
- `adj`: lista de adjacência.
- `caminho`: caminho hamiltoniano conhecido para validação.

## Referências

- Demaine, E. D., Demaine, M. L., Harvey, N. J., Uehara, R., Uno, T., & Uno, Y. (2010). **The complexity of UNO**. arXiv preprint arXiv:1003.2851.
- Dataset de grafos hamiltonianos citado no projeto: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/hcp/

## Como citar

```bibtex
@software{Souza2024-hy,
  title    = "{complexity-of-UNO}",
  author   = "Souza, Henrique Parede de and Barroso, Pedro Brasil and
              Vasconcellos, Pedro Damasceno and Miguel, Vinicius Patriarca Miranda",
  month    =  dec,
  year     =  2024,
  language = "pt"
}
```