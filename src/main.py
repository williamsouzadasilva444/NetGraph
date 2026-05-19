import networkx as nx
import matplotlib.pyplot as plt

from .core.lista_adjacente import lista_adjacente
from .core.rede_grafo import montar_grafo
from .algorithms.tarjan import control_tarjan

if __name__ == "__main__":
    print("Bem vindo ao NetGraph CLI:")

    lista_adj = lista_adjacente()

    grafo = montar_grafo(lista_adj)

    print("Rede scaneada! Vamos encontrar dispositivos e conexoes criticas")

    pontes, articulacao = control_tarjan(lista_adj)

    print(
        "Caso essas conexoes sejam cortadas, irao desconectar certos dispositivos da rede"
    )
    for ponte in pontes:
        print(f"Conexao Critica: {ponte}")

    print("Caso esse dispositivo seja desconectado, toda rede cai")
    for corte in articulacao:
        print(f"Dispositivo Critico: {corte}")

    print("Exibindo sua rede local...")
    print("Feche a janela para sair do programa")
    nx.draw_spring(grafo, with_labels=True)
    plt.show()

    print("Saindo... Obrigado por testar o NetGraph...")
