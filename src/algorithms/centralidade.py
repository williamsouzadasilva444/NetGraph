import networkx as nx


# Funcao para calcular centralidade utilizando networkx
def centralidade(G):
    # Centralidade de Grau
    grau_centro = nx.degree_centrality(G)

    # Centralidade de Intermediacao
    entre_centro = nx.betweenness_centrality(G)

    vertice_central = set()

    # Adicionando o vertice mais central de ambas as metricas
    # Caso seja a mesma, por ser um set nao havera valores repetidos
    vertice_central.add(max(grau_centro, key=grau_centro.get))
    vertice_central.add(max(entre_centro, key=entre_centro.get))

    return vertice_central
