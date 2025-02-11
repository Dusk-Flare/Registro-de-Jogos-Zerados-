import tkinter as tk
from tkinter import messagebox
import json
import datetime
from datetime import datetime
import re
import os
from extraUtils import*
from listHandler import*
from mainUltimate import*
from statisticManager import*
from externalManager import*
from uiHandler import*

def carregar_lista():

    caminho_arquivo = os.path.join("saves", "jogos.json")
    try:
        with open(caminho_arquivo, "r") as arquivo:
            lista_jogos = json.load(arquivo)

            # Ordenar apenas jogos com "Data de Zeramento" válida
            jogos_com_data = [
                jogo for jogo in lista_jogos
                if jogo.get("Data de Zeramento") and re.match(r"^\d{2}/\d{2}/\d{4}$", jogo["Data de Zeramento"])
            ]
            jogos_sem_data = [
                jogo for jogo in lista_jogos
                if not jogo.get("Data de Zeramento") or not re.match(r"^\d{2}/\d{2}/\d{4}$", jogo["Data de Zeramento"])
            ]

            jogos_com_data = sorted(
                jogos_com_data,
                key=lambda jogo: datetime.strptime(
                    jogo["Data de Zeramento"], "%d/%m/%Y")
            )

            # Reunir jogos com e sem data, mantendo os sem data no final
            return jogos_com_data + jogos_sem_data

    except FileNotFoundError:
        return []
    except json.decoder.JSONDecodeError:
        return []


def validar_campos(titulo, genero, plataforma, data_zeramento, tempo_jogado, nota, estado):
    # Validação do campo 'Título'
    if not titulo.strip():
        return "O campo 'Título' é obrigatório! Não deixe seu jogo sem nome."

    # Validação do campo 'Gênero'
    if not genero.strip():
        return "O campo 'Gênero' é obrigatório! Escolha o tipo do seu jogo."

    # Validação do campo 'Plataforma'
    if not plataforma.strip():
        return "O campo 'Plataforma' é obrigatório! Onde você jogou?"

    # Validação do campo 'Forma de Zeramento'
    if not estado.strip():
        return "O campo 'Forma de Zeramento' é obrigatório! Você zerou? Se sim, como?"

    # Validação adicional para estados específicos
    if estado not in ["Planejo Jogar", "Desistência"]:
        # Validação do campo 'Data de Zeramento'
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', data_zeramento):
            return "A data de zeramento deve estar no formato DIA/MÊS/ANO."
        try:
            datetime.strptime(data_zeramento, "%d/%m/%Y")
        except ValueError:
            return "A data de zeramento não é válida!"

        # Validação do campo 'Tempo Jogado'
        if not re.match(r'^\d{1,2}:\d{2}$', tempo_jogado):
            return "O tempo jogado deve estar no formato HORAS:MINUTOS!"
        try:
            horas, minutos = map(int, tempo_jogado.split(":"))
            if horas < 0 or minutos < 0 or minutos >= 60:
                return "O tempo jogado é inválido! Certifique-se de que está no formato correto."
        except ValueError:
            return "O tempo jogado é inválido! Tente novamente."

    # Validação do campo 'Nota'
    if not (1 <= nota <= 10):
        return "A nota deve estar entre 1 e 10!"

    # Tudo está válido
    return None


def organizar_lista(metodo):
    global lista_jogos

    # Separar jogos zerados e não zerados
    jogos_zerados = [jogo for jogo in lista_jogos if jogo.get("Data de Zeramento")]
    jogos_nao_zerados = [jogo for jogo in lista_jogos if not jogo.get("Data de Zeramento")]

    if metodo == "Data de Zeramento":
        jogos_zerados.sort(key=lambda jogo: datetime.strptime(jogo["Data de Zeramento"], "%d/%m/%Y"))
    elif metodo == "Data de Lançamento (Antigo -> Novo)":
        lista_jogos.sort(key=lambda jogo: datetime.strptime(jogo.get("Data de Lançamento", "01/01/3000"), "%d/%m/%Y"))
    elif metodo == "Data de Lançamento (Novo -> Antigo)":
        lista_jogos.sort(key=lambda jogo: datetime.strptime(jogo.get("Data de Lançamento", "01/01/1900"), "%d/%m/%Y"), reverse=True)
    elif metodo == "Ordem Alfabética":
        jogos_zerados.sort(key=lambda jogo: jogo["Título"].lower())
        jogos_nao_zerados.sort(key=lambda jogo: jogo["Título"].lower())
    elif metodo == "Tempo Jogado":
        jogos_zerados.sort(
            key=lambda jogo: int(jogo.get("Tempo Jogado", "0:00").split(":")[0]) * 60 + int(jogo.get("Tempo Jogado", "0:00").split(":")[1]),
            reverse=True
        )
    elif metodo == "Nota":
        jogos_zerados.sort(key=lambda jogo: float(jogo.get("Nota", 0)), reverse=True)
    elif metodo == "Plataforma":
        jogos_zerados.sort(key=lambda jogo: (jogo["Plataforma"].lower(), jogo["Título"].lower()))
        jogos_nao_zerados.sort(key=lambda jogo: (jogo["Plataforma"].lower(), jogo["Título"].lower()))

    # Unindo novamente os jogos zerados e não zerados, mantendo os não zerados no final
    lista_jogos = jogos_zerados + jogos_nao_zerados

    atualizar_lista(lista_jogos)

