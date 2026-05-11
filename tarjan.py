def encontrar_bridges(grafo):
    """
    Algoritmo de Tarjan para encontrar bridges.
    Bridge = conexão cuja remoção desconecta a rede.
    """
    visitado = set()
    discovery = {}
    low = {}
    pai = {}
    bridges = []
    timer = [0]

    def dfs(u):
        visitado.add(u)
        discovery[u] = low[u] = timer[0]
        timer[0] += 1

        for v in grafo.get(u, []):
            if v not in visitado:
                pai[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])

                # Se low[v] > discovery[u], a aresta u-v é uma bridge
                if low[v] > discovery[u]:
                    bridges.append((u, v))

            elif v != pai.get(u):
                low[u] = min(low[u], discovery[v])

    for node in grafo:
        if node not in visitado:
            dfs(node)

    return bridges 