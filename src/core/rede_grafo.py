import networkx as nx

# Obtem a lista de adjacencia para formar o grafo
def montar_grafo(adj):
    # Grafo nao direcionado
    G = nx.Graph()
    
    # Para cada vertice dentro das chaves da lista_adjacente
    for vertice in adj.keys():
        # Conecte as arestas de acordo com a quantidade de vertices conectadas vincalados a um vertice
        for aresta in range(len(adj[vertice])):
            G.add_edge(vertice, adj[vertice][aresta])

    return G
