from tkinter import messagebox, filedialog
from tkinter.simpledialog import askinteger
import numpy as np
import json
import datetime
from datetime import datetime
import re
import matplotlib.pyplot as plt
from extraUtils import*
from listHandler import*
from mainUltimate import*
from statisticManager import*
from externalManager import*
from uiHandler import*


def criar_distribuicao_plataformas():
    if not lista_jogos:
        messagebox.showinfo("Informação", "A lista de jogos está vazia.")
        return

    # Filtrar jogos válidos (excluir "Planejo Jogar" e "Desistência")
    jogos_validos = [
        jogo for jogo in lista_jogos
        if jogo.get("Forma de Zeramento") not in ["Planejo Jogar", "Desistência"]
    ]

    # Contagem de jogos por plataforma
    plataforma_contagem = {}
    for jogo in jogos_validos:
        plataforma = jogo["Plataforma"]
        plataforma_contagem[plataforma] = plataforma_contagem.get(
            plataforma, 0) + 1

    if not plataforma_contagem:
        messagebox.showinfo(
            "Informação", "Não há jogos válidos para exibir no gráfico.")
        return

    plataformas = list(plataforma_contagem.keys())
    contagens = list(plataforma_contagem.values())

    # Adicionar os números nos rótulos das plataformas
    labels = [f"{plataforma} ({quantidade})" for plataforma,
              quantidade in zip(plataformas, contagens)]

    # Criar o gráfico de pizza
    plt.figure(figsize=(8, 6))
    plt.pie(contagens, labels=labels, autopct='%1.1f%%',
            startangle=140, colors=plt.cm.Paired.colors)

    # Configurações do gráfico
    plt.title("Jogos Zerados por Plataforma",
              fontsize=14, fontweight='bold')
    plt.axis('equal')  # Garantir que o gráfico seja um círculo
    plt.tight_layout()

    # Exibir o gráfico
    plt.show()


def criar_media_notas_plataformas():
    if not lista_jogos:
        messagebox.showinfo("Informação", "A lista de jogos está vazia.")
        return

    # Filtrar jogos válidos (excluir "Planejo Jogar" e "Desistência")
    jogos_validos = [
        jogo for jogo in lista_jogos
        if jogo.get("Forma de Zeramento") not in ["Planejo Jogar", "Desistência"]
    ]

    if not jogos_validos:
        messagebox.showinfo(
            "Informação", "Não há jogos válidos para calcular a média de notas.")
        return

    # Calcular médias por plataforma
    notas_por_plataforma = {}
    for jogo in jogos_validos:
        plataforma = jogo["Plataforma"]
        nota = float(jogo["Nota"])
        if plataforma not in notas_por_plataforma:
            notas_por_plataforma[plataforma] = []
        notas_por_plataforma[plataforma].append(nota)

    # Calcular a média e preparar os rótulos
    plataformas = list(notas_por_plataforma.keys())
    medias = [sum(notas) / len(notas)
              for notas in notas_por_plataforma.values()]
    labels = [
        f"{plataforma} ({len(notas_por_plataforma[plataforma])})" for plataforma in plataformas]

    # Gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(plataformas, medias, color='skyblue', edgecolor='black')

    # Adicionar valores acima das barras
    for i, media in enumerate(medias):
        plt.text(i, media + 0.1, f"{media:.2f}", ha='center', fontsize=10)

    # Configurações do gráfico
    plt.title("Média de Notas por Plataforma",
              fontsize=14, fontweight='bold')
    plt.xlabel("Plataformas", fontsize=12)
    plt.ylabel("Média das Notas", fontsize=12)
    plt.xticks(range(len(plataformas)), labels, rotation=45, fontsize=10)
    plt.tight_layout()

    # Exibir o gráfico
    plt.show()


