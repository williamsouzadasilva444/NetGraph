import json

from ..io import scanner
from ..core import conexoes


# Por enquanto apenas retorna dispositivos como mapear_rede()
# Pretendemos verificar tipos de host nessa funcao futuramente
def definir_dispositivos():
    ip = scanner.descobrir_ip()

    return scanner.mapear_rede(ip)


# Ira montar uma lista de Adjacencia com os dados que capturamos
def lista_adjacente():
    # Dispositivos scaneados serao vertices
    vertices = definir_dispositivos()

    # Conexoes com o gateway serao arestas
    arestas = conexoes.definir_conexoes(vertices)

    adj = {}

    # Atribuindo chaves, onde cada chave sera um vertice
    for vert in vertices.keys():
        adj[vert] = []

    # Conectando as arestas ao vertices
    for origem, destino in arestas:
        # Deve adicionar um caminho de volta por ser um grafo nao direcionado
        adj[origem].append(destino)
        adj[destino].append(origem)

    # Salvando arquivo em JSON, para uso futuro
    with open("lista_adj.json", "w") as lista:
        json.dump(adj, lista, indent=4)

    return adj
