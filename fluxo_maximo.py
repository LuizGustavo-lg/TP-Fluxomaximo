import sys
from ortools.graph.python.max_flow import SimpleMaxFlow
import networkx as nx
import matplotlib.pyplot as plt

#  PARSER DA INSTÂNCIA
def parse_instance(path='./fluxo_maximo.txt'):
    """
    Lê uma instância de fluxo máximo a partir de um arquivo de texto.

    O arquivo pode conter linhas vazias ou iniciadas com '#', que serão ignoradas.
    A função espera um cabeçalho contendo quatro inteiros (n, m, s, t) e,
    em seguida, exatamente m linhas descrevendo as arestas no formato: u v cap.

    Args:
        path (str): Caminho do arquivo contendo a instância do problema.

    Returns:
        tuple: Uma tupla contendo:
            - n (int): Número de vértices.
            - m (int): Número de arestas.
            - s (int): Nó origem.
            - t (int): Nó destino.
            - edge_list (list): Lista de tuplas (u, v, cap) representando as arestas.

    Raises:
        ValueError: Se o arquivo estiver vazio, o cabeçalho for inválido,
            ou o número de arestas não corresponder ao valor informado.
    """
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            lines.append(parts)

    if len(lines) == 0:
        raise ValueError("Arquivo sem dados úteis.")

    # Primeira linha: n m s t
    header = lines[0]
    if len(header) != 4:
        raise ValueError("Cabeçalho inválido — esperado: n m s t")
    n = int(header[0])
    m = int(header[1])
    s = int(header[2])
    t = int(header[3])

    # Validar número de arestas
    if len(lines) - 1 != m:
        raise ValueError(
            f"Esperado m = {m} arestas, mas apenas {len(lines)-1} foram encontradas."
        )

    # Ler arestas
    edge_list = []
    for parts in lines[1:]:
        if len(parts) != 3:
            raise ValueError("Linha de aresta inválida. Esperado: u v cap")
        u = int(parts[0])
        v = int(parts[1])
        cap = int(parts[2])
        edge_list.append((u, v, cap))

    return n, m, s, t, edge_list


#  FUNÇÃO DE FLUXO MÁXIMO
def solve_max_flow(n, s, t, edge_list):
    """
    Resolve um problema de fluxo máximo utilizando o SimpleMaxFlow.

    A função cria um solver, insere todas as arestas com suas capacidades
    e executa o cálculo do fluxo máximo entre os nós origem (s) e destino (t).

    Args:
        n (int): Número de vértices do grafo.
        s (int): Nó de origem.
        t (int): Nó de destino.
        edge_list (list): Lista de arestas no formato (u, v, cap).

    Returns:
        tuple: Uma tupla contendo:
            - maxflow (int): Valor total do fluxo máximo.
            - flows (list): Lista contendo, para cada arco do solver,
              uma tupla (tail, head, capacity, flow).

    Raises:
        RuntimeError: Se o solver não encontrar uma solução ótima.
    """
    solver = SimpleMaxFlow()

    # Inserir arestas
    for (u, v, cap) in edge_list:
        solver.add_arc_with_capacity(u, v, cap)

    status = solver.solve(s, t)
    if status != solver.OPTIMAL:
        raise RuntimeError("Falha no solver de fluxo máximo.")

    maxflow = solver.optimal_flow()
    flows = []
    for i in range(solver.num_arcs()):
        flows.append((
            solver.tail(i),
            solver.head(i),
            solver.capacity(i),
            solver.flow(i),
        ))

    return maxflow, flows


