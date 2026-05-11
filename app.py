from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
from scanner import scan_network
from graph import build_graph, gerar_visual
import json

app = Flask(__name__, static_folder='ui', static_url_path='')
# Permite CORS para todas as origens, necessário para o frontend acessar a API sem bloqueios de CORS
CORS(app, origins="*")

grafo_cache = None
bridges_cache = None

# adicioniando rota para servir o index.html (20:44)


@app.route('/')
def index():
    return send_file('ui/index.html')


@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    alvo = data.get('target', '192.168.1.0/24')
    resultado = scan_network(alvo)
    return jsonify(resultado)


@app.route('/build-graph', methods=['POST'])
def build():
    global grafo_cache, bridges_cache
    data = request.json
    grafo_cache, bridges_cache = build_graph(data['nodes'])
    caminho = gerar_visual(grafo_cache, bridges_cache)

    return jsonify({
        'grafo_url': '/static/grafo.html',
        'bridges': bridges_cache,
        'total_nodes': grafo_cache.number_of_nodes(),
        'total_edges': grafo_cache.number_of_edges()
    })


@app.route('/export', methods=['GET'])
def export():
    if grafo_cache is None:
        return jsonify({'erro': 'Nenhum grafo gerado ainda'}), 400
    return send_file('ui/grafo.html', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
