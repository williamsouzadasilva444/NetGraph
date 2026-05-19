import os
from pyvis.network import Network
from src.algorithms.tarjan import control_tarjan
from src.core.lista_adjacente import lista_adjacente
from src.core.conexoes import encontrar_gateway

# Caminho relativo à raiz do projeto
OUTPUT_PATH = os.path.join(os.path.dirname(
    __file__), '..', '..', 'ui', 'static', 'grafo.html')


def build_graph(nodes: list = None):
    """
    Constrói o grafo usando os módulos existentes do projeto.
    - conexoes.py  → detecta o gateway real via scapy
    - lista_adjacente.py → monta o dicionário de adjacência
    - tarjan.py    → encontra pontes e pontos de articulação

    O parâmetro `nodes` é aceito por compatibilidade com o app.py,
    mas a lista de adjacência é montada internamente pelos módulos.
    """
    adj = lista_adjacente()

    if not adj:
        raise Exception("Nenhum dispositivo encontrado na rede.")

    pontes, articulacao = control_tarjan(adj)

    gateway = encontrar_gateway()
    bridges = [{'from': u, 'to': v} for u, v in pontes]

    # Reconstrói lista de nós a partir do dicionário de adjacência
    all_ips = set(adj.keys())
    nodes_list = [{'id': ip, 'label': ip} for ip in all_ips]

    grafo_obj = _GraphObj(adj, nodes_list, gateway, pontes, articulacao)

    return grafo_obj, bridges


def gerar_visual(grafo_obj, bridges: list) -> str:
    """
    Gera o HTML interativo com PyVis em ui/static/grafo.html.
    - Gateway: índigo (#6366F1), tamanho maior
    - Hosts:   ciano (#22d3ee)
    - Bridges: arestas em vermelho (#ef4444)
    """
    output = os.path.abspath(OUTPUT_PATH)
    os.makedirs(os.path.dirname(output), exist_ok=True)

    net = Network(
        height='100%',
        width='100%',
        bgcolor='transparent',
        font_color='#f3f4f6',
        directed=False
    )

    bridge_set = {frozenset([b['from'], b['to']]) for b in bridges}

    for node in grafo_obj.nodes:
        is_gateway = (node['id'] == grafo_obj.gateway)
        net.add_node(
            node['id'],
            label=node.get('label', node['id']),
            title=(
                f"<b>{node.get('label', node['id'])}</b><br>"
                f"IP: {node['id']}<br>"
                f"MAC: {node.get('mac', 'N/A')}<br>"
                f"Vendor: {node.get('vendor', '?')}"
            ),
            color='#6366F1' if is_gateway else '#22d3ee',
            size=30 if is_gateway else 18,
            font={'size': 12, 'color': '#f3f4f6'}
        )

    adicionadas = set()
    for u, vizinhos in grafo_obj.adjacencia.items():
        for v in vizinhos:
            aresta = frozenset([u, v])
            if aresta in adicionadas:
                continue
            adicionadas.add(aresta)
            is_bridge = aresta in bridge_set
            net.add_edge(
                u, v,
                color='#ef4444' if is_bridge else 'rgba(255,255,255,0.18)',
                width=3 if is_bridge else 1.5,
                title='⚠️ Bridge — ponto crítico' if is_bridge else ''
            )

    net.set_options("""
    {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -8000,
          "centralGravity": 0.3,
          "springLength": 130
        },
        "stabilization": { "iterations": 200 }
      },
      "interaction": { "hover": true, "tooltipDelay": 80 }
    }
    """)

    net.save_graph(output)
    return output


class _GraphObj:
    """Objeto que expõe a interface esperada pelo app.py."""

    def __init__(self, adjacencia, nodes, gateway, pontes, articulacao):
        self.adjacencia = adjacencia
        self.nodes = nodes
        self.gateway = gateway
        self.pontes = pontes
        self.articulacao = articulacao

    def number_of_nodes(self):
        return len(self.adjacencia)

    def number_of_edges(self):
        total = sum(len(v) for v in self.adjacencia.values())
        return total // 2
