import json
from pathlib import Path

import pytest

from src.algorithms.tarjan import control_tarjan

raiz = Path(__file__).parent.parent


# Testando tarjan com um grafo predeterminado, deve ser 1 articulacao e 8 pontes
def test_base_tarjan():
    # Obtendo JSON com grafo de exemplo
    grafo_arquivo = raiz / "data" / "grafo_exemplo.json"

    # Carregando JSON na memoria
    with open(grafo_arquivo) as grafo:
        grafo_base = json.load(grafo)

    # Chamando JSON com grafo
    pontes, articulacao = control_tarjan(grafo_base)

    # Resultados esperados
    articulacao_esperado = ["192.168.0.1"]

    pontes_esperado = [
        ("192.168.0.1", "192.168.0.12"),
        ("192.168.0.1", "192.168.0.24"),
        ("192.168.0.1", "192.168.0.37"),
        ("192.168.0.1", "192.168.0.58"),
        ("192.168.0.1", "192.168.0.76"),
        ("192.168.0.1", "192.168.0.103"),
        ("192.168.0.1", "192.168.0.145"),
        ("192.168.0.1", "192.168.0.201"),
    ]

    # Testando resultados
    assert articulacao_esperado == articulacao
    assert pontes_esperado == pontes


# Testando caso o grafo esteja vazio, deve levantar erro/excecao
def test_grafo_nulo():
    grafo_nulo = {}

    # Verificando por excecoes, caso aconteca, o teste passa
    with pytest.raises(Exception, match="ERRO: O grafo esta vazio..."):
        control_tarjan(grafo_nulo)


# Testando caso o grafo for completo, nao deve ter pontes ou articulacao
def test_grafo_completo():
    grafo_completo_arquivo = raiz / "data" / "grafo_completo_exemplo.json"

    with open(grafo_completo_arquivo) as grafo:
        grafo_completo = json.load(grafo)

    print(grafo_completo)

    pontes, articulacao = control_tarjan(grafo_completo)

    articulacao_esperado = []

    pontes_esperado = []

    assert articulacao_esperado == articulacao
    assert pontes_esperado == pontes
