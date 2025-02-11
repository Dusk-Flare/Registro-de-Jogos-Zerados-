from tkinter import messagebox, filedialog
import pandas as pd
import json
import openpyxl
from openpyxl.styles import NamedStyle, Alignment
from openpyxl.utils import get_column_letter
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from extraUtils import*
from listHandler import*
from mainUltimate import*
from statisticManager import*
from externalManager import*
from uiHandler import*

def exportar_para_pdf():
    if not lista_jogos:
        messagebox.showerror(
            "Erro", "A lista de jogos está vazia. Não há nada para exportar.")
        return

    nome_arquivo = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
    if nome_arquivo:
        # Criar um documento PDF
        doc = SimpleDocTemplate(nome_arquivo, pagesize=landscape(letter))
        elements = []

        # Calcular a largura da página e margens
        width, height = landscape(letter)
        margin = 0.5 * inch  # Margem de 0,5 polegadas nas laterais

        # Calcular a largura efetiva da tabela
        effective_width = width - 2 * margin

        # Criar uma tabela para os dados da lista de jogos
        data = [["Título", "Gênero", "Plataforma", "Data de Zeramento",
                 "Forma de Zeramento", "Descrição de Zeramento", "Tempo Jogado", "Nota"]]
        for jogo in lista_jogos:
            # Remover a nota para "Planejo Jogar" e "Desistência"
            nota = "" if jogo["Forma de Zeramento"] in [
                "Planejo Jogar", "Desistência"] else str(jogo["Nota"])
            data.append([str(jogo["Título"]), str(jogo["Gênero"]), str(jogo["Plataforma"]), str(jogo["Data de Zeramento"]),
                         str(jogo["Forma de Zeramento"]), str(jogo["Descrição de Zeramento"]), str(jogo["Tempo Jogado"]), nota])

        # Calcular a largura das colunas com base no conteúdo, limitando a um valor máximo
        max_col_width = effective_width / len(data[0])
        colWidths = [min(max(len(data[i][j]) * 7, max_col_width)
                         for i in range(len(data))) for j in range(len(data[0]))]

        # Definir um estilo de parágrafo para o conteúdo da célula
        styles = getSampleStyleSheet()
        cell_style = ParagraphStyle(name='TableCell')
        cell_style.alignment = 1  # Centralizar o texto na célula
        cell_style.leading = 12  # Espaçamento entre linhas

        # Adicionar a tabela de dados com cores por estado
        table_data = []
        for i, row in enumerate(data):
            table_row = []
            for cell_content in row:
                # Criar um parágrafo com o estilo da célula
                cell_paragraph = Paragraph(cell_content, cell_style)
                table_row.append(cell_paragraph)
            table_data.append(table_row)

        # Criar a tabela e definir o estilo
        table = Table(table_data, colWidths=colWidths)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Cabeçalho
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centralizar verticalmente
        ])

        # Adicionar cores específicas por estado
        for i in range(1, len(data)):
            estado = data[i][4]  # Índice da coluna "Forma de Zeramento"
            if estado == "Planejo Jogar":
                style.add('BACKGROUND', (0, i), (-1, i),
                          colors.beige)  # Cor bege
            elif estado == "Desistência":
                style.add('BACKGROUND', (0, i), (-1, i),
                          colors.lightcoral)  # Cor vermelho claro
            else:
                style.add('BACKGROUND', (0, i), (-1, i),
                          colors.white)  # Cor branca padrão

        # Aplicar estilo à tabela
        table.setStyle(style)

        # Adicionar a tabela ao elemento PDF
        elements.append(Spacer(1, 0.25 * inch))  # Espaço antes da tabela
        elements.append(table)
        elements.append(Spacer(1, 0.25 * inch))  # Espaço após a tabela

        # Construir o PDF
        doc.build(elements)

        messagebox.showinfo(
            "Sucesso", f"Lista de jogos exportada para {nome_arquivo} (PDF) com sucesso!")


