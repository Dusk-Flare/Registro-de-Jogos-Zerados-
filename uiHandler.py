import tkinter as tk
from tkinter import messagebox, filedialog, Menu, END, ttk
import json
import datetime
from datetime import datetime
import re
import os
import webbrowser
import urllib.parse
import pyperclip
from PIL import Image, ImageTk
from extraUtils import*
from listHandler import*
from mainUltimate import*
from statisticManager import*
from externalManager import*
from uiHandler import*

def estilizar_botao(botao, cor_fundo, cor_texto="white", fonte=("Arial", 10, "bold"),
                    largura=20, altura=2, wrap=150, borda=3, efeito_hover="#333333"):
    botao.config(
        bg=cor_fundo, fg=cor_texto,
        font=fonte,
        width=largura, height=altura,
        wraplength=wrap,
        relief="raised", bd=borda,
        cursor="hand2"
    )

    # Efeito hover personalizável
    botao.bind("<Enter>", lambda e: botao.config(bg=efeito_hover))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor_fundo))


def abrir_menu_contexto(event):
    # Obter o índice do item clicado com o botão direito
    index = lista_jogos_listbox.nearest(event.y)

    # Selecionar o item correspondente
    lista_jogos_listbox.selection_clear(0, END)  # Limpar seleções anteriores
    lista_jogos_listbox.selection_set(index)  # Selecionar o item clicado
    lista_jogos_listbox.activate(index)  # Focar no item clicado

    # Verificar se há uma seleção válida antes de abrir o menu
    if not lista_jogos_listbox.curselection():
        return

    # Criar um menu de contexto
    menu = Menu(lista_jogos_listbox, tearoff=0)
    menu.add_command(label="Pesquisar no Google", command=pesquisar_no_google)
    menu.add_command(label="Copiar nome do Jogo", command=copiar_nome)
    menu.add_command(label="Organizar lista", command=abrir_menu_organizacao)
    menu.add_command(label="Filtrar", command=mostrar_jogos_filtrados)
    menu.add_command(label="Limpar Filtros", command=limpar_filtros)
    menu.add_command(label="Editar jogo", command=editar_jogo)
    menu.add_command(label="Excluir Jogo", command=excluir_jogo)

    # Exibir o menu na posição do cursor
    menu.post(event.x_root, event.y_root)


def pesquisar_no_google():
    # Obtenha o índice do jogo selecionado
    indice_selecionado = lista_jogos_listbox.curselection()[0]
    jogo_selecionado = lista_jogos_listbox.get(indice_selecionado)

    # Use uma expressão regular para encontrar o título do jogo após o número e o ponto
    padrao_titulo = r'\d+\.\s*(.+)'
    correspondencia = re.search(padrao_titulo, jogo_selecionado)
    if correspondencia:
        titulo_do_jogo = correspondencia.group(1)
    else:
        titulo_do_jogo = "Título não encontrado"

    # Remover apenas os emojis ✅, 📅, ❌
    titulo_sem_emojis = re.sub(r'[✅📅❌]', '', titulo_do_jogo)

    # Criar uma URL de pesquisa no Google com o título limpo
    pesquisa_google_url = f"https://www.google.com/search?q={urllib.parse.quote(titulo_sem_emojis)}"

    # Abrir o navegador padrão para realizar a pesquisa
    webbrowser.open(pesquisa_google_url)


