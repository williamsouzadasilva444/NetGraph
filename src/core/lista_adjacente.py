import json

from ..io import scanner
from ..core import conexoes


def definir_dispositivos():
    ip = scanner.descobrir_ip()
    return scanner.mapear_rede(ip)


def lista_adjacente():
    vertices = definir_dispositivos()
    arestas = conexoes.definir_conexoes(vertices)

    adj = {}

    for vert in vertices.keys():
        adj[vert] = []

    # Garante que o gateway existe no dicionário mesmo se não foi escaneado
    for origem, destino in arestas:
        if origem not in adj:
            adj[origem] = []
        if destino not in adj:
            adj[destino] = []
        adj[origem].append(destino)
        adj[destino].append(origem)

    with open("lista_adj.json", "w") as lista:
        json.dump(adj, lista, indent=4)

    return adj