def abrir_menu_organizacao():
    janela_organizacao = tk.Toplevel(root)
    janela_organizacao.title("Organizar Jogos")
    janela_organizacao.resizable(False, False)
    janela_organizacao.geometry("300x270")
    centralizar_janela(janela_organizacao, 300, 270)
    
    tk.Label(janela_organizacao, text="Escolha o método de organização:", font=("Arial", 10, "bold")).pack(pady=10)
    
    metodos = ["Data de Zeramento", "Ordem Alfabética", "Tempo Jogado", "Nota", "Plataforma"]
    for metodo in metodos:
        tk.Button(janela_organizacao, text=metodo, command=lambda m=metodo: [organizar_lista(m), janela_organizacao.destroy()]).pack(pady=5)


def atualizar_entry(event):
    genero_entry.delete(0, tk.END)
    texto_digitado = genero_combobox.get()
    genero_entry.insert(0, texto_digitado)


def limpar_filtros():
    global jogos_filtrados
    jogos_filtrados = lista_jogos.copy()
    atualizar_lista(jogos_filtrados)
    if filtro_window:
        filtro_window.destroy()


def limpar_campos():
    global nota_entry, titulo_entry, genero_entry, plataforma_entry, data_zeramento_entry, descricao_zeramento_entry, tempo_jogado_entry

    if nota_entry:
        nota_entry.delete(0, tk.END)
    if titulo_entry:
        titulo_entry.delete(0, tk.END)
    if genero_entry:
        genero_entry.delete(0, tk.END)
    if plataforma_entry:
        plataforma_entry.delete(0, tk.END)
    if data_zeramento_entry:
        data_zeramento_entry.delete(0, tk.END)
    if descricao_zeramento_entry:
        descricao_zeramento_entry.delete(0, tk.END)
    if tempo_jogado_entry:
        tempo_jogado_entry.delete(0, tk.END)

    # Limpar as combobox
    genero_combobox.set('')
    plataforma_combobox.set('')
    forma_zeramento_combobox.set('')


def formatar_tempo_jogado(event):
    texto = tempo_jogado_entry.get()
    # Remove caracteres não numéricos
    texto = ''.join(filter(str.isdigit, texto))

    # Formatação automática
    if len(texto) > 2:
        texto = texto[:2] + ":" + texto[2:]

    # Limitar a dois dígitos para horas e minutos
    if len(texto) > 5:
        texto = texto[:5]

    tempo_jogado_entry.delete(0, tk.END)
    tempo_jogado_entry.insert(0, texto)


def formatar_data(entry):
    input_text = entry.get()

    input_text = ''.join(filter(str.isdigit, input_text))

    if len(input_text) >= 2:
        formatted_text = input_text[:2]
        if len(input_text) >= 4:
            formatted_text += '/' + input_text[2:4]
            if len(input_text) >= 8:
                formatted_text += '/' + input_text[4:8]
        entry.delete(0, tk.END)
        entry.insert(0, formatted_text)


