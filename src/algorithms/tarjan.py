# Algoritmo principal Tarjan
def dfs_tarjan(
    vertice_in, grafo, visitado, desc_temp, low, pais, pontes, articulacao, tempo
):
    # Adicionando o Vertice atual (u) na lista de visitados
    visitado.append(vertice_in)

    # Definindo tempo de descobrimento do vertice(u) na arvore DFS
    desc_temp[vertice_in] = tempo[0]

    # Definindo low-link do vertice(u)
    low[vertice_in] = tempo[0]

    # Incrementando tempo de descobrimento para o proximo vertice
    tempo[0] += 1

    # Inicializando filhos
    filhos = 0

    # Para cada vertice(v) ligado ao vertice(u)
    for vertice in grafo[vertice_in]:
        # Caso vertice (v) nao esteja em visitado
        if vertice not in visitado:
            # Adicione vertice atual(u) aos pais do vertice(v)
            pais[vertice] = vertice_in

            # Incremente o numero de filhos do vertice(u)
            filhos += 1

            # Chame recusivamente o DFS para o vertice vizinho(v)
            dfs_tarjan(
                vertice,
                grafo,
                visitado,
                desc_temp,
                low,
                pais,
                pontes,
                articulacao,
                tempo,
            )

            # Ache o valor minimo de Low-Link entre os vertices (u, v), e atualize o Low-Link do vertice(u)
            # Caso dois vertices possuem o mesmo Low-Link, logo possui caminho alternativo entre eles
            low[vertice_in] = min(low[vertice_in], low[vertice])

            # Se o tempo de descobrimento do vertice(u) for menor que o Low-Link do vertice(v)
            # Logo e uma ponte, nao existe caminhos alternativos entre os dois vertices
            if desc_temp[vertice_in] < low[vertice]:
                pontes.append((vertice_in, vertice))

            # Caso vertice(u) nao seja a raiz da arvore DFS
            # E o tempo de descobrimento do vertice(u) for menor que Low-Link do vertice(v)
            # Logo vertice(u) e um ponto de articulacao, vertice(v) depende de vertice(u)
            if pais[vertice_in] is not None and desc_temp[vertice_in] <= low[vertice]:
                articulacao.append(vertice_in)

        # Caso o vertice(v) ja esteja visitado, e nao ser pai de vertice(u)
        elif vertice != pais[vertice_in]:
            # Atualize Low-Link de vertice(u), logo possui caminhos alternativos
            low[vertice_in] = min(low[vertice_in], desc_temp[vertice])

    # Caso o vertice(u) seja a raiz da arvore DFS
    # E tenha mais que dois filhos
    if pais[vertice_in] is None and filhos > 2:
        # Automaticamente sera um ponto de articulacao
        articulacao.append(vertice_in)

    return


# Controlador do do algoritmo de Tarjan, ira inicializar todas as estruturas necessarias para realizar o algoritmo
def control_tarjan(grafo):
    if not grafo:
        raise Exception("ERRO: O grafo esta vazio...")

    # Capturando a primeira chave/vertice do grafo, para ser o vertice inicial
    vertice_in = next(iter(grafo))

    # Lista para manter os vertices visitados
    visitado = []

    # Contador global e mutavel para manter tempo de descobrimento
    tempo = [0]

    # Dicionario de Tempo de descobrimento do DFS em cada vertice
    desc_temp = {}

    # Dicionario de Low-Link de cada vertice, mantendo o ancestral mais antigo que conseguem voltar, contando com ele mesmo
    low = {}

    # Inicilizando dicionario de Pais, iniciando cada pai de vertice como None
    pais = {vertice: None for vertice in grafo.keys()}

    # Lista de pontes/arestas de corte detectadas
    # Ira conter tuplas com vertices que formam a pontes -> (u, v)
    pontes = []

    # Lista de vertices que sao pontos de articulacao/vertices de corte
    articulacao = []

    # Chamando o processo de DFS do Tarjan
    dfs_tarjan(
        vertice_in, grafo, visitado, desc_temp, low, pais, pontes, articulacao, tempo
    )

    return pontes, articulacao
