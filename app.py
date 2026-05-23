from flask import Flask, jsonify, request, send_file, render_template

from flask_cors import CORS

from src.core.grafo import build_graph, gerar_visual

from src.io.scanner import descobrir_ip, mapear_rede, encontrar_gateway
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=os.path.join(
    BASE_DIR, 'src', 'ui'), static_url_path='')
CORS(app, origins="*")

grafo_cache = None
bridges_cache = None


@app.route('/')
def index():
    return send_file(os.path.join(BASE_DIR, 'src', 'ui', 'index.html'))


@app.route('/scan', methods=['POST'])
def scan():
    """
    O scan agora é feito internamente pelo lista_adjacente.py,
    que chama scanner.py e conexoes.py automaticamente.
    Retornamos apenas a confirmação para o front seguir para /build-graph.
    """
    try:
        ip_subnet = descobrir_ip()
        dispositivos = mapear_rede(ip_subnet)

        nodes = []
        for ip, info in dispositivos.items():
            nodes.append({
                'id': ip,
                'ip': ip,
                'status': info.get('status', 'up'),
                'tipo': info.get('tipo', 'host'),
                'mac': info.get('MAC'),
                'vendor': info.get('vendor')
            })
        return jsonify({'status': 'ok', 'nodes': nodes})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    

@app.route('/build-graph', methods=['POST'])
def build():
    global grafo_cache, bridges_cache

    try:
        # build_graph já chama scanner + conexoes + tarjan internamente

        grafo_cache, bridges_cache = build_graph()
        gerar_visual(grafo_cache, bridges_cache)

        return jsonify({
            'grafo_url': '/static/grafo.html',
            'bridges': bridges_cache,
            'total_nodes': grafo_cache.number_of_nodes(),
            'total_edges': grafo_cache.number_of_edges()
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/export', methods=['GET'])
def export():
    if grafo_cache is None:
        return jsonify({'erro': 'Nenhum grafo gerado ainda'}), 400
    caminho = os.path.join(BASE_DIR, 'src', 'ui', 'grafo.html')
    return send_file(caminho, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
