import networkx as nx
from pyvis.network import Network
from tarjan import encontrar_bridges


def build_graph(nodes):
    G = nx.Graph()

    for node in nodes:
        G.add_node(node['ip'], label=node['ip'], title=node['hostname'])

    # Conecta todos ao gateway (primeiro da lista)
    if len(nodes) > 1:
        gateway = nodes[0]['ip']
        for node in nodes[1:]:
            G.add_edge(gateway, node['ip'])

    # Converter para dict para rodar o Tarjan
    grafo_dict = {n: list(G.neighbors(n)) for n in G.nodes}
    bridges = encontrar_bridges(grafo_dict)

    return G, bridges


def gerar_visual(G, bridges):
    net = Network(height='600px', width='100%',
                  bgcolor='#0d1117', font_color='white')

    # Adiciona nós
    for node in G.nodes:
        net.add_node(node, label=node, color='#4a9eff')

    # Adiciona arestas — bridges em vermelho, normais em branco
    bridges_set = set(map(tuple, [sorted(b) for b in bridges]))
    for u, v in G.edges:
        aresta = tuple(sorted([u, v]))
        if aresta in bridges_set:
            net.add_edge(u, v, color='red', width=3, title='⚠️ Ponto crítico!')
        else:
            net.add_edge(u, v, color='white')

    caminho = 'ui/grafo.html'
    net.save_graph(caminho)
    return caminho
