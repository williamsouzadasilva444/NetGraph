import socket

import nmap


def mapear_rede(ip_alvo):
    # 1. Instanciamos o scanner do Nmap
    nm = nmap.PortScanner()
    print(f"Varrendo a rede {ip_alvo}... (Isso pode demorar alguns segundos)")

    # Realiza um Ping Scan rápido (-sn) para descobrir hosts online
    nm.scan(hosts=ip_alvo, arguments="-sn")

    dispositivos = {}

    # Passando por todos os hosts scaneados
    for host in nm.all_hosts():
        # nm.scan(hosts=host, arguments="--top-ports 1000 -sS")

        # Criando um dicionario de dicionarios para armazenar cada dispositivo
        dispositivos[host] = {}

        # Obtendo IP
        dispositivos[host]["IP"] = host

        # Obtendo status do host (up ou down)
        dispositivos[host]["status"] = nm[host].state()

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


# Solucao temporaria e fraca, para descobrir o subnet do usuario
# Por enquanto so resolve ips de classe C com CIDR /24
def resolver_subnet(ip):
    # Acha o primeiros octavo do endereco IP
    first_octo = ip.find(".", 8)

    # Copia apenas o 3 primeiros octavos
    ip = ip[: (first_octo + 1)]

    # Retorna subnet = XXX.XXX.XXX.0/24
    return ip + "0/24"


# Solucao para descobrir IP do host do usuario
def descobrir_ip():
    # Obtendo endereco de IP do usuario
    host = socket.gethostname()

    ip_local = socket.gethostbyname(host)

    ip_subnet = resolver_subnet(ip_local)

    return ip_subnet
