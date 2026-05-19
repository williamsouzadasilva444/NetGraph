from ..io.scanner import encontrar_gateway


# Definindo as arestas do grafo
def definir_conexoes(host):
    gw = encontrar_gateway()

    conexoes = [()]

    # Caso Gateway esteja entre os IPs scaneados
    if gw in host.keys():
        # Adicione cada IP ao Gateway, a nao ser ele mesmo
        conexoes = [(gw, i) for i in host.keys() if gw != i]
    else:
        # Se nao, adicione cada IP ao Gateway
        conexoes = [(gw, i) for i in host.keys()]

    return conexoes
