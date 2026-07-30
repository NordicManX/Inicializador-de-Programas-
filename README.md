# 🚀 Orquestrador de Inicialização de Servidor

Um gerenciador de inicialização customizado para servidores Windows, desenvolvido em Python. Ele orquestra a abertura de sistemas de retaguarda em lote (como módulos de ERP, bancos de dados e serviços de link), garantindo que cada serviço tenha tempo suficiente para carregar antes de ser ocultado da tela.

## 🎯 O Problema que Resolvemos (O "Porquê")

Sistemas modulares complexos costumam causar travamentos ou erros de conexão se forem ditosparados simultaneamente logo no boot do servidor. Além disso, as janelas de console desses sistemas poluem a Área de Trabalho. Este proje resolve essa dor através de:

* **Atraso Inicial:** Aguarda o carregamento completo do Windows e serviços de rede (ex: 3 minutos) antes de iniciar a esteira.
* **Fila de Execução Inteligente:** Abre um programa, aguarda o tempo de processamento (20 segundos) e minimiza a janela à força usando a API nativa do Windows, repetindo o ciclo ordenadamente.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface Gráfica:** `tkinter` (Biblioteca nativa)
* **Integração OS:** `ctypes` (Acesso direto à API do Windows para varredura de janelas) e `subprocess`
* **Busca de PID:** Varredura invisível via linha de comando (`tasklist /FO CSV`)
* **Compilação:** `PyInstaller` (Empacotamento em `.exe` independente)
* **Infraestrutura:** Agendador de Tarefas do Windows (Task Scheduler)

## ⚙️ Como a Arquitetura Funciona

O projeto é dividido em dois microsserviços embutidos em arquivos `.exe`, que se comunicam através de um arquivo de configuração `.json`:

1. **`inicializador.exe` (A Interface):** Uma tela visual onde o administrador configura o tempo de espera inicial e seleciona os caminhos dos executáveis que devem ser abertos, criando o arquivo `config_programas.json`.
2. **`executor.exe` (O Trabalhador):** O script invisível (rodando em *background*). Ele lê o `.json`, obedece aos tempos estipulados, abre os softwares e caça os PIDs (Process IDs) ativos, enviando o comando de minimização (`SW_FORCEMINIMIZE`) direto para o núcleo do Windows.

---

## 🚀 Guia de Deploy no Servidor

### 1. Preparação da Infraestrutura
Crie uma pasta raiz segura no servidor (ex: `C:\Script_inicializador_Não_remover\`) e armazene os arquivos `inicializador.exe` e `executor.exe` dentro dela.

### 2. Configuração dos Softwares
1. Execute o `inicializador.exe`.
2. Defina o tempo de atraso inicial em segundos (ex: `180` para 3 minutos).
3. Adicione os programas na ordem lógica de dependência.
4. Clique em **Salvar Configurações**. 

### 3. Configuração do Agendador de Tarefas (Elevação de Privilégios)
Para que o script possua poder administrativo para minimizar janelas do sistema:

1. Abra o **Agendador de Tarefas** do Windows e clique em **Criar Tarefa...**
2. **Aba Geral:** Nomeie a tarefa e marque a caixa **Executar com privilégios mais altos**.
3. **Aba Disparadores (Gatilho):** Adicione um novo disparador com a opção **Ao fazer logon** (apontando para o usuário Administrador). Isso garante que a Área de Trabalho exista antes de desenhar as janelas.
4. **Aba Ações:** 
    * Ação: *Iniciar um programa*.
    * Programa/script: Aponte para o `C:\Script_inicializador_Não_remover\executor.exe`.
    * **Iniciar em (opcional):** Digite `C:\Script_inicializador_Não_remover\` *(Sem aspas. Passo crucial para a leitura do JSON)*.
5. **Aba Condições:** Desmarque a exigência de estar ligado à rede elétrica.

Salve a tarefa e o servidor estará orquestrado.


# 📦 Guia de Compilação: Transformando Python em Executável (.exe)

Este guia documenta o processo de transformação dos scripts Python (`.py`) em arquivos executáveis independentes (`.exe`). 

**Por que compilar?**
Ao transformar os arquivos em `.exe`, embutimos o interpretador do Python e todas as dependências no próprio arquivo. Isso significa que o projeto pode rodar nativamente em qualquer servidor Windows, sem a necessidade de instalar a linguagem Python ou configurar variáveis de ambiente na máquina de destino.

---

## 🛠️ Pré-requisitos

Antes de iniciar a compilação, você precisa ter o Python instalado na sua máquina de desenvolvimento e instalar a biblioteca **PyInstaller**, que é o "motor" que fará a conversão.

1. Abra o Terminal (Prompt de Comando ou PowerShell).
2. Execute o comando de instalação:
   ```cmd
   pip install pyinstaller
   ```

   #⚙️ Passo a Passo da Compilação
Para evitar problemas de permissão ou falta de reconhecimento do comando no Windows, utilizaremos o prefixo python -m, que força o Python a localizar o módulo do PyInstaller internamente.

### 1. Compilando a Interface Gráfica
Navegue pelo terminal até a pasta onde está o código fonte e execute:
```cmd

python -m PyInstaller --noconsole --onefile inicializador.py
```

### 2. Compilando o Executor Invisível
Aguarde o término do comando anterior e execute o próximo:

```cmd
python -m PyInstaller --noconsole --onefile executor.py
```

O Porquê das Flags (Parâmetros):

--onefile: Instrui o PyInstaller a não criar uma pasta cheia de bibliotecas espalhadas, mas sim compactar tudo em um único e limpo arquivo .exe.

--noconsole: É vital para este projeto. Ele impede que a tela preta do terminal do Windows (cmd) seja aberta. Isso garante que a interface gráfica fique limpa e que o executor rode 100% invisível em segundo plano no servidor.

# 📂 Onde estão os meus arquivos?
Após a execução dos comandos, o PyInstaller criará novas pastas no seu diretório (build, dist e arquivos .spec).

Você pode ignorar ou apagar as pastas build e os arquivos .spec.

Entre na pasta dist (Distribution).

Lá dentro estarão os seus arquivos finais: inicializador.exe e executor.exe. Estes são os únicos arquivos que você precisa copiar para o servidor.

# ⚠️ Solução de Problemas Comuns
1. O executor.exe não apareceu na pasta dist ou sumiu rapidamente:
O PyInstaller cria .exes genéricos compactados, técnica também usada por malwares. É comum o Windows Defender ou antivírus de terceiros darem um "falso positivo" e deletarem o arquivo silenciosamente.

Solução: Vá no Histórico de Proteção do antivírus, localize a ameaça recém-bloqueada e selecione "Restaurar" ou "Permitir no dispositivo". Recompile se necessário.

2. Erro "O termo 'pyinstaller' não é reconhecido":
Isso ocorre quando o PyInstaller é instalado em uma pasta de usuário que não está no PATH do Windows.

Solução: Utilize sempre o comando completo com o prefixo python -m PyInstaller em vez de chamar apenas pyinstaller.

---

> ⚡ **Desenvolvido por Nordic-Tech**
> 
> *Feito com muita pressa hahahaha! (Mas o que importa é que está em produção e funcionando perfeitamente 🚀)*

