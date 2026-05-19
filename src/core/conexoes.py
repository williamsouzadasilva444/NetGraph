from scapy.all import conf


# Funcao para encontrar gateway do sistema, que normalmente sao
# Roteadores ou tambem Switchs
def encontrar_gateway():
    gateway = conf.route.route("0.0.0.0")[2]

    return gateway


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
