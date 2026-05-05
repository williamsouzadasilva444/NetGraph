# E1 — Proposta e Definição do Projeto
> **Disciplina:** Teoria dos Grafos
> > **Prazo:Peso:** 10% da nota final 18 de março de 2026

---
## Identificação do Grupo
| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | GraphNet |
| Integrante 1 | William Souza — 41057619 |
| Integrante 2 | Matheus Akira Saito de Souza — 38746344 |
| Integrante 3 | José Gonçalves Braz Júnior — 40789659 |
| Domínio de aplicação | Redes de Computadores |
---
## 1. Contexto e Motivação
> Descreva o problema do mundo real que será abordado. Por que ele é relevante?
> *Orientação: 2 a 3 parágrafos. Seja específico — evite generalizações.*
> Na área de redes de computadores, os Administradores de Rede, são os responsáveis por garantir a operação contínua e eficiente da infraestrutura após implementação. Mas, estruturas de redes estão sujeitos a problemas que podem prejudicar a performance da rede e a disponibilidade de serviços. Indentificar esses problemas podem tomar muito tempo dos analistas por conta da falta de visão estruturada da rede.
> Administradores de Redes precisam monitorar a estrutura de forma precisa para observar possíveis problemas, como detecção de anomalias, problemas de performance, dispositivos não autorizados etc. Mesmo que programas como NMap, já realizam a parte de mapear a estrutura da rede, muito das informações apresentadas não são intuitivas e ficam por parte do administrador interpretar. A aplicação de Teoria dos Grafos, pode modelar os dispositivos e representar a estrutura de rede de forma gráfica, além de podermos usar conceitos como conectividade de grafos para contribuir para identificação de problemas.
> Para isso, nosso projeto é um Mapeador de Redes com o objetivo de gerar um mapa/grafo com os dispositivos que estão conectados em uma rede local utilizando a biblioteca NMap do Python, para auxiliar administradores a compreenderem e monitorarem a estrutura de forma clara.
---
## 2. Objetivo Geral
> O que o sistema deve ser capaz de fazer ao final?
> *Orientação: 1 frase clara e objetiva. Ex.: "O sistema deve calcular a rota de menor custo entre dois pontos em um mapa urbano."*
> Descobrir cada dispositivo conectado em uma rede local com NMap, e gerar um grafo com base nos dispositivos indentificados.
---
## 3. Objetivos Específicos
> Desmembre o objetivo geral em metas mensuráveis.
> *Orientação: liste entre 3 e 5 itens. Cada item deve ser verificável — use verbos como "implementar", "calcular", "exibir", "carregar".*

- [ Criar interface web, e utilizar Flask para criar a aplicação] 
- [ Exibir grafo na interface web utilizando NetworkX]   
- [ Identificar pontos centrais dentro de uma rede, como hubs e switches.  ]
- [ Identificar pontos críticos, onde pode oferecer riscos para a estrutura e conexão de outros serviços ]
- [ Analisar caminhos alternativos e resiliência da estrutura ]
---
## 4. Público-Alvo / Caso de Uso Principal
> Para quem ou em qual cenário o sistema seria utilizado?
> bairro."*Orientação: descreva um cenário concreto de uso. Ex.: "Um entregador de aplicativo que precisa otimizar a sequência de entregas em um *

> Analistas e Administradores de Rede, serão o principal público-alvo, com o intuito de auxiliar em certos casos como, por exemplo: O cliente percebe que a sua internet está mais lenta que o normal, o administrador usa o GraphNet para analisar a centralidade da rede e indentificar dispositivos com alto tráfego, caso o Administrador encontre qualquer dispositivo suspeito, ele poderá usar a ferramenta de corte, para analisar quais dispositivos devem ser desconectados para isolar tal dispositivo, sem que afete a estrutura inteira da rede.
---
## 5. Justificativa Técnica — Por que Grafos?
> Por que a modelagem em grafo é a abordagem mais adequada para este problema?
> que reforçam a escolha.*Orientação: explique quais elementos do problema mapeiam naturalmente para vértices e arestas. Mencione se há pesos, direção, ou restrições *

> A modelagem em grafos permite uma visualização intuitiva da estrutura da rede, podemos descrever cada dispositivo como um vértice, e as conexões (PC – Switch) serão nossas arestas. Como em uma estrutura de redes os dispositivos mantém uma conexão mútua podemos representar como um Grafo Não-Dirigido.
> Além disso podemos utilizar de conceitos como centralidade, para identificar dispositivos importantes como switches que são responsáveis por distribuir sinal para vários dispositivos conectados a ele. Vértices de corte para encontrar dispositivos e conexões críticas, que podem falhar a rede se forem desconectados. Conectividade para detectar sub redes dentro da estrutura e avaliar a resistência da rede caso haja falha de certos dispositivos, utilizando DFS/BFS para identificar esses pontos e contribuir para interpretação do administrador.

---
## 6. Tipo de Grafo
> Especifique as características do grafo que o problema requer.


| Característica | Escolha | Justificativa breve |
|----------------|---------|---------------------|
| Dirigido ou não-dirigido | Não-Dirigido | Como nosso objetivo geral é mapear toda rede Ethernet local, um grafo não-dirigido será adequado para demonstrar que os dispositivos conectados possuem conexão mútua. Uma implementação dirigida, para identificar tráfego de pacotes podem ser implementados no futuro. |
| Ponderado ou não-ponderado | Não-ponderado | Não entra no escopo do objetivo geral, pode ser ponderado em futuras implementações |
| Conectado / bipartido / geral | Geral | Porque iremos apresentar apenas uma rede, um grafo geral deve ser suficiente |
| Representação interna pretendida | Lista de Adjacência | Como não iremos saber exatamente quantos dispositivos podem estar conectados em uma rede, uma lista de adjacência será bem menos complexo em questão de espaço |

---
## 7. Diagrama Conceitual
>> Insira aqui ao menos uma figura que ilustre o domínio do problema. *Pode ser uma imagem exportada do Draw.io, Excalidraw, foto de esboço à mão etc.*

![diagrama_exemplo](E1_Grupo3_Grafo.jpg "Diagrama Rede")
****Legenda: O diagrama acima, demonstra um grafo simples não-direcionado, com 4 vértices. Cada vértice contém seu Nome, Tipo e IP, sendo que tipos diferentes contém símbolos diferentes, Hosts(Círculos) e Switch(Quadrado). o Grafo está conectado de uma forma para representar uma Topologia Estrela**
---
## Checklist de Entrega
Antes de submeter, confirme:

- [ X ] Texto entre 300 e 600 palavras (seções 1 a 5)
- [ X ] Todos os campos da tabela de identificação preenchidos [ X ] Tipo de grafo especificado com justificativa
- [ X ] Diagrama presente e referenciado no texto 
- [ X ] Arquivo nomeado como `E1_NomeGrupo_Grafos.docx` (versão Word) ou PR aberto (versão GitHub)

---
*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*


