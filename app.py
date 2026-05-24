import os

from flask import Flask, jsonify, render_template, request, send_file
from flask_cors import CORS

from src.algorithms.centralidade import centralidade
from src.algorithms.tarjan import control_tarjan
from src.core.grafo import build_graph, gerar_visual
from src.core.lista_adjacente import lista_adjacente
from src.core.nx_grafo import montar_grafo
from src.io.scanner import descobrir_ip, mapear_rede

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__, static_folder=os.path.join(BASE_DIR, "src", "ui"), static_url_path=""
)
CORS(app, origins="*")

grafo_cache = None
bridges_cache = None


ip_subnet = descobrir_ip()
dispositivos = mapear_rede(ip_subnet)


@app.route("/")
def index():
    return send_file(os.path.join(BASE_DIR, "src", "ui", "index.html"))


@app.route("/scan", methods=["POST"])
def scan():
    """
    O scan agora é feito internamente pelo lista_adjacente.py,
    que chama scanner.py e conexoes.py automaticamente.
    Retornamos apenas a confirmação para o front seguir para /build-graph.
    """
    try:
        nodes = []
        for ip, info in dispositivos.items():
            nodes.append(
                {
                    "id": ip,
                    "ip": ip,
                    "status": info.get("status", "up"),
                    "tipo": info.get("tipo", "host"),
                    "mac": info.get("MAC"),
                    "vendor": info.get("vendor"),
                }
            )
        return jsonify({"status": "ok", "nodes": nodes})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/build-graph", methods=["POST"])
def build():
    global grafo_cache, bridges_cache

    try:
        # build_graph já chama conexoes + tarjan internamente
        grafo_cache, bridges_cache = build_graph(dispositivos)
        gerar_visual(grafo_cache, dispositivos, bridges_cache)

        return jsonify(
            {
                "grafo_url": "/static/grafo.html",
                "bridges": bridges_cache,
                "total_nodes": grafo_cache.number_of_nodes(),
                "total_edges": grafo_cache.number_of_edges(),
            }
        )
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/network-details")
def details():
    adj = lista_adjacente(dispositivos)
    ponte, articulacao = control_tarjan(adj)
    nx_adj = montar_grafo(adj)
    central = centralidade(nx_adj)

    dados = {
        "ips": [ip for ip in dispositivos.keys()],
        "articulacoes": articulacao,
        "pontes": ponte,
        "central": list(central),
    }

    return jsonify(dados)


@app.route("/export", methods=["GET"])
def export():
    if grafo_cache is None:
        return jsonify({"erro": "Nenhum grafo gerado ainda"}), 400
    caminho = os.path.join(BASE_DIR, "src", "ui", "grafo.html")
    return send_file(caminho, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
