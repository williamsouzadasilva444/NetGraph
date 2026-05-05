import nmap
import networkx as nx
import json

def mapear_rede(ip_alvo):
    # 1. Instanciamos o scanner do Nmap
    nm = nmap.PortScanner()
    print(f"Varrendo a rede {ip_alvo}... (Isso pode demorar alguns segundos)")
    
    # Realiza um Ping Scan rápido (-sn) para descobrir hosts online
    nm.scan(hosts=ip_alvo, arguments='-sn')
    
    # 2. Criamos o nosso Grafo no NetworkX
    G = nx.Graph()
    gateway = '192.168.0.1' # Exemplo: O roteador principal (Nó raiz)
    
    G.add_node(gateway, tipo='roteador')
    
    # 3. Inserindo os dados do Nmap no Grafo
    for host in nm.all_hosts():
        if host != gateway:
            # Pegando informações úteis
            hostname = nm[host].hostname() if nm[host].hostname() else host
            estado = nm[host].state()
            
            # Adiciona o Host como um Nó
            G.add_node(host, name=hostname, state=estado)
            
            # Cria a aresta (ligação) entre o roteador e esse host
            G.add_edge(gateway, host)
            
    return G

# Vamos mapear sua rede local (exemplo comum de gateway base)
grafo_da_rede = mapear_rede('192.168.0.1/24')
