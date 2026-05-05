# E2 — Design Técnico, Arquitetura e Backlog

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 20 de abril de 2026  
> **Peso:** 20% da nota final  

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | NetGraph |
| Repositório GitHub | https://github.com/williamsouzadasilva444/NetGraph |
| Integrante 1 | William Souza — 41057619 |
| Integrante 2 | Matheus Akira Saito de Souza — 38746344 |
| Integrante 3 | José Gonçalves Braz Júnior — 40789659 |

---

## 1. Algoritmos Escolhidos

### 1.1 Algoritmo Principal

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | Tarjan |
| Categoria | Busca/Passagem |
| Complexidade de tempo | O(V + E) |
| Complexidade de espaço | O(V) |
| Problema que resolve | Encontrar Pontos de Articulação e Pontes |

**Por que este algoritmo foi escolhido?**

> Algoritmo de Tarjan é uma extensão de DFS, esse algoritmo foi escolhido por conta da sua simplicidade em encontrar Pontos de Articulação/Vértice de Corte e Pontes. Vértices de Corte são vértices que caso forem desconectados, transformam o grafo em dois componentes. Isso pode ser encarado dentro de uma estrutura de redes de computadores como Dispositivos Críticos, como switches que intermediam toda a rede, e se caso cair, toda a rede cai como em uma Topologia do tipo Estrela.
> Pontes são arestas que, assim como Vértices de Corte, caso forem desconectadas separa o grafo. Dentro no nosso projeto pode ser visto como um Ponto Crítico, como uma conexão que, caso falhe, desconecta parte da rede, como uma conexão entre um switch e um dispositivo, ou um roteador e dois switches.
> O algoritmo de Tarjan mesmo sendo aplicado normalmente para detectar Componentes Fortemente Conexos em grafos direcionados, esse algoritmo consegue em apenas uma varredura com tempo linear, descobrir esses pontos em grafos não direcionados com simples verificações com o tempo de descobrimento de um vértice (a primeira vez que um vértice é visitado no DFS) e Low Links (tempo de um descobrimento mínimo, verifica se existe algum caminho alternativo até seus descendentes).

**Alternativa descartada e motivo:**

| Algoritmo alternativo | Motivo da exclusão |
|----------------------|-------------------|
| Kosaraju | Além de precisar de duas varreduras DFS para concluir, Kosaraju é feito apenas para encontrar Componentes Fortemente Conexos em grafos direcionados, ou seja, não tem a versatilidade que Tarjan oferece. |

**Limitações no contexto do problema:**

- O Algoritmo de Tarjan vai apenas assumir uma rede estática, ou seja, uma rede Ethernet no máximo. O algoritmo não foi pensado em lidar com Grafos Dinâmicos, onde vértices podem desconectar e reconectar novamente como dispositivos móveis em uma rede Wifi, para perceber qualquer mudança realizada em uma rede, uma nova varredura feita com NMap deve ser feita.

- O algoritmo vai apenas medir a resiliência estrutural da rede de computadores, sua topologia, e ignora comportamentos como latência, gargalo e performance.

**Referência bibliográfica:**

> MEHLHORN, K; NÄHER, S.; SANDER, P. Engineering DFS-Based Graph Algorithms. Research Gate, 2007.
> TARJAN, R. DEPTH-FIRST SEARCH AND LINEAR GRAPH ALGORITHMS. Vol. 1. Nova Iorque: SIAM Journal on Computing, 1972.

---

### 1.2 Algoritmo Adicional *(se houver)*

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | BFS |
| Categoria | Busca/Passagem |
| Complexidade de tempo | O(V + E) |
| Complexidade de espaço | O(V) |

**Justificativa:**

> Iremos utilizar BFS para calcular a menor distância entre dois vértices, nesse caso, dois dispositivos onde a a distância será calculado por Hops. Escolhemos BFS porque ele permite calculo de menores caminhos em grafos não ponderados.

**Referência bibliográfica:**

> ARUL, S. M. et al. Graph Theory and Algorithms for Network Analysis. 399. ed. E3S Web of Conferences, 2023.

---

## 2. Arquitetura em Camadas

> Insira o diagrama abaixo. Pode ser exportado do Draw.io, Excalidraw, etc.

![Diagrama de arquitetura](./docs/arquitetura_e2.png)

### Descrição das camadas

| Camada | Responsabilidade | Artefatos principais |
|--------|-----------------|----------------------|
| Apresentação (UI/CLI) | William | Interface Frontend, que vai incluir: Painel de Visualização de Grafo, Opções de Métricas e Análises, Tela de Resultados(Dispositivos e Conexões Críticas, Dispositivos importantes, HOPS, etc.). |
| Aplicação (Service) | José | O serviço aplicados serão Scan de Rede, aplicado com python-nmap, Construtor de Grafo com NetworkX, Calculo de Centralidade de Grau e Intermediação com NetworkX, Analíse de Resiliência com Tarjan e Detecção e Componentes e Caminho mais Curto com BFS. |
| Domínio (Core) | Matheus | Lista de Adjacência para construir grafos, BFS que será usado para encontrar componentes conectados, Tarjan será usado para encontrar Pontos de Articulação e Pontes, Calculo de Centralidade para encontrar disposisitivos importantes dentro da rede. |
| Infraestrutura (I/O) | William e Matheus | Coleta de Dados responsável por python-nmap, que irá importar os dados recebidos e construir o grafo com NetworkX, os grafos poderão ser exportados em formato JSON. |

