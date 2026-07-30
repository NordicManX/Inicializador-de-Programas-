import json
import os
import time
import subprocess

ARQUIVO_CONFIG = "config_programas.json"

def carregar_configuracao():
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, 'r') as arquivo:
                return json.load(arquivo)
        except:
            pass
    return None

def iniciar_programas():
    config = carregar_configuracao()
    
    if not config or "programas" not in config or not config["programas"]:
        return

    tempo_espera = config.get("atraso_segundos", 180) 
    programas = config["programas"]
    
    # 1. Espera inicial do servidor para os serviços subirem
    time.sleep(tempo_espera)

    for programa in programas:
        try:
            # 2. Abre o programa (ex: SIMServer.exe)
            subprocess.Popen(programa)
            
            # 3. Aguarda 20 segundos ANTES de abrir o próximo programa da lista.
            # A janela ficará aberta na tela, e o servidor terá tempo de respirar.
            time.sleep(20) 
                
        except Exception as e:
            pass

if __name__ == "__main__":
    iniciar_programas()