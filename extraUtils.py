import tkinter as tk
from tkinter import messagebox, ttk, font as tkFont
from extraUtils import*
from listHandler import*
from mainUltimate import*
from statisticManager import*
from externalManager import*
from uiHandler import*

def show_error_message(message):
    error_window = tk.Toplevel(root)
    error_window.title("Algo está errado ;-;")
    error_label = tk.Label(error_window, text=message)
    error_label.pack()
    ok_button = tk.Button(error_window, text="OK",
                          command=error_window.destroy)
    ok_button.pack()


def on_closing():
    resposta = messagebox.askyesnocancel(
        "Sair", "Deseja salvar antes de Sair? Os dados não salvos serão perdidos.")
    if resposta is None:
        return
    elif resposta:
        salvar_lista()
    root.destroy()

def criar_aba_resumo():
    resumo_window = tk.Toplevel(root)
    resumo_window.title("Resumo Geral")
    resumo_window.geometry("590x650")
    resumo_window.resizable(False, False)
    centralizar_janela(resumo_window, 590, 650)

    # Filtrar os jogos por estado
    jogos_zerados = [
        jogo for jogo in lista_jogos if jogo.get("Data de Zeramento")]
    jogos_desistidos = [jogo for jogo in lista_jogos if jogo.get(
        "Forma de Zeramento") == "Desistência"]
    jogos_planejados = [jogo for jogo in lista_jogos if jogo.get(
        "Forma de Zeramento") == "Planejo Jogar"]

    # Frame principal com Canvas e Scrollbar
    canvas = tk.Canvas(resumo_window, bg="black", width=780)
    scrollbar = ttk.Scrollbar(
        resumo_window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="black")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Estilo de texto
    header_font = tkFont.Font(family="Arial", size=16, weight="bold")
    text_font = tkFont.Font(family="Arial", size=14)

    # Cabeçalho
    tk.Label(scroll_frame, text="Resumo Geral", font=header_font,
             bg="black", fg="white").pack(pady=10)

    # Total de jogos zerados, desistidos e planejados
    tk.Label(scroll_frame, text=f"Total de Jogos Zerados: {len(jogos_zerados)}",
             font=text_font, bg="black", fg="white").pack(pady=5)
    tk.Label(scroll_frame, text=f"Total de Jogos Desistidos: {len(jogos_desistidos)}",
             font=text_font, bg="black", fg="white").pack(pady=5)
    tk.Label(scroll_frame, text=f"Total de Jogos Planejados: {len(jogos_planejados)}",
             font=text_font, bg="black", fg="white").pack(pady=5)

    # Média de notas
    notas = [float(jogo["Nota"]) for jogo in jogos_zerados if jogo.get("Nota")]
    media_notas = sum(notas) / len(notas) if notas else 0
    tk.Label(
        scroll_frame,
        text=f"Média de Notas dos Jogos Zerados: {media_notas:.2f}",
        font=text_font,
        bg="black",
        fg="white",
    ).pack(pady=5)

    # Resumo por Gêneros
    tk.Label(
        scroll_frame,
        text="Resumo por Gêneros (Jogos e Tempo):",
        font=header_font,
        bg="black",
        fg="white",
    ).pack(pady=10)

    genero_contagem = {}
    for jogo in jogos_zerados:
        genero = jogo.get("Gênero", "Outro")
        genero_contagem[genero] = genero_contagem.get(
            genero, {"quantidade": 0, "tempo": 0})
        genero_contagem[genero]["quantidade"] += 1
        genero_contagem[genero]["tempo"] += calcular_total_minutos(
            jogo.get("Tempo Jogado", "0:00"))

    generos_frame = tk.Frame(scroll_frame, bg="black")
    generos_frame.pack(pady=5, fill="x")

    generos_tree = ttk.Treeview(generos_frame, columns=(
        "Genero", "Quantidade", "Tempo"), show="headings", height=5)
    generos_tree.heading("Genero", text="Gênero")
    generos_tree.heading("Quantidade", text="Quantidade")
    generos_tree.heading("Tempo", text="Tempo Jogado (Horas)")
    generos_tree.column("Genero", width=200, anchor="center")
    generos_tree.column("Quantidade", width=100, anchor="center")
    generos_tree.column("Tempo", width=150, anchor="center")

    for genero, dados in genero_contagem.items():
        horas = dados["tempo"] // 60
        generos_tree.insert("", "end", values=(
            genero, dados["quantidade"], f"{horas}h"))
    generos_tree.pack(side="left", fill="both", expand=True)

    generos_scrollbar = ttk.Scrollbar(
        generos_frame, orient="vertical", command=generos_tree.yview)
    generos_tree.configure(yscrollcommand=generos_scrollbar.set)
    generos_scrollbar.pack(side="right", fill="y")

    # Resumo por Estado e Plataforma
    tk.Label(
        scroll_frame,
        text="Resumo por Estado (Plataformas):",
        font=header_font,
        bg="black",
        fg="white",
    ).pack(pady=10)

    plataforma_resumo = {}
    for jogo in lista_jogos:
        plataforma = jogo["Plataforma"]
        if plataforma not in plataforma_resumo:
            plataforma_resumo[plataforma] = {
                "Planeja Jogar": 0, "Desistidos": 0, "Zerados": 0, "Horas Jogadas": 0}

        estado = jogo["Forma de Zeramento"]
        if estado == "Planejo Jogar":
            plataforma_resumo[plataforma]["Planeja Jogar"] += 1
        elif estado == "Desistência":
            plataforma_resumo[plataforma]["Desistidos"] += 1
        elif estado in ["História", "100%", "Platina"]:
            plataforma_resumo[plataforma]["Zerados"] += 1
            if jogo.get("Tempo Jogado"):
                plataforma_resumo[plataforma]["Horas Jogadas"] += calcular_total_minutos(
                    jogo["Tempo Jogado"]) // 60

    plataformas_frame = tk.Frame(scroll_frame, bg="black")
    plataformas_frame.pack(pady=5, fill="x")

    plataformas_tree = ttk.Treeview(
        plataformas_frame,
        columns=("Plataforma", "Planeja Jogar",
                 "Desistidos", "Zerados", "Horas Jogadas"),
        show="headings",
        height=5
    )
    plataformas_tree.heading("Plataforma", text="Plataforma")
    plataformas_tree.heading("Planeja Jogar", text="Planeja Jogar")
    plataformas_tree.heading("Desistidos", text="Desistidos")
    plataformas_tree.heading("Zerados", text="Zerados")
    plataformas_tree.heading("Horas Jogadas", text="Horas Jogadas (h)")
    plataformas_tree.column("Plataforma", width=150, anchor="center")
    plataformas_tree.column("Planeja Jogar", width=100, anchor="center")
    plataformas_tree.column("Desistidos", width=100, anchor="center")
    plataformas_tree.column("Zerados", width=100, anchor="center")
    plataformas_tree.column("Horas Jogadas", width=120, anchor="center")

    for plataforma, stats in plataforma_resumo.items():
        plataformas_tree.insert("", "end", values=(
            plataforma,
            stats["Planeja Jogar"],
            stats["Desistidos"],
            stats["Zerados"],
            f"{stats['Horas Jogadas']}h"
        ))
    plataformas_tree.pack(side="left", fill="both", expand=True)

    plataformas_scrollbar = ttk.Scrollbar(
        plataformas_frame, orient="vertical", command=plataformas_tree.yview)
    plataformas_tree.configure(yscrollcommand=plataformas_scrollbar.set)
    plataformas_scrollbar.pack(side="right", fill="y")

    # Tempo total jogado
    total_minutos = sum(calcular_total_minutos(
        jogo["Tempo Jogado"]) for jogo in jogos_zerados if jogo.get("Tempo Jogado"))
    total_horas = total_minutos // 60
    total_dias = total_horas // 24
    tk.Label(
        scroll_frame,
        text=f"Tempo Total Jogado: {total_dias} dias, {total_horas % 24} horas",
        font=text_font,
        bg="black",
        fg="white",
    ).pack(pady=10)


def substituir_espaco_por_dois_pontos(event):
    tempo_jogado_entry_var.set(tempo_jogado_entry_var.get().replace(" ", ":"))
