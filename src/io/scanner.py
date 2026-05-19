import ipaddress
import socket

import nmap
import psutil
from scapy.all import conf, get_if_addr


# Funcao para encontrar gateway do sistema, que normalmente sao
# Roteadores ou tambem Switchs
def encontrar_gateway():
    gateway = conf.route.route("0.0.0.0")[2]

    return gateway


def mapear_rede(ip_alvo):
    # 1. Instanciamos o scanner do Nmap
    nm = nmap.PortScanner()
    print(f"Varrendo a rede {ip_alvo}... (Isso pode demorar alguns segundos)")

    # Realiza um Ping Scan rápido (-sn) para descobrir hosts online
    nm.scan(hosts=ip_alvo, arguments="-sn")

    dispositivos = {}

    # Obtendo gateway
    gateway = encontrar_gateway()

    # Passando por todos os hosts scaneados
    for host in nm.all_hosts():
        # nm.scan(hosts=host, arguments="--top-ports 1000 -sS")

        # Criando um dicionario de dicionarios para armazenar cada dispositivo
        dispositivos[host] = {}

        # Obtendo IP
        dispositivos[host]["IP"] = host

        # Obtendo status do host (up ou down)
        dispositivos[host]["status"] = nm[host].state()

        # Inferindo tipo gateway ou host
        dispositivos[host]["tipo"] = "gateway" if host == gateway else "host"

        # Verificando se o host possui endereco MAC
        if "mac" in nm[host]["addresses"].keys():
            # Caso sim, obtendo endereco MAC
            dispositivos[host]["MAC"] = nm[host]["addresses"]["mac"]
        else:
            # Caso nao, armazene None
            dispositivos[host]["MAC"] = None

        # Verificando se o dispositivo possui um fabricante vinculado
        if nm[host]["vendor"] != {}:
            # Caso sim, obtendo informacao do fabricante
            dispositivos[host]["vendor"] = nm[host]["vendor"][
                nm[host]["addresses"]["mac"]
            ]
        else:
            # Caso nao, armazene None
            dispositivos[host]["vendor"] = None

    return dispositivos


# Descobrindo subnet do usuario
# deve resolver ips de qualquer classe e CIDR
def resolver_subnet(ip):
    subnet = ipaddress.ip_network(ip, strict=False)

    # Retorna ip da rede com CIDR correto = XXX.XXX.XXX.0/XX
    return subnet.with_prefixlen


# Solucao para descobrir IP do host do usuario
def descobrir_ip():
    # Obtendo endereco de IP da maquina do usuario
    host = socket.gethostname()

    ip = socket.gethostbyname(host)

    # Encontrando a mascara da subrede
    for enderecos in psutil.net_if_addrs().values():
        # Passando por cada atributo da interface
        for endereco in enderecos:
            # Reduzindo os ips para apenas IPv4
            if endereco.family == socket.AF_INET:
                # Caso ache ip da maquina, obtenha a mascara da subrede associada
                if endereco.address == ip:
                    netmask = endereco.netmask
                    break

    # Obtendo ip local completo
    ip_local = ip + "/" + netmask

    # Resolvendo subnet
    ip_subnet = resolver_subnet(ip_local)

    return ip_subnet