def exportar_para_excel():
    if not lista_jogos:
        messagebox.showerror(
            "Erro", "A lista de jogos está vazia. Não há nada para exportar.")
        return

    # Criar um novo arquivo Excel e uma nova planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lista de Jogos"

    # Definir estilos para o cabeçalho
    header_style = NamedStyle(name="header_style")
    header_style.font = openpyxl.styles.Font(bold=True, color="FFFFFF")
    header_style.fill = openpyxl.styles.PatternFill(
        start_color="333333", end_color="333333", fill_type="solid")
    header_style.alignment = Alignment(horizontal="center")  # Centralizar
    for col_num, column_title in enumerate(["Título", "Gênero", "Plataforma", "Data de Zeramento",
                                            "Forma de Zeramento", "Descrição de Zeramento", "Tempo Jogado", "Nota"], 1):
        cell = ws.cell(row=1, column=col_num, value=column_title)
        # Atribuir diretamente o estilo ao cabeçalho
        cell.style = header_style

    # Definir estilos de cores para "Planejo Jogar" e "Desistência"
    estilo_planejo = openpyxl.styles.PatternFill(
        start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")  # Bege
    estilo_desistencia = openpyxl.styles.PatternFill(
        start_color="F4CCCC", end_color="F4CCCC", fill_type="solid")  # Vermelho claro

    # Preencher os dados
    for row_num, jogo in enumerate(lista_jogos, start=2):
        for col_num, (chave, valor) in enumerate(jogo.items(), start=1):
            # Ajustar a nota para "Planejo Jogar" e "Desistência"
            if chave == "Nota" and jogo["Forma de Zeramento"] in ["Planejo Jogar", "Desistência"]:
                valor = ""
            cell = ws.cell(row=row_num, column=col_num, value=valor)

            # Aplicar cores conforme o estado do jogo
            if jogo["Forma de Zeramento"] == "Planejo Jogar":
                cell.fill = estilo_planejo
            elif jogo["Forma de Zeramento"] == "Desistência":
                cell.fill = estilo_desistencia

    # Ajustar largura das colunas
    for col in ws.columns:
        max_length = 0
        column = get_column_letter(col[0].column)
        for cell in col:
            try:
                if cell.value and len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width
        for cell in col:
            cell.alignment = Alignment(horizontal="center")

    # Salvar o arquivo Excel
    nome_arquivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
    if nome_arquivo:
        wb.save(nome_arquivo)
        messagebox.showinfo(
            "Sucesso", f"Lista de jogos exportada para {nome_arquivo} com sucesso!")


def importar_de_excel():
    nome_arquivo = filedialog.askopenfilename(
        filetypes=[("Arquivos Excel", "*.xlsx")])
    if not nome_arquivo:
        return  # Cancelamento do diálogo

    try:
        # Ler o arquivo Excel em um DataFrame
        df = pd.read_excel(nome_arquivo)

        # Verificar se as colunas necessárias estão presentes
        colunas_esperadas = ["Título", "Gênero", "Plataforma", "Data de Zeramento",
                             "Forma de Zeramento", "Descrição de Zeramento", "Tempo Jogado", "Nota"]
        for coluna in colunas_esperadas:
            if coluna not in df.columns:
                messagebox.showerror(
                    "Erro", f"A coluna '{coluna}' está ausente no arquivo Excel.")
                return

        # Substituir valores NaN por strings vazias
        df = df.fillna("")

        # Converter o DataFrame em uma lista de dicionários
        lista_importada = df.to_dict(orient='records')

        # Criar um conjunto de identificadores únicos (título + plataforma + estado)
        jogos_existentes = {
            (jogo["Título"].strip().lower(), jogo["Plataforma"].strip(
            ).lower(), jogo["Forma de Zeramento"].strip().lower())
            for jogo in lista_jogos
        }

        # Adicionar todos os jogos (incluindo validação de campos obrigatórios)
        jogos_adicionados = 0
        for jogo in lista_importada:
            # Criar um identificador único para o jogo
            identificador = (
                jogo["Título"].strip().lower(),
                jogo["Plataforma"].strip().lower(),
                jogo["Forma de Zeramento"].strip().lower()
            )

            # Verificar título vazio ou inválido
            if not jogo["Título"].strip():
                print(f"Jogo ignorado por título vazio: {jogo}")
                continue  # Ignorar jogos sem título

            # Verificar se o jogo já existe na lista
            if identificador in jogos_existentes:
                print(f"Jogo ignorado por ser duplicado: {jogo}")
                continue

            # Validar e formatar a nota
            try:
                nota = float(jogo["Nota"])
                if 1 <= nota <= 10:
                    jogo["Nota"] = nota
                else:
                    jogo["Nota"] = ""  # Nota inválida
            except (ValueError, TypeError):
                jogo["Nota"] = ""  # Nota ausente ou inválida

            # Adicionar o jogo à lista
            lista_jogos.append(jogo)
            # Atualizar o conjunto de identificadores
            jogos_existentes.add(identificador)
            jogos_adicionados += 1

        # Atualizar a lista exibida
        atualizar_lista()
        limpar_filtros()

        # Mensagem de sucesso
        if jogos_adicionados > 0:
            messagebox.showinfo(
                "Sucesso", f"{jogos_adicionados} jogos foram importados de {nome_arquivo} com sucesso!"
            )
        else:
            messagebox.showinfo(
                "Informação", "Nenhum novo jogo foi importado. Todos os jogos já existem na lista."
            )

    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado.")
    except ValueError as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo Excel: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")


def salvar_lista():
    os.makedirs("saves", exist_ok=True)
    caminho_arquivo = os.path.join("saves", "jogos.json")
    with open(caminho_arquivo, "w") as arquivo:
        json.dump(lista_jogos, arquivo)
    messagebox.showinfo("Salvar", "Lista de jogos salva com sucesso!")