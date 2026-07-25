import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

ARQUIVO_CONFIG = "config_programas.json"

def carregar_configuracao():
    """Lê o arquivo JSON. Agora retorna um dicionário com tempo e programas."""
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, 'r') as arquivo:
                dados = json.load(arquivo)
                # Verifica se o arquivo lido é um Dicionário (dict). 
                # Se for o formato antigo (lista), ele ignora e cria um novo.
                if isinstance(dados, dict):
                    return dados
        except Exception:
            # Se o arquivo estiver corrompido, ele passa reto e recria
            pass
            
    # Retorno padrão caso não exista ou seja o formato antigo
    return {"atraso_segundos": 180, "programas": []}
    """Lê o arquivo JSON. Agora retorna um dicionário com tempo e programas."""
    if os.path.exists(ARQUIVO_CONFIG):
        with open(ARQUIVO_CONFIG, 'r') as arquivo:
            return json.load(arquivo)
    # Se não existir, retorna esse formato padrão:
    return {"atraso_segundos": 180, "programas": []}

def salvar_configuracao():
    """Salva o tempo digitado e a lista visual no JSON."""
    try:
        # Pega o que o usuário digitou na caixinha de tempo e converte para número (inteiro)
        tempo = int(entry_tempo.get())
    except ValueError:
        messagebox.showerror("Erro", "O tempo deve ser um número inteiro!")
        return

    programas_atuais = list(listbox_programas.get(0, tk.END))
    
    dados_para_salvar = {
        "atraso_segundos": tempo,
        "programas": programas_atuais
    }
    
    with open(ARQUIVO_CONFIG, 'w') as arquivo:
        json.dump(dados_para_salvar, arquivo)
    
    messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")

def adicionar_programa():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o programa",
        filetypes=[("Executáveis", "*.exe"), ("Todos os arquivos", "*.*")]
    )
    if caminho_arquivo:
        listbox_programas.insert(tk.END, caminho_arquivo)

def remover_programa():
    selecao = listbox_programas.curselection()
    if selecao:
        listbox_programas.delete(selecao)

# --- Construção da Interface Gráfica ---
janela = tk.Tk()
janela.title("Configurador de Inicialização")
janela.geometry("550x450")
janela.config(padx=15, pady=15)

# Carrega os dados que já existem (ou os padrões)
config = carregar_configuracao()

# --- Sessão do Tempo ---
frame_tempo = tk.Frame(janela)
frame_tempo.pack(pady=10, anchor="w")

tk.Label(frame_tempo, text="Tempo de espera (em segundos): ").pack(side=tk.LEFT)
entry_tempo = tk.Entry(frame_tempo, width=10)
entry_tempo.pack(side=tk.LEFT)
entry_tempo.insert(0, str(config["atraso_segundos"])) # Preenche com o tempo salvo

# --- Sessão da Lista de Programas ---
tk.Label(janela, text="Programas para iniciar:").pack(anchor="w")

listbox_programas = tk.Listbox(janela, width=80, height=12)
listbox_programas.pack(pady=5)

for prog in config["programas"]:
    listbox_programas.insert(tk.END, prog)

# --- Botões de Ação ---
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

tk.Button(frame_botoes, text="Adicionar Programa", command=adicionar_programa).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text="Remover Selecionado", command=remover_programa).grid(row=0, column=1, padx=5)

# Botão gigante de Salvar no final
tk.Button(janela, text="SALVAR CONFIGURAÇÕES", bg="green", fg="white", command=salvar_configuracao, height=2).pack(pady=15, fill="x")

janela.mainloop()