def editar_jogo():
    global filtro_window, janela_edicao, nota_entry
    selecionado = lista_jogos_listbox.curselection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um jogo para editar.")
        return

    indice = int(selecionado[0])

    if 0 <= indice < len(lista_jogos):
        jogo_selecionado = lista_jogos[indice]

        janela_edicao = tk.Toplevel(root)
        janela_edicao.title("Editar Jogo")
        janela_edicao.geometry("330x370")
        janela_edicao.resizable(False, False)
        centralizar_janela(janela_edicao, 330, 370)

        # Criar rótulos e entradas
        tk.Label(janela_edicao, text="Título:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, padx=5, pady=5, sticky="W")
        tk.Label(janela_edicao, text="Gênero:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, padx=5, pady=5, sticky="W")
        tk.Label(janela_edicao, text="Plataforma:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, padx=5, pady=5, sticky="W")
        tk.Label(janela_edicao, text="Data de Zeramento:", font=(
            "Arial", 10, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="W")
        tk.Label(janela_edicao, text="Forma de Zeramento:", font=(
            "Arial", 10, "bold")).grid(row=4, column=0, padx=5, pady=5, sticky="W")
        tk.Label(janela_edicao, text="Descrição de Zeramento:", font=(
            "Arial", 10, "bold")).grid(row=5, column=0, padx=5, pady=5, sticky="W")
        tk.Label(janela_edicao, text="Tempo Jogado (HH:MM):", font=(
            "Arial", 10, "bold")).grid(row=6, column=0, padx=5, pady=5, sticky="W")
        tk.Label(janela_edicao, text="Nota:", font=("Arial", 10, "bold")).grid(
            row=7, column=0, padx=5, pady=5, sticky="W")

        # Criar widgets de entrada
        titulo_edit = tk.Entry(janela_edicao)
        titulo_edit.insert(0, jogo_selecionado['Título'])

        genero_edit = ttk.Combobox(
            janela_edicao, values=generos_disponiveis, state="readonly")
        genero_edit.set(jogo_selecionado['Gênero'])

        plataforma_edit = ttk.Combobox(
            janela_edicao, values=plataformas_disponiveis, state="readonly")
        plataforma_edit.set(jogo_selecionado['Plataforma'])

        data_zeramento_edit = tk.Entry(janela_edicao)
        data_zeramento_edit.insert(0, jogo_selecionado['Data de Zeramento'])

        forma_zeramento_edit = ttk.Combobox(janela_edicao, values=[
                                            "História", "100%", "Platina", "Planejo Jogar", "Desistência", "Outro"], state="readonly")
        forma_zeramento_edit.set(jogo_selecionado['Forma de Zeramento'])

        descricao_zeramento_edit = tk.Entry(janela_edicao)
        descricao_zeramento_edit.insert(
            0, jogo_selecionado['Descrição de Zeramento'])

        tempo_jogado_edit_horas = tk.Spinbox(
            janela_edicao, from_=0, to=999, width=5)
        tempo_jogado_edit_minutos = tk.Spinbox(
            janela_edicao, from_=0, to=59, width=5)
        tempo_jogado = jogo_selecionado.get('Tempo Jogado', '').strip()
        if tempo_jogado:
            horas, minutos = map(int, tempo_jogado.split(":"))
        else:
            horas, minutos = 0, 0
        tempo_jogado_edit_horas.delete(0, tk.END)
        tempo_jogado_edit_horas.insert(0, horas)
        tempo_jogado_edit_minutos.delete(0, tk.END)
        tempo_jogado_edit_minutos.insert(0, minutos)

        nota_slider = tk.Scale(janela_edicao, from_=1,
                               to=10, orient=tk.HORIZONTAL)
        nota_slider.set(
            float(jogo_selecionado['Nota']) if jogo_selecionado['Nota'] else 1)

        # Posicionar widgets na janela
        titulo_edit.grid(row=0, column=1, padx=5, pady=5, sticky="EW")
        genero_edit.grid(row=1, column=1, padx=5, pady=5, sticky="EW")
        plataforma_edit.grid(row=2, column=1, padx=5, pady=5, sticky="EW")
        data_zeramento_edit.grid(row=3, column=1, padx=5, pady=5, sticky="EW")
        forma_zeramento_edit.grid(row=4, column=1, padx=5, pady=5, sticky="EW")
        descricao_zeramento_edit.grid(
            row=5, column=1, padx=5, pady=5, sticky="EW")
        tempo_jogado_edit_horas.grid(
            row=6, column=1, padx=5, pady=5, sticky="W")
        tempo_jogado_edit_minutos.grid(
            row=6, column=1, padx=5, pady=5, sticky="E")
        nota_slider.grid(row=7, column=1, padx=5, pady=5, sticky="EW")

        # Função para desativar/ativar campos com base no estado
        def atualizar_campos_edicao(estado):
            if estado in ["Planejo Jogar", "Desistência"]:
                # Desativar campos
                data_zeramento_edit.delete(0, tk.END)
                data_zeramento_edit.config(state="disabled")
                tempo_jogado_edit_horas.delete(0, tk.END)
                tempo_jogado_edit_horas.insert(0, 0)
                tempo_jogado_edit_horas.config(state="disabled")
                tempo_jogado_edit_minutos.delete(0, tk.END)
                tempo_jogado_edit_minutos.insert(0, 0)
                tempo_jogado_edit_minutos.config(state="disabled")
                nota_slider.set(1)
                nota_slider.config(state="disabled")
            else:
                # Reativar campos
                data_zeramento_edit.config(state="normal")
                tempo_jogado_edit_horas.config(state="normal")
                tempo_jogado_edit_minutos.config(state="normal")
                nota_slider.config(state="normal")

        # Chamar a função imediatamente com o estado atual
        atualizar_campos_edicao(forma_zeramento_edit.get())

        # Atualizar campos ao alterar o estado
        forma_zeramento_edit.bind(
            "<<ComboboxSelected>>", lambda event: atualizar_campos_edicao(forma_zeramento_edit.get()))

        # Botão para salvar alterações
        def salvar_edicao():
            try:
                jogo_selecionado['Título'] = titulo_edit.get()
                jogo_selecionado['Gênero'] = genero_edit.get()
                jogo_selecionado['Plataforma'] = plataforma_edit.get()
                jogo_selecionado['Data de Zeramento'] = data_zeramento_edit.get(
                ) if data_zeramento_edit["state"] == "normal" else ""
                jogo_selecionado['Forma de Zeramento'] = forma_zeramento_edit.get()
                jogo_selecionado['Descrição de Zeramento'] = descricao_zeramento_edit.get(
                )
                if tempo_jogado_edit_horas["state"] == "normal":
                    horas = int(tempo_jogado_edit_horas.get())
                    minutos = int(tempo_jogado_edit_minutos.get())
                    jogo_selecionado['Tempo Jogado'] = f"{horas}:{minutos:02d}"
                else:
                    jogo_selecionado['Tempo Jogado'] = ""
                jogo_selecionado['Nota'] = nota_slider.get(
                ) if nota_slider["state"] == "normal" else None

                messagebox.showinfo("Sucesso", "Jogo editado com sucesso!")
                atualizar_lista()
                janela_edicao.destroy()
            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao salvar as alterações: {e}")

        salvar_button = tk.Button(janela_edicao, text="Salvar Edição",
                                  command=salvar_edicao)
        salvar_button.grid(row=8, column=0, columnspan=2, pady=10)
        estilizar_botao(salvar_button, cor_fundo="gray", largura=20, altura=1)

        excluir_button = tk.Button(janela_edicao, text="Excluir Jogo", 
                                   command=lambda: [excluir_jogo(), janela_edicao.destroy()])
        excluir_button.grid(row=9, column=0, columnspan=2, pady=10)
        estilizar_botao(excluir_button, cor_fundo="gray", largura=20, altura=1)


def mostrar_jogos_filtrados():
    global filtro_window, filtro_titulo_entry, filtro_genero_entry, filtro_plataforma_combobox
    global filtro_min_nota_entry, filtro_max_nota_entry, filtro_ano_entry, filtro_metodo_combobox

    filtro_window = tk.Toplevel(root)
    filtro_window.title("Filtrar Jogos")
    filtro_window.geometry("420x370")
    filtro_window.resizable(False, False)
    centralizar_janela(filtro_window, 420, 370)

    # Rótulos e campos para os filtros
    filtros = [
        ("Título", 0, tk.Entry),
        ("Gênero", 1, ttk.Combobox),
        ("Plataforma", 2, ttk.Combobox),
        ("Nota mínima", 3, tk.Entry),
        ("Ano", 4, tk.Entry),
        ("Método de Zeramento", 5, ttk.Combobox)
    ]

    header_label = tk.Label(filtro_window, text="Selecione os Filtros", font=(
        "Arial", 14, "bold"), fg="#333")
    header_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    filtro_titulo_entry = tk.Entry(filtro_window, width=30)
    filtro_genero_entry = ttk.Combobox(
        filtro_window, values=generos_disponiveis, width=27)
    filtro_plataforma_combobox = ttk.Combobox(
        filtro_window, values=plataformas_disponiveis, width=27)
    filtro_min_nota_entry = tk.Entry(filtro_window, width=30)
    filtro_ano_entry = tk.Entry(filtro_window, width=30)
    filtro_metodo_combobox = ttk.Combobox(filtro_window, values=[
                                          "História", "100%", "Platina", "Planejo Jogar", "Desistência"], width=27)

    widgets = [
        ("Título", filtro_titulo_entry),
        ("Gênero", filtro_genero_entry),
        ("Plataforma", filtro_plataforma_combobox),
        ("Nota mínima", filtro_min_nota_entry),
        ("Ano", filtro_ano_entry),
        ("Método de Zeramento", filtro_metodo_combobox)
    ]

    for idx, (label_text, widget) in enumerate(widgets, start=1):
        label = tk.Label(filtro_window, text=label_text,
                         font=("Arial", 10, "bold"))
        label.grid(row=idx, column=0, padx=20, pady=10, sticky="E")
        widget.grid(row=idx, column=1, padx=20, pady=10, sticky="W")

    # Função para aplicar o filtro
    def aplicar_filtro():
        global jogos_filtrados
        filtros = {
            "Título": filtro_titulo_entry.get(),
            "Gênero": filtro_genero_entry.get(),
            "Plataforma": filtro_plataforma_combobox.get(),
            "Nota": filtro_min_nota_entry.get(),
            "Ano": filtro_ano_entry.get(),
            "Método": filtro_metodo_combobox.get()
        }

        def validar_jogo(jogo):
            if filtros["Título"] and filtros["Título"].lower() not in jogo["Título"].lower():
                return False
            if filtros["Gênero"] and filtros["Gênero"] != jogo["Gênero"]:
                return False
            if filtros["Plataforma"] and filtros["Plataforma"] != jogo["Plataforma"]:
                return False
            if filtros["Nota"]:
                try:
                    if float(jogo["Nota"]) < float(filtros["Nota"]):
                        return False
                except ValueError:
                    messagebox.showerror(
                        "Erro", "Nota inválida. Use números entre 1 e 10.")
                    return False
            if filtros["Ano"]:
                try:
                    ano_jogo = datetime.strptime(
                        jogo["Data de Zeramento"], "%d/%m/%Y").year
                    if int(filtros["Ano"]) != ano_jogo:
                        return False
                except ValueError:
                    messagebox.showerror("Erro", "Ano inválido.")
                    return False
            if filtros["Método"] and filtros["Método"] != jogo["Forma de Zeramento"]:
                return False
            return True

        jogos_filtrados = [jogo for jogo in lista_jogos if validar_jogo(jogo)]

        atualizar_lista(jogos_filtrados)
        filtro_window.destroy()

    botao_filtro = tk.Button(
        filtro_window, text="Aplicar Filtro", command=aplicar_filtro,
        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15
    )
    botao_filtro.grid(row=7, column=0, columnspan=2, pady=(10, 5))

    estilizar_botao(botao_filtro, cor_fundo="gray", largura=15, altura=1)


def gerenciar_checklist():
    pasta_saves = "saves"
    os.makedirs(pasta_saves, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_saves, "tarefas.json")

    checklist_window = tk.Toplevel(root)
    checklist_window.title("Tarefas")
    checklist_window.geometry("500x500")
    checklist_window.resizable(False, False)
    centralizar_janela(checklist_window, 500, 500)

    try:
        with open(caminho_arquivo, "r") as arquivo:
            tarefas = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        tarefas = []

    # Salvar tarefas no arquivo JSON
    def salvar_tarefas():
        with open(caminho_arquivo, "w") as arquivo:
            json.dump(tarefas, arquivo, indent=4)

    def atualizar_tarefas():
        tarefas_listbox.delete(0, tk.END)
        for tarefa in tarefas:
            status = "✔" if all(m["concluido"]
                                for m in tarefa["missoes"]) else "✘"
            tarefas_listbox.insert(tk.END, f"{status} {tarefa['nome']}")

    def adicionar_tarefa():
        nova_tarefa_nome = tarefa_entry.get()
        if nova_tarefa_nome:
            tarefas.append({"nome": nova_tarefa_nome, "missoes": []})
            salvar_tarefas()
            atualizar_tarefas()
            tarefa_entry.delete(0, tk.END)

    def excluir_tarefa():
        selecionado = tarefas_listbox.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma tarefa para excluir.")
            return

        indice = selecionado[0]
        confirmar = messagebox.askyesno(
            "Confirmação", "Tem certeza que deseja excluir esta tarefa?")
        if confirmar:
            tarefas.pop(indice)
            salvar_tarefas()
            atualizar_tarefas()

    def gerenciar_missoes():
        selecionado = tarefas_listbox.curselection()
        if not selecionado:
            messagebox.showerror(
                "Erro", "Selecione uma tarefa para gerenciar.")
            return

        indice_tarefa = selecionado[0]
        tarefa = tarefas[indice_tarefa]

        missoes_window = tk.Toplevel(checklist_window)
        missoes_window.title(f"Missões - {tarefa['nome']}")
        missoes_window.geometry("400x450")
        missoes_window.resizable(False, False)
        centralizar_janela(missoes_window, 400, 450)

        progresso_label = tk.Label(
            missoes_window, text="", font=("Arial", 10, "bold"))
        progresso_label.pack(pady=5)

        missoes_listbox = tk.Listbox(missoes_window, width=40, height=15)
        missoes_listbox.pack(padx=10, pady=10)

        def atualizar_missoes():
            missoes_listbox.delete(0, tk.END)
            concluido = sum(1 for m in tarefa["missoes"] if m["concluido"])
            total = len(tarefa["missoes"])
            progresso_label.config(
                text=f"Progresso: {concluido}/{total} missões concluídas"
            )

            for missao in tarefa["missoes"]:
                status = "✔" if missao["concluido"] else "✘"
                missoes_listbox.insert(tk.END, f"{status} {missao['nome']}")

            salvar_tarefas()
            atualizar_tarefas()

        def adicionar_missao():
            nova_missao_nome = missao_entry.get()
            if nova_missao_nome:
                tarefa["missoes"].append(
                    {"nome": nova_missao_nome, "concluido": False})
                salvar_tarefas()
                atualizar_missoes()
                missao_entry.delete(0, tk.END)

        def excluir_missao():
            selecionado = missoes_listbox.curselection()
            if not selecionado:
                messagebox.showerror(
                    "Erro", "Selecione uma missão para excluir.")
                return

            indice_missao = selecionado[0]
            confirmar = messagebox.askyesno(
                "Confirmação", "Tem certeza que deseja excluir esta missão?")
            if confirmar:
                tarefa["missoes"].pop(indice_missao)
                salvar_tarefas()
                atualizar_missoes()

        def alternar_status_missao():
            selecionado = missoes_listbox.curselection()
            if not selecionado:
                return
            indice_missao = selecionado[0]
            tarefa["missoes"][indice_missao]["concluido"] = not tarefa["missoes"][indice_missao]["concluido"]
            salvar_tarefas()
            atualizar_missoes()

        missao_entry = tk.Entry(missoes_window, width=30)
        missao_entry.pack(pady=3)
        adicionar_missao_button = tk.Button(
            missoes_window, text="Adicionar Missão", command=adicionar_missao, bg="#4CAF50", fg="white"
        )
        estilizar_botao(adicionar_missao_button,
                        cor_fundo="#4CAF50", largura=15, altura=1)
        adicionar_missao_button.pack(pady=5)

        excluir_missao_button = tk.Button(
            missoes_window, text="Excluir Missão", command=excluir_missao, bg="#f44336", fg="white"
        )
        estilizar_botao(excluir_missao_button,
                        cor_fundo="#f44336", largura=15, altura=1)
        excluir_missao_button.pack(pady=5)

        alternar_status_button = tk.Button(
            missoes_window, text="Marcar/Desmarcar", command=alternar_status_missao, bg="#FFD700", fg="black"
        )
        estilizar_botao(alternar_status_button,
                        cor_fundo="gray", largura=15, altura=1)
        alternar_status_button.pack(pady=5)

        atualizar_missoes()

    # Layout Principal
    header_label = tk.Label(
        checklist_window, text="Checklist de Tarefas", font=("Arial", 16, "bold"))
    header_label.pack(pady=10)

    frame_lista = tk.Frame(checklist_window)
    frame_lista.pack(pady=10, fill="both", expand=True)

    tarefas_listbox = tk.Listbox(frame_lista, width=50, height=15)
    tarefas_listbox.pack(side="left", fill="both", expand=True, padx=10)

    scrollbar = ttk.Scrollbar(
        frame_lista, orient="vertical", command=tarefas_listbox.yview)
    tarefas_listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    frame_acoes = tk.Frame(checklist_window)
    frame_acoes.pack(pady=10)

    tk.Label(frame_acoes, text="Nova Tarefa:").grid(
        row=0, column=0, padx=5, pady=5, sticky="w")
    tarefa_entry = tk.Entry(frame_acoes, width=30)
    tarefa_entry.grid(row=0, column=1, padx=5, pady=5)

    # Aplicando nos botões
    adicionar_button = tk.Button(
        frame_acoes, text="Adicionar", command=adicionar_tarefa)
    adicionar_button["bg"] = "gray"
    adicionar_button["fg"] = "white"
    estilizar_botao(adicionar_button, "gray", largura=15, altura=1)
    adicionar_button.grid(row=0, column=2, padx=5, pady=5)

    excluir_button = tk.Button(
        frame_acoes, text="Excluir", command=excluir_tarefa)
    estilizar_botao(excluir_button, "#f44336", largura=15, altura=1)
    excluir_button.grid(row=1, column=2, padx=5, pady=5)

    gerenciar_missoes_button = tk.Button(
        frame_acoes, text="Gerenciar Missões", command=gerenciar_missoes)
    estilizar_botao(gerenciar_missoes_button, "#808080", largura=15, altura=1)
    gerenciar_missoes_button.grid(row=2, column=0, columnspan=3, pady=10)

    atualizar_tarefas()


def mostrar_informacoes(event):
    selecionado = lista_jogos_listbox.curselection()
    if selecionado:
        indice_selecionado = int(selecionado[0])
        if 0 <= indice_selecionado < len(jogos_filtrados):
            # Obter o jogo diretamente da lista filtrada
            jogo_selecionado = jogos_filtrados[indice_selecionado]

            mensagem = f"Informações do Jogo:\n\nTítulo: {jogo_selecionado['Título']}\nGênero: {jogo_selecionado['Gênero']}\nPlataforma: {jogo_selecionado['Plataforma']}\nData de Zeramento: {jogo_selecionado['Data de Zeramento']}\nForma de Zeramento: {jogo_selecionado['Forma de Zeramento']}\nDescrição de Zeramento: {jogo_selecionado['Descrição de Zeramento']}\nTempo Jogado: {jogo_selecionado['Tempo Jogado']}\nNota: {jogo_selecionado['Nota']}"
            messagebox.showinfo("Informações do Jogo", mensagem)


def copiar_nome():
    # Obtenha o índice do jogo selecionado
    indice_selecionado = lista_jogos_listbox.curselection()[0]
    jogo_selecionado = lista_jogos_listbox.get(indice_selecionado)

    # Use uma expressão regular para encontrar o título do jogo após o número, ponto e emoji
    padrao_titulo = r'\d+\.\s*[^\w\s]+\s*(.+)'
    correspondencia = re.search(padrao_titulo, jogo_selecionado)
    if correspondencia:
        titulo_do_jogo = correspondencia.group(1)
    else:
        titulo_do_jogo = "Título não encontrado"

    # Copie o título do jogo para a área de transferência
    pyperclip.copy(titulo_do_jogo)

def selecionar_wallpaper():
    """Abre um seletor de arquivos para escolher a imagem e inicia a edição."""
    caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
    if caminho_imagem:
        editar_wallpaper(caminho_imagem)


def editar_wallpaper(caminho_imagem):
    """Abre uma janela para recortar o wallpaper antes de salvar."""
    global img_tk, img_editando, canvas, rect_id, img_original
    global x_inicial, y_inicial, desloc_x, desloc_y, redimensionando, largura_recorte, altura_recorte

    # Proporção fixa do recorte
    largura_recorte = 600
    altura_recorte = 400

    # Criar a janela de edição
    janela_edicao = tk.Toplevel(root)
    janela_edicao.title("Editar Wallpaper")
    janela_edicao.geometry("850x650")
    janela_edicao.configure(bg="#2C3E50")
    centralizar_janela(janela_edicao, 850, 650)
    janela_edicao.resizable(False, False)

    # Carregar a imagem e redimensioná-la
    img_original = Image.open(caminho_imagem)
    fator_escala = min(800 / img_original.width, 550 / img_original.height)
    nova_largura = int(img_original.width * fator_escala)
    nova_altura = int(img_original.height * fator_escala)
    img_editando = img_original.resize((nova_largura, nova_altura), Image.LANCZOS)

    # Converter para exibição no Tkinter
    img_tk = ImageTk.PhotoImage(img_editando)

    # Criar o Canvas
    canvas = tk.Canvas(janela_edicao, width=nova_largura, height=nova_altura, bg="#ECF0F1", bd=2, relief="solid")
    canvas.pack(pady=10)

    # Exibir a imagem no Canvas
    canvas.create_image(0, 0, anchor="nw", image=img_tk)

    # Posicionamento inicial do recorte (centralizado)
    x_inicial = (nova_largura - largura_recorte) // 2
    y_inicial = (nova_altura - altura_recorte) // 2
    x_final = x_inicial + largura_recorte
    y_final = y_inicial + altura_recorte

    # Criar o retângulo de recorte já visível
    rect_id = canvas.create_rectangle(x_inicial, y_inicial, x_final, y_final, outline="red", width=2, tags="recorte")

    # Variáveis de controle
    desloc_x, desloc_y = 0, 0
    redimensionando = False

    # Função para iniciar o movimento do recorte
    def iniciar_movimento(event):
        global desloc_x, desloc_y
        desloc_x, desloc_y = event.x, event.y

    # Função para mover o recorte
    def mover_recorte(event):
        global desloc_x, desloc_y
        dx = event.x - desloc_x
        dy = event.y - desloc_y
        desloc_x, desloc_y = event.x, event.y
        canvas.move(rect_id, dx, dy)

    # Função para iniciar o redimensionamento
    def iniciar_redimensionamento(event):
        global desloc_x, desloc_y, redimensionando
        desloc_x, desloc_y = event.x, event.y
        redimensionando = True

    # Função para redimensionar mantendo a proporção
    def redimensionar_recorte(event):
        global largura_recorte, altura_recorte, x_inicial, y_inicial
        if redimensionando:
            nova_largura = max(100, event.x - x_inicial)  # Mínimo de 100 px
            nova_altura = int(nova_largura * (altura_recorte / largura_recorte))  # Mantém a proporção

            x_final = x_inicial + nova_largura
            y_final = y_inicial + nova_altura

            # Atualiza o retângulo mantendo a proporção 600x400
            canvas.coords(rect_id, x_inicial, y_inicial, x_final, y_final)

    # Vincular eventos para mover e redimensionar
    canvas.tag_bind("recorte", "<ButtonPress-1>", iniciar_movimento)
    canvas.tag_bind("recorte", "<B1-Motion>", mover_recorte)
    canvas.bind("<ButtonPress-3>", iniciar_redimensionamento)  # Clique direito para redimensionar
    canvas.bind("<B3-Motion>", redimensionar_recorte)  # Arrastar para redimensionar

    # Função para salvar a imagem recortada
    def salvar_recorte():
        x1, y1, x2, y2 = canvas.coords(rect_id)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        if x2 > x1 and y2 > y1:
            img_crop = img_editando.crop((x1, y1, x2, y2))
            img_crop = img_crop.resize((largura_recorte, altura_recorte))
            salvar_wallpaper(img_crop, largura_recorte, altura_recorte)
        else:
            messagebox.showerror("Erro", "Selecione uma área válida para recorte.")
        
        atualizar_wallpaper()
        carregar_background()
        janela_edicao.destroy()
    # Botão para salvar
    btn_confirmar = tk.Button(janela_edicao, text="Salvar Recorte", command=salvar_recorte, bg="#27AE60", fg="white",
                              font=("Arial", 12, "bold"), padx=10, pady=5, relief="raised", borderwidth=3)
    btn_confirmar.pack(pady=10)

def salvar_wallpaper(imagem, largura, altura):
    """Salva a imagem cortada como wallpaper.png na pasta layout."""
    pasta_layout = "layout"
    os.makedirs(pasta_layout, exist_ok=True)

    caminho_salvar = os.path.join(pasta_layout, "wallpaper.png")
    imagem_redimensionada = imagem.resize((largura, altura))
    imagem_redimensionada.save(caminho_salvar, "PNG")

    messagebox.showinfo("Sucesso!", "Wallpaper atualizado com sucesso!")

    # Atualizar a interface
    atualizar_wallpaper()

def atualizar_wallpaper():
    caminho_wallpaper = os.path.join("layout", "wallpaper.png")
    
    if os.path.exists(caminho_wallpaper):
        img = Image.open(caminho_wallpaper)
        img_tk = ImageTk.PhotoImage(img)

        # Aplicar o wallpaper como fundo
        wallpaper_label.config(image=img_tk)
        wallpaper_label.image = img_tk

def carregar_wallpaper():
    global wallpaper_tk

    caminho_wallpaper = os.path.join("layout", "wallpaper.png")
    
    if os.path.exists(caminho_wallpaper):
        img = Image.open(caminho_wallpaper).convert("RGBA")
        wallpaper_tk = ImageTk.PhotoImage(img)

        # Aplicar o wallpaper como fundo
        wallpaper_label.config(image=wallpaper_tk)
        wallpaper_label.image = wallpaper_tk  # Evita descarte

def carregar_background():
    global background_tk

    caminho_wallpaper = os.path.join("layout", "wallpaper.png")
    caminho_background = os.path.join("layout", "background.png")

    if os.path.exists(caminho_wallpaper) and os.path.exists(caminho_background):
        wallpaper = Image.open(caminho_wallpaper).convert("RGBA")
        background = Image.open(caminho_background).convert("RGBA")

        # Garantir que ambas as imagens tenham o mesmo tamanho
        wallpaper = wallpaper.resize(background.size)

        # Mesclar as imagens (background sobre wallpaper)
        imagem_final = Image.alpha_composite(wallpaper, background)

        # Converter para o formato do Tkinter
        background_tk = ImageTk.PhotoImage(imagem_final)

        # Aplicar ao Label
        background_label.config(image=background_tk)
        background_label.image = background_tk  # Evita descarte