import networkx as nx

from .lista_adjacente import lista_adjacente

# Obtem a lista de adjacencia para formar o grafo
def montar_grafo():
    # Grafo nao direcionado
    G = nx.Graph()
    
    # Obtendo lista de adjacencia
    adj = lista_adjacente()
    
    # Para cada vertice dentro das chaves da lista_adjacente
    for vertice in adj.keys():
        # Conecte as arestas de acordo com a quantidade de vertices conectadas vincalados a um vertice
        for aresta in range(len(adj[vertice])):
            G.add_edge(vertice, adj[vertice][aresta])

    return G
