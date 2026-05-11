import nmap

def scan_network(alvo):
    nm = nmap.PortScanner()
    nm.scan(hosts=alvo, arguments='-sn')

    hosts = []
    for host in nm.all_hosts():
        hosts.append({
            'ip': host,
            'status': nm[host].state(),
            'hostname': nm[host].hostname() or 'desconhecido'
        })

    return {'nodes': hosts}