---

## 3. Estrutura de Diretórios

```
NetGraph/
├── docs/
│   ├── README.md
│   └── E1_Grupo3_Avaliação.md
│   └── E2_Grupo3_Designer_Técnico.md
├── src/
│   ├── core/
│   │   ├── graph.py          
│   │   ├── edge.py
│   │   ├── vertex.py
│   │   └── devices.py
│   ├── algorithms/
│   │   ├── BFS.py
│   │   ├── tarjan.py
│   │   ├── centrality_network.py
│   ├── ui/
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── graph_dashboard.py          
│   ├── io/ 
│   │   ├── json_exporter.py
│   └── main.py
├── tests/
│   ├── test_graph.py
│   ├── test_BFS.py
│   └── test_tarjan.py
├── data/
└── requirements.txt          
```

> **Justificativa de desvios** *(se houver)*: 

- Incluímos a pasta UI para conter nossa interface web

## 4. Definição do Dataset

**Formato de entrada aceito:**

Lista de Adjacência

**Exemplo de estrutura do arquivo de entrada:**

```json
grafo = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 4],
    3: [1],
    4: [1, 2]
}
```

**Estratégia de geração aleatória:**

| Parâmetro | Descrição |
|-----------|-----------|
| Número de vértices | Quantidade de dispositivos, configurável via argumento |
| Densidade | Probabilidade de existência de conexões entre pares de dispositivos (0.0 a 1.0) | 
---

## 5. Backlog do Projeto

### 5.1 In-Scope — O que será implementado

| # | Funcionalidade | Prioridade | Critério de aceite |
|---|---------------|------------|-------------------|
| 1 | Mapear estrutura de rede de computadores como um grafo visual | Alta | Dado uma rede local com dispositivos ativos identificados durante a varredura utilizando a biblioteca "python-nmap", quando o usuário executar o mapeamento da rede, então o sistema deverá gerar e exibir um grafo visual contendo os dispositivos como vértices e suas conexões como arestas. |
| 2 | Medir resiliência estrutural | Alta | Dado um grafo representando a rede, quando o usuário executar o algoritmo de Tarjan, então o sistema deverá identificar e exibir pontos de articulação e pontes, indicando dispositivos e conexões cuja remoção pode comprometer a conectividade da rede. |
| 3 | Encontrar dispositivos importantes | Média | Dado um grafo representando a topologia da rede, quando o usuário executar a análise de centralidade, então o sistema deverá calcular e exibir os dispositivos com maior grau e maior centralidade de intermediação com uso da biblioteca NetworkX, identificando nós críticos da rede. |
| 4 | Calcular menores distâncias entre dispositivos | Baixa | Dado um grafo representando a rede e um dispositivo de origem selecionado, quando o usuário executar o BFS, então o sistema deverá calcular e exibir o menor número de hops entre o dispositivo de origem e os demais dispositivos alcançáveis na rede. |
| 5 | Detectar componentes conectados | Baixa | Dado um grafo representando a rede, quando o usuário executar a análise de componentes conectados com BFS, então o sistema deverá identificar e exibir grupos de dispositivos conectados e possíveis segmentos isolados da rede. |

### 5.2 Out-of-Scope — O que NÃO será feito

| Funcionalidade excluída | Motivo |
|------------------------|--------|
| Calcular Corte Mínimo | Determinar quantos dispositivos precisam ser desconectados para a rede cair, os os algoritmos por trás do calculo do Corte Mínimo para grafos não direcionados e não ponderados estão muito além do nosso conhecimento atual, e ainda estão desenvolvendo algoritmos tentando alcalçar uma complexidade próxima da linear em várias aplicações. |
| Calcular Fluxo Máximo da rede baseado em Banda Larga | Utilizariamos o algoritmo de Ford-Fulkerson para encontrar Fluxo-Máximo e Corte Mínimo, o motivo da exclusão foi o tipo de grafo que não é de fluxo, e algoritmos como Ford-Fulkerson e Edmonds-Karp são recomendados em pelo menos grafos direcionados e ponderados, pode ser realizado em futuras implementações. |
| Expandir Rede | Usar Link Prediction em grafos, onde o sistema poderia indicar a melhor configuração, para instalar novos dispositivos, porém ao analisar a complexidade do problema, onde extendiam para Machine Leaning, descartamos rapidamente a ideia.  |

---

## Checklist de Entrega

- [ X ] Big-O de tempo e espaço declarados para cada algoritmo
- [ X ] Ao menos 1 alternativa descartada com justificativa
- [ X ] Diagrama de arquitetura com 4 camadas identificadas
- [ X ] Referência bibliográfica para cada algoritmo (ABNT ou IEEE)
- [ X ] Backlog com ≥ 5 itens In-Scope e ≥ 3 Out-of-Scope
- [ X ] Ao menos 3 critérios de aceite no formato "dado / quando / então"
- [ X ] Exemplo de estrutura de arquivo de entrada presente

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
