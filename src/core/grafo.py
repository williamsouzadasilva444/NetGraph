import os
from pyvis.network import Network

from src.algorithms.tarjan import control_tarjan

from src.core.lista_adjacente import lista_adjacente

from src.io.scanner import encontrar_gateway

OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "ui", "static", "grafo.html"
)


def build_graph(nodes: list = None):
    adj = lista_adjacente()
    if not adj:
        raise Exception("Nenhum dispositivo encontrado na rede.")
    pontes, articulacao = control_tarjan(adj)
    gateway = encontrar_gateway()
    bridges = [{"from": u, "to": v} for u, v in pontes]
    all_ips = set(adj.keys())
    nodes_list = [{"id": ip, "label": ip} for ip in all_ips]
    grafo_obj = _GraphObj(adj, nodes_list, gateway, pontes, articulacao)
    return grafo_obj, bridges


def gerar_visual(grafo_obj, bridges: list) -> str:
    output = os.path.abspath(OUTPUT_PATH)
    os.makedirs(os.path.dirname(output), exist_ok=True)

    net = Network(
        height="100%",
        width="100%",
        bgcolor="transparent",
        font_color="#f3f4f6",
        directed=False,
    )

    bridge_set = {frozenset([b["from"], b["to"]]) for b in bridges}

    for node in grafo_obj.nodes:
        is_gateway = node["id"] == grafo_obj.gateway
        net.add_node(
            node["id"],
            label=node.get("label", node["id"]),
            title=(
                f"<b style='color:{'#818cf8' if is_gateway else '#67e8f9'}'>{node['id']}</b><br>"
                f"<span style='color:#9ca3af'>MAC:</span> {node.get('mac', 'N/A')}<br>"
                f"<span style='color:#9ca3af'>Vendor:</span> {node.get('vendor', '?')}<br>"
                f"<span style='color:#9ca3af'>Status:</span> <span style='color:#22d3ee'>● UP</span>"
            ),
            color={
                "background": "#6366F1" if is_gateway else "#22d3ee",
                "border": "#818cf8" if is_gateway else "#67e8f9",
                "highlight": {
                    "background": "#4f46e5" if is_gateway else "#0891b2",
                    "border": "#a5b4fc" if is_gateway else "#a5f3fc",
                },
            },
            size=30 if is_gateway else 16,
            shape="dot",
            font={"size": 11, "color": "#9ca3af", "face": "Inter, sans-serif"},
            borderWidth=2,
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
                u,
                v,
                color={
                    "color": "#ef4444" if is_bridge else "rgba(255,255,255,0.15)",
                    "highlight": "#ef4444" if is_bridge else "rgba(255,255,255,0.4)",
                },
                width=2.5 if is_bridge else 1.5,
                dashes=[6, 4] if is_bridge else False,
                title=(
                    "<span style='color:#ef4444'>⚠️ Bridge crítica</span><br>"
                    "<span style='color:#9ca3af;font-size:11px'>Remoção isola segmento da rede</span>"
                )
                if is_bridge
                else "",
            )

    net.set_options("""
    {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -9000,
          "centralGravity": 0.25,
          "springLength": 140,
          "springConstant": 0.04,
          "damping": 0.09
        },
        "stabilization": { "iterations": 250 }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 60,
        "navigationButtons": false,
        "keyboard": false
      }
    }
    """)

    net.save_graph(output)

    # ── Injeta CSS para corrigir fundo, altura e estilo ──────────────────────
    with open(output, "r", encoding="utf-8") as f:
        html = f.read()

    css = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  html, body {
    width: 100%;
    height: 100%;
    background: transparent !important;
    overflow: hidden;
  }

  /* Remove card branco do Bootstrap */
  .card {
    width: 100% !important;
    height: 100% !important;
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }

  /* Grafo ocupa 100% do espaço */
  #mynetwork {
    width: 100% !important;
    height: 100vh !important;
    background: transparent !important;
    border: none !important;
    position: absolute !important;
    top: 0; left: 0;
  }

  /* Tooltip estilizado */
  .vis-tooltip {
    background: rgba(10, 13, 25, 0.95) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f3f4f6 !important;
    font-family: Inter, sans-serif !important;
    font-size: 12px !important;
    padding: 10px 14px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
    line-height: 1.6 !important;
  }

  /* Remove títulos vazios gerados pelo PyVis */
  center, h1 { display: none !important; }
</style>
"""

    html = html.replace("</head>", css + "</head>")

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    return output


class _GraphObj:
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
