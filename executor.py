import json
import os
import time
import subprocess
import ctypes
from ctypes import wintypes
import csv
import io

ARQUIVO_CONFIG = "config_programas.json"

# Comando 11 é o FORCEMINIMIZE (Minimiza até janelas teimosas que não respondem)
SW_FORCEMINIMIZE = 11

def obter_pids_por_nome(nome_executavel):
    """Procura no Gerenciador de Tarefas todos os PIDs com o nome do programa."""
    pids = []
    try:
        # Executa o comando tasklist do Windows invisivelmente
        comando = f'tasklist /FO CSV /NH /FI "IMAGENAME eq {nome_executavel}"'
        saida = subprocess.check_output(comando, shell=True, text=True)
        
        # Lê a resposta e extrai os números dos PIDs
        leitor = csv.reader(io.StringIO(saida))
        for linha in leitor:
            if len(linha) > 1 and linha[1].isdigit():
                pids.append(int(linha[1]))
    except Exception:
        pass
    return pids

def minimizar_janelas(pids):
    """Varre o Windows e força a minimização das janelas dos PIDs informados."""
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    ShowWindow = ctypes.windll.user32.ShowWindow
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW

    def callback(hwnd, lparam):
        if IsWindowVisible(hwnd):
            pid_out = ctypes.c_ulong()
            GetWindowThreadProcessId(hwnd, ctypes.byref(pid_out))
            
            # Se a janela pertence a um dos PIDs do nosso programa...
            if pid_out.value in pids:
                # Confere se a janela tem um Título (evita minimizar janelas invisíveis de sistema)
                if GetWindowTextLength(hwnd) > 0:
                    ShowWindow(hwnd, SW_FORCEMINIMIZE)
        return True

    EnumWindows(EnumWindowsProc(callback), 0)

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
    
    # 1. Espera inicial do servidor
    time.sleep(tempo_espera)

    for programa in programas:
        try:
            # Descobre o nome do executável (ex: pega "SIMServer.exe" a partir de "F:/Prisma/SIMServer.exe")
            nome_exe = os.path.basename(programa)
            
            # 2. Abre o programa
            subprocess.Popen(programa)
            
            # 3. Aguarda os 20 segundos cruciais para o programa carregar na tela
            time.sleep(20) 
            
            # 4. Procura o(s) novo(s) PID(s) reais no Gerenciador de Tarefas pelo nome
            pids_reais = obter_pids_por_nome(nome_exe)
            
            # 5. Força a minimização
            if pids_reais:
                minimizar_janelas(pids_reais)
                
        except Exception as e:
            pass

if __name__ == "__main__":
    iniciar_programas()