#  FORMATAÇÃO DA SAÍDA
def print_didactic_output(n, m, s, t, maxflow, flows):
    """
    Exibe na tela um resumo didático dos resultados do cálculo de fluxo máximo.

    A função imprime informações gerais sobre o grafo, o valor do fluxo máximo
    encontrado e uma lista formatada contendo apenas as arestas que receberam
    fluxo positivo. Também identifica quais arestas ficaram saturadas, além de
    apresentar observações interpretativas para auxiliar o entendimento.

    Args:
        n (int): Número de vértices do grafo.
        m (int): Número de arestas declaradas no cabeçalho.
        s (int): Índice do nó de origem.
        t (int): Índice do nó de destino.
        maxflow (int): Valor total do fluxo máximo obtido.
        flows (list): Lista de tuplas (u, v, capacidade, fluxo) para cada arco
            retornado pelo solver.

    Returns:
        None
    """

    print("\n===========================================")
    print("              RESULTADO DO TP              ")
    print("===========================================\n")

    print(f"⚙️   Número de vértices        : {n}")
    print(f"⚙️   Número de arestas         : {m}")
    print(f"🚩 Nó de origem (source)      : {s}")
    print(f"🏁 Nó de destino (target)     : {t}")

    print("\n===========================================")
    print("              FLUXO MÁXIMO                 ")
    print("===========================================\n")

    print(f"📦 Fluxo máximo encontrado: {maxflow}\n")

    print("===========================================")
    print("     ARESTAS QUE FIZERAM PARTE DO FLUXO    ")
    print("===========================================\n")

    active_edges = [(u, v, cap, f) for (u, v, cap, f) in flows if f > 0]

    if not active_edges:
        print("Nenhuma aresta recebeu fluxo > 0.\n")
    else:
        for (u, v, cap, f) in active_edges:
            status = " (⭐ saturada)" if f == cap else ""
            print(f"{u:2d} → {v:2d}  | cap = {cap:3d} | fluxo = {f:3d}{status}")

    print("\n\n===========================================")
    print("        OBSERVAÇÕES E INTERPRETAÇÃO         ")
    print("===========================================\n")

    print("• As arestas marcadas com '⭐ saturada' atingiram a capacidade máxima.")
    print("• Elas representam gargalos do sistema.")
    print("• O valor total do fluxo é a soma do fluxo que chega ao nó destino.\n")

    print("===========================================\n")


def plot_grafo(flows):
    """
    Desenha o grafo contendo apenas as arestas que possuem fluxo positivo.

    A função filtra as arestas para mostrar somente aquelas nas quais o
    solver atribuiu um fluxo maior que zero. Em seguida, constrói um
    grafo direcionado com NetworkX, posiciona os nós usando o layout
    spring e exibe o grafo com rótulos de vértices e capacidades.

    Args:
        flows (list): Lista de tuplas no formato (u, v, capacidade, fluxo)
            contendo a saída do solver de fluxo máximo.

    Returns:
        None
    """
    active_edges = [(u, v, cap, f) for (u, v, cap, f) in flows if f > 0]

    G = nx.DiGraph()
    for (u, v, cap, _) in active_edges:
        G.add_edge(u, v, capacity=cap)

    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(G, k=2.0, iterations=200)

    nx.draw(
        G,
        pos,
        with_labels=True,
        arrows=True,
        node_size=1200,
        font_size=12,
        width=2.5
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=nx.get_edge_attributes(G, 'capacity'),
        font_size=10
    )

    plt.show()


def args_option(args=list, option=str):
    """
    Retorna True se a opção fornecida estiver presente na lista de argumentos.

    Args:
        args (list): Lista de argumentos, como sys.argv.
        option (str): Opção que deve ser procurada na lista.

    Returns:
        bool: True se a opção estiver na lista de argumentos; caso contrário, False.
    """
    for i in args[1:]:
        if option == i:
            return True
    return False

#  MAIN
def main():
    if len(sys.argv) < 2 or args_option(sys.argv, '--help'):
        print("Uso: python3 fluxo_maximo.py [OPTIONS] [file]")
        print("    --help : mensagem de ajuda")
        print("    --plot : exibe uma imagem do grafo final")
        return
    
    path = sys.argv[-1]
    n, m, s, t, edges = parse_instance(path)

    print(f"📥 Lendo instância desde: {path}\n")

    maxflow, flows = solve_max_flow(n, s, t, edges)
    
    # flows.sort()

    print_didactic_output(n, m, s, t, maxflow, flows)

    if args_option(sys.argv, '--plot'):
        plot_grafo(flows)

if __name__ == "__main__":
    main()