def criar_tempo_total_plataformas():
    if not lista_jogos:
        messagebox.showinfo("Informação", "A lista de jogos está vazia.")
        return

    # Filtrar jogos válidos (excluir "Planejo Jogar" e "Desistência")
    jogos_validos = [
        jogo for jogo in lista_jogos
        if jogo.get("Forma de Zeramento") not in ["Planejo Jogar", "Desistência"]
    ]

    if not jogos_validos:
        messagebox.showinfo(
            "Informação", "Não há jogos válidos para calcular o tempo total.")
        return

    # Calcular tempo total por plataforma
    tempo_por_plataforma = {}
    for jogo in jogos_validos:
        plataforma = jogo["Plataforma"]
        tempo_jogado = jogo.get("Tempo Jogado", "").strip()

        # Verificar se o tempo jogado está no formato "HH:MM"
        if re.match(r"^\d{1,2}:\d{2}$", tempo_jogado):
            horas, minutos = map(int, tempo_jogado.split(":"))
            tempo_total = horas * 60 + minutos
            tempo_por_plataforma[plataforma] = tempo_por_plataforma.get(
                plataforma, 0) + tempo_total
        else:
            # Ignorar jogos com tempo inválido
            continue

    if not tempo_por_plataforma:
        messagebox.showinfo(
            "Informação", "Não há tempos válidos para exibir no gráfico.")
        return

    plataformas = list(tempo_por_plataforma.keys())
    # Converter minutos para horas
    tempos_horas = [tempo // 60 for tempo in tempo_por_plataforma.values()]
    labels = [f"{plataforma} ({tempos_horas[i]}h)" for i,
              plataforma in enumerate(plataformas)]

    # Gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(plataformas, tempos_horas, color='lightgreen', edgecolor='black')

    # Adicionar valores acima das barras
    for i, tempo in enumerate(tempos_horas):
        plt.text(i, tempo + 0.1, f"{tempo}h", ha='center', fontsize=10)

    # Configurações do gráfico
    plt.title("Tempo Total de zeramento por Plataforma",
              fontsize=14, fontweight='bold')
    plt.xlabel("Plataformas", fontsize=12)
    plt.ylabel("Tempo Total (Horas)", fontsize=12)
    plt.xticks(range(len(plataformas)), labels, rotation=45, fontsize=10)
    plt.tight_layout()

    # Exibir o gráfico
    plt.show()


def criar_grafico_jogos_por_ano():
    if not lista_jogos:
        messagebox.showinfo("Informação", "A lista de jogos está vazia.")
        return

    jogos_por_ano = {}

    for jogo in lista_jogos:
        try:
            ano = datetime.strptime(jogo["Data de Zeramento"], "%d/%m/%Y").year
            jogos_por_ano[ano] = jogos_por_ano.get(ano, 0) + 1
        except ValueError:
            continue

    anos = sorted(jogos_por_ano.keys())
    contagem = [jogos_por_ano[ano] for ano in anos]

    plt.figure(figsize=(8, 5))
    plt.bar(anos, contagem, color='skyblue')
    plt.xlabel("Ano")
    plt.ylabel("Quantidade de Jogos Zerados")
    plt.title("Jogos Zerados por Ano")
    plt.xticks(anos, rotation=45)
    plt.tight_layout()
    plt.show()


def criar_grafico_comparativo_generos():
    if not lista_jogos:
        messagebox.showinfo("Informação", "A lista de jogos está vazia.")
        return

    # Filtrar apenas os jogos zerados (com Data de Zeramento válida)
    jogos_zerados = [
        jogo for jogo in lista_jogos if jogo.get("Data de Zeramento")]

    # Dicionário para armazenar os dados por ano e gênero
    dados_generos = {}

    for jogo in jogos_zerados:
        try:
            ano = datetime.strptime(jogo["Data de Zeramento"], "%d/%m/%Y").year
            genero = jogo["Gênero"]
            if ano not in dados_generos:
                dados_generos[ano] = {}
            dados_generos[ano][genero] = dados_generos[ano].get(genero, 0) + 1
        except ValueError:
            continue

    # Preparar os dados para o gráfico
    anos = sorted(dados_generos.keys())
    generos = sorted(set(g for dados in dados_generos.values() for g in dados))

    valores = {genero: [dados_generos.get(ano, {}).get(
        genero, 0) for ano in anos] for genero in generos}

    # Plotar o gráfico
    plt.figure(figsize=(10, 6))
    for genero, valores_genero in valores.items():
        plt.plot(anos, valores_genero, marker='o', label=genero)

    # Configurações do gráfico
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel("Quantidade de Jogos Zerados", fontsize=12)
    plt.title("Comparação de Gêneros Zerados por Ano",
              fontsize=14, fontweight="bold")
    plt.xticks(anos, rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(title="Gêneros", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()


def criar_analise_de_notas():
    if not lista_jogos:
        messagebox.showinfo("Informação", "A lista de jogos está vazia.")
        return

    # Filtrar jogos válidos para análise (excluir "Planejo Jogar" e "Desistência")
    jogos_validos = [
        jogo for jogo in lista_jogos
        if jogo.get("Forma de Zeramento") not in ["Planejo Jogar", "Desistência"]
    ]

    # Calcular contagem de jogos por nota
    notas = [int(jogo["Nota"]) for jogo in jogos_validos if jogo["Nota"]]
    if not notas:
        messagebox.showinfo(
            "Informação", "Não há jogos válidos para análise de notas.")
        return

    contagem_notas = {i: notas.count(i) for i in range(1, 11)}

    # Calcular a média das notas
    media_notas = np.mean(notas)

    # Gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(contagem_notas.keys(), contagem_notas.values(),
            color='skyblue', edgecolor='black')

    # Destacar a média das notas
    plt.axhline(y=media_notas, color='red', linestyle='--',
                label=f'Média: {media_notas:.2f}')

    # Configurações do gráfico
    plt.title("Análise de Notas",
              fontsize=14, fontweight='bold')
    plt.xlabel("Notas", fontsize=12)
    plt.ylabel("Quantidade de Jogos", fontsize=12)
    plt.xticks(range(1, 11), fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(loc="upper right", fontsize=10)
    plt.tight_layout()

    # Exibir o gráfico
    plt.show()


def contar_jogos_zerados_por_ano(ano):
    numero_jogos_zerados = 0
    for jogo in lista_jogos:
        data_zeramento_str = jogo["Data de Zeramento"]
        if data_zeramento_str:
            data_zeramento = datetime.strptime(data_zeramento_str, "%d/%m/%Y")
            if data_zeramento.year == ano:
                numero_jogos_zerados += 1
    return numero_jogos_zerados


def calcular_tempo_total_jogado():
    total_minutos = 0

    for jogo in lista_jogos:
        tempo_jogado = jogo.get("Tempo Jogado", "").strip()

        # Validar se o tempo jogado está no formato correto (HH:MM)
        if re.match(r"^\d{1,2}:\d{2}$", tempo_jogado):
            horas, minutos = map(int, tempo_jogado.split(":"))
            total_minutos += horas * 60 + minutos
        else:
            # Ignorar jogos com tempo inválido
            continue

    total_horas = total_minutos // 60
    total_minutos = total_minutos % 60
    total_dias = total_horas // 24
    total_horas = total_horas % 24

    messagebox.showinfo(
        "Tempo Total Jogado", f"Você perdeu {total_dias} dias, {total_horas} horas, {total_minutos} minutos, da sua vida com jogos"
    )


def calcular_total_minutos(tempo_jogado):
    horas, minutos = map(int, tempo_jogado.split(":"))
    return horas * 60 + minutos


def criar_grafico_generos():
    if not lista_jogos:
        messagebox.showinfo("Informação", "A lista de jogos está vazia.")
        return

    genero_contagem = {}

    for jogo in lista_jogos:
        estado = jogo["Forma de Zeramento"]
        # Considerar apenas jogos "completos" ou "desistidos"
        if estado in ["História", "100%", "Platina", "Desistência"]:
            genero = jogo["Gênero"]
            if genero in genero_contagem:
                genero_contagem[genero] += 1
            else:
                genero_contagem[genero] = 1

    if not genero_contagem:
        messagebox.showinfo(
            "Informação", "Não há jogos válidos para exibir no gráfico.")
        return

    # Preparar dados do gráfico
    generos = list(genero_contagem.keys())
    contagem = list(genero_contagem.values())

    # Adicionar números nos rótulos
    labels = [f"{genero} ({quantidade})" for genero,
              quantidade in zip(generos, contagem)]

    # Criar gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(contagem, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Distribuição de Gêneros (Número de Jogos)')
    plt.axis('equal')  # Garantir que o gráfico seja um círculo
    plt.show()


def exibir_numero_jogos_zerados_por_ano():
    try:
        ano = askinteger("Jogos Zerados (Por ano)", "Digite o ano desejado:")
        if ano is not None:
            numero_jogos_zerados = contar_jogos_zerados_por_ano(ano)
            messagebox.showinfo(
                "Número de Jogos Zerados", f"Foram zerados {numero_jogos_zerados} jogos em {ano}.")
    except ValueError:
        messagebox.showerror("Erro", "Ano inválido. Digite um ano válido.")


def mostrar_jogos_longos_curto():
    # Filtrar apenas os jogos zerados com tempo jogado válido
    jogos_zerados = [
        jogo for jogo in lista_jogos
        if jogo.get("Data de Zeramento") and jogo.get("Tempo Jogado")
    ]

    if not jogos_zerados:
        messagebox.showinfo("Informação", "Não há jogos zerados para exibir.")
        return

    try:
        # Ordenar os jogos por tempo jogado
        jogos_zerados.sort(
            key=lambda jogo: calcular_total_minutos(jogo["Tempo Jogado"]))

        # Identificar o mais curto e o mais longo
        jogo_mais_curto = jogos_zerados[0]
        jogo_mais_longo = jogos_zerados[-1]

        # Exibir os resultados
        mensagem = (
            f"Jogo mais curto:\n"
            f"{jogo_mais_curto['Título']} - {jogo_mais_curto['Tempo Jogado']}\n\n"
            f"Jogo mais longo:\n"
            f"{jogo_mais_longo['Título']} - {jogo_mais_longo['Tempo Jogado']}"
        )
        messagebox.showinfo("Jogos mais e Menos longos", mensagem)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


def salvar_em_arquivo():
    nome_arquivo = filedialog.asksaveasfilename(
        defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
    if nome_arquivo:
        with open(nome_arquivo, "w") as arquivo:
            json.dump(lista_jogos, arquivo)
        messagebox.showinfo(
            "Salvar em Arquivo", f"Lista de jogos salva em {nome_arquivo} com sucesso!")


def carregar_de_arquivo():
    nome_arquivo = filedialog.askopenfilename(
        filetypes=[("Arquivos JSON", "*.json")])
    if nome_arquivo:
        try:
            with open(nome_arquivo, "r") as arquivo:
                lista_carregada = json.load(arquivo)
            lista_jogos.extend(lista_carregada)
            atualizar_lista()
            messagebox.showinfo(
                "Carregar de Arquivo", f"Lista de jogos carregada de {nome_arquivo} com sucesso!")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado.")
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Ocorreu um erro ao carregar o arquivo JSON: {e}")