def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela - largura) // 2
    y = (altura_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def formatar_data_zeramento(event):
    input_text = data_zeramento_entry.get()

    # Remover todos os caracteres que não sejam dígitos ou parênteses
    formatted_text = re.sub(r'[^0-9()]', '', input_text)

    # Limitar o ano a 4 dígitos
    if '/' in formatted_text:
        parts = formatted_text.split('/')
        if len(parts) > 2:
            parts[2] = parts[2][:4]
            formatted_text = '/'.join(parts)

    # Recriar a entrada formatada, adicionando barras automaticamente
    if len(formatted_text) >= 2 and formatted_text[1] != '/':
        formatted_text = formatted_text[:2] + '/' + formatted_text[2:]
    if len(formatted_text) >= 5 and formatted_text[4] != '/':
        formatted_text = formatted_text[:5] + '/' + formatted_text[5:]

    # Limitar o ano a 4 dígitos
    if '/' in formatted_text:
        parts = formatted_text.split('/')
        if len(parts) > 2:
            parts[2] = parts[2][:4]
            formatted_text = '/'.join(parts)

    data_zeramento_entry.delete(0, tk.END)
    data_zeramento_entry.insert(0, formatted_text)


def is_valid_nota(nota):
    try:
        nota = float(nota)
        return 1 <= nota <= 10
    except ValueError:
        return False


def atualizar_data_zeramento(event):
    data_atual = datetime.now().strftime("%d/%m/%Y")
    data_zeramento_entry.delete(0, tk.END)
    data_zeramento_entry.insert(0, data_atual)
    formatar_data_zeramento(data_atual)


def excluir_jogo():
    selecionado = lista_jogos_listbox.curselection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um jogo para excluir.")
        return

    indice = int(selecionado[0])

    if 0 <= indice < len(lista_jogos):
        # Confirmar exclusão
        jogo_a_excluir = lista_jogos[indice]
        confirmar = messagebox.askyesno(
            "Confirmação", f"Tem certeza que deseja excluir o jogo '{jogo_a_excluir['Título']}'?"
        )

        if confirmar:
            jogo_excluido = lista_jogos.pop(indice)
            atualizar_lista()
            messagebox.showinfo(
                "Sucesso", f"Jogo '{jogo_excluido['Título']}' excluído com sucesso!")
            if janela_edicao:
                janela_edicao.destroy()


def adicionar_jogo():
    # Capturar os valores dos campos
    titulo = titulo_entry.get()
    genero = genero_entry.get()
    plataforma = plataforma_entry.get()
    data_zeramento = data_zeramento_entry.get()
    tempo_jogado = tempo_jogado_entry.get()
    nota = nota_slider.get()
    estado = forma_zeramento_combobox.get()

    # Validar os campos
    mensagem_erro = validar_campos(
        titulo, genero, plataforma, data_zeramento, tempo_jogado, nota, estado)
    if mensagem_erro:
        show_error_message(mensagem_erro)
        return

    # Criar o novo jogo
    novo_jogo = {
        "Título": titulo,
        "Gênero": genero,
        "Plataforma": plataforma,
        "Data de Zeramento": data_zeramento if estado not in ["Planejo Jogar", "Desistência"] else "",
        "Forma de Zeramento": estado,
        "Descrição de Zeramento": descricao_zeramento_entry.get(),
        "Tempo Jogado": tempo_jogado if estado not in ["Planejo Jogar", "Desistência"] else "",
        "Nota": nota,
    }

    # Adicionar o jogo à lista
    lista_jogos.append(novo_jogo)
    atualizar_lista()
    limpar_filtros()
    limpar_campos()

    # Mensagem de sucesso
    messagebox.showinfo(
        "Sucesso!", f"O jogo '{titulo}' foi adicionado com sucesso!")


def atualizar_campos(event):
    estado = forma_zeramento_combobox.get()
    if estado in ["Planejo Jogar", "Desistência"]:
        # Desativar campos
        tempo_jogado_entry_var.set("")  # Use set() para limpar o campo
        tempo_jogado_entry.config(state="disabled")
        nota_slider.set(1)
        nota_slider.config(state="disabled")
        data_zeramento_entry.delete(0, tk.END)
        data_zeramento_entry.config(state="disabled")
    else:
        # Reativar campos
        tempo_jogado_entry.config(state="normal")
        nota_slider.config(state="normal")
        data_zeramento_entry.config(state="normal")


def atualizar_genero(event):
    genero_entry.delete(0, tk.END)
    genero_selecionado = genero_combobox.get()
    genero_entry.insert(0, genero_selecionado)


def atualizar_plataforma(event):
    plataforma_entry.delete(0, tk.END)
    plataforma_entry.insert(0, plataforma_var.get())


def validar_numero(P):
    # Esta função permite entrada numérica e espaços
    if P == "" or re.match("^[0-9\s]*$", P):
        return True
    else:
        return False


def atualizar_lista(jogos=None):
    if jogos is None:
        jogos = lista_jogos
    lista_jogos_listbox.delete(0, tk.END)
    for idx, jogo in enumerate(jogos, start=1):
        estado = jogo["Forma de Zeramento"]
        if estado == "História":
            icone = "✅"
        elif estado == "Planejo Jogar":
            icone = "📅"
        elif estado == "Desistência":
            icone = "❌"
        else:
            icone = "✅"
        lista_jogos_listbox.insert(tk.END, f"{idx}. {icone} {jogo['Título']}")