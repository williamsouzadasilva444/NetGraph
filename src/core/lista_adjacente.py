import json

from ..io import scanner


# Ira transformar
def definir_dispositivos():
    ip = scanner.descobrir_ip()

    dispositivos = scanner.mapear_rede(ip)

    dispositivos_json = json.dumps(dispositivos, indent=4)
    print(dispositivos_json)
    pass
