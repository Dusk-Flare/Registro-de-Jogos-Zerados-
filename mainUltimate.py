import tkinter as tk
from tkinter import messagebox, ttk
import os
from PIL import Image, ImageTk
from extraUtils import*
from listHandler import*
from mainUltimate import*
from statisticManager import*
from externalManager import*
from uiHandler import*

# Inicializa a lista de jogos
lista_jogos = carregar_lista()
titulo_entry = None
genero_entry = None
plataforma_entry = None
filtro_window = None
nota_entry = None
janela_edicao = None
jogos_filtrados = lista_jogos.copy()
datetime_value = "algum_valor"


root = tk.Tk()
root.title("Registro ULTIMATE de jogos")


icon_path = os.path.join(os.getcwd(), "layout", "icon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print(f"Ícone não encontrado no caminho: {icon_path}")


root.protocol("WM_DELETE_WINDOW", on_closing)

# Caminho do arquivo na pasta 'layout'
image_path = os.path.join(os.getcwd(), "layout", "Background.png")

try:
    # Criar label para o wallpaper
    wallpaper_label = tk.Label(root)
    wallpaper_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Carregar o background garantindo transparência
    img_background = Image.open(image_path).convert("RGBA")
    background_tk = ImageTk.PhotoImage(img_background)

    # Criar label para o background com transparência
    background_label = tk.Label(root, image=background_tk)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Manter referência da imagem para evitar descarte
    background_label.image = background_tk

except Exception as e:
    messagebox.showerror("Erro", f"Não foi possível carregar o fundo.\nDetalhes: {e}")

# Atualizar as imagens de fundo
atualizar_wallpaper()
carregar_background()

titulo_label = tk.Label(root, text="Título*:")
titulo_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
titulo_entry = tk.Entry(root)
titulo_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

genero_entry = tk.Entry(root)
genero_entry.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

genero_label = tk.Label(root, text="Gênero*:")
genero_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
generos_disponiveis = [
    # RPG
    "RPG", "Action RPG", "RPG de Turno", "RPG Tático", "JRPG", "Action JRPG",
    "JRPG de Turno", "JRPG Tático", "Dungeon Crawler", "MMORPG", "True RPG",

    # Aventura
    "Aventura", "Aventura Gráfica", "Point and Click", "Metroidvania", "Survival Horror",

    # Ação
    "Ação", "Hack and Slash", "Beat 'em Up", "Stealth", "Action-Adventure",

    # Estratégia
    "Estratégia", "RTS (Real-Time Strategy)", "TBS (Turn-Based Strategy)",
    "Tower Defense", "4X (eXplore, eXpand, eXploit, eXterminate)",

    # Simulação
    "Simulação", "Simulação de Vida", "Simulação de Construção", "Simulação de Negócios",
    "Simulação de Voo", "Simulação de Veículos", "Simulação Social",

    # Esportes
    "Esportes", "Futebol", "Basquete", "Corrida", "Golfe", "Tênis", "Esportes Radicais",
    "Automobilismo", "Futebol Americano",

    # Puzzle
    "Puzzle", "Quebra-Cabeças Lógicos", "Match-3", "Jogos de Palavras", "Sokoban", "Escape Room",

    # Luta
    "Luta", "2D Fighting", "3D Fighting", "Arena Fighting", "Party Fighting", "Beat 'em Up",

    # Tiro
    "Tiro", "FPS (First-Person Shooter)", "TPS (Third-Person Shooter)", "Shoot 'em Up",
    "Light Gun Shooter", "Bullet Hell",

    # Horror
    "Horror", "Survival Horror", "Psychological Horror", "Action Horror", "VR Horror",

    # Sandbox
    "Sandbox", "World Builder", "Exploration", "Open World", "Criativo",

    # Party Games
    "Jogos de Festa", "Minigames", "Quiz", "Jogos de Tabuleiro Adaptados",

    # Outros Gêneros
    "Educação", "Treinamento", "Documentário", "Outro"
]
genero_var = tk.StringVar()
genero_combobox = ttk.Combobox(
    root, textvariable=genero_var, values=generos_disponiveis, state="readonly")
genero_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
genero_combobox.set("")
genero_combobox.bind("<KeyRelease>", atualizar_entry)
genero_combobox.bind("<<ComboboxSelected>>", atualizar_genero)

plataformas_disponiveis = [
    # Atari
    "Atari 2600", "Atari 5200", "Atari 7800",

    # Nintendo
    "NES (Nintendo Entertainment System)", "SNES (Super Nintendo Entertainment System)",
    "Nintendo 64", "GameCube", "Game Boy", "Game Boy Color",
    "Game Boy Advance", "Nintendo DS", "Nintendo Switch",

    # Sega
    "Sega Master System", "Sega Genesis (Mega Drive)",
    "Sega Saturn", "Sega Dreamcast", "Game Gear",

    # Sony
    "PlayStation 1", "PlayStation 2", "PlayStation 3",
    "PlayStation 4", "PlayStation 5", "PlayStation Portable",

    # Microsoft
    "Xbox Clássico", "Xbox 360", "Xbox One", "Xbox Series X|S",

    # SNK
    "Neo Geo", "Neo Geo Pocket", "Neo Geo Pocket Color",

    # NEC
    "TurboGrafx-16 (PC Engine)", "TurboGrafx-CD",

    # Mattel
    "Intellivision",

    # Coleco
    "ColecoVision",

    # Commodore
    "Commodore 64", "Amiga",

    # Sinclair
    "ZX Spectrum",

    # Panasonic/GoldStar
    "3DO",

    # Modernos e genéricos
    "PC", "Mobile",

    # Outros
    "Outro"
]

# Campo de entrada e label para plataforma
plataforma_label = tk.Label(root, text="Plataforma*:")
plataforma_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

# Variável para armazenar o valor da plataforma
plataforma_var = tk.StringVar()

# Combobox para plataformas
plataforma_combobox = ttk.Combobox(
    root, textvariable=plataforma_var, values=plataformas_disponiveis, state="readonly"
)
plataforma_combobox.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

# Entrada de texto para personalização
plataforma_entry = tk.Entry(root)
plataforma_entry.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)

# Vincular a ação de seleção do Combobox à função de atualização
plataforma_combobox.bind("<<ComboboxSelected>>", atualizar_plataforma)

data_zeramento_label = tk.Label(root, text="Data de Zeramento:*")
data_zeramento_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
data_zeramento_entry = tk.Entry(root)
data_zeramento_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

data_zeramento_entry.bind("<KeyRelease>", formatar_data_zeramento)
data_zeramento_entry.bind("<Double-Button-1>", atualizar_data_zeramento)

forma_zeramento_label = tk.Label(
    root, text="Forma de Zeramento:*", anchor="w")
forma_zeramento_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
forma_zeramento_var = tk.StringVar()
forma_zeramento_combobox = ttk.Combobox(
    root, textvariable=forma_zeramento_var, values=["História", "100%", "Platina", "Planejo Jogar", "Desistência", "Outro"], state="readonly")
forma_zeramento_combobox.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
forma_zeramento_combobox.bind("<<ComboboxSelected>>", atualizar_campos)
forma_zeramento_combobox.set("")

descricao_zeramento_label = tk.Label(
    root, text="Descrição de Zeramento:")
descricao_zeramento_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
descricao_zeramento_entry = tk.Entry(root)
descricao_zeramento_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

# Modificar apenas o campo de entrada de tempo
tempo_label = tk.Label(root, text="Tempo Jogado (H:M)*:")
tempo_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

tempo_jogado_entry_var = tk.StringVar()
tempo_jogado_entry = tk.Entry(root, textvariable=tempo_jogado_entry_var)
tempo_jogado_entry.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

# Vincular a função ao evento de liberação de tecla
tempo_jogado_entry.bind("<KeyRelease>", formatar_tempo_jogado)

nota_label = tk.Label(root, text="Nota:")
nota_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
nota_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
nota_slider.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)

adicionar_button = tk.Button(
    root, text="Adicionar Jogo", command=adicionar_jogo)
estilizar_botao(adicionar_button, cor_fundo="gray", cor_texto="white",
                largura=15, altura=1, fonte=("Arial", 8, "bold"))
adicionar_button.grid(row=8, column=0, columnspan=2, pady=10)

list_frame = tk.Frame(root)
list_frame.grid(row=0, column=2, rowspan=9, padx=10, pady=5, sticky=tk.N)

lista_jogos_listbox = tk.Listbox(list_frame, width=40, height=15)
lista_jogos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
scrollbar.config(command=lista_jogos_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


lista_jogos_listbox.config(yscrollcommand=scrollbar.set)


lista_jogos_listbox.bind("<Double-Button-1>", mostrar_informacoes)
lista_jogos_listbox.bind("<Button-3>", abrir_menu_contexto)

atualizar_lista()

menu = tk.Menu(root)
root.config(menu=menu)


arquivo_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Arquivo", menu=arquivo_menu)
arquivo_menu.add_command(label="Exportar para PDF", command=exportar_para_pdf)
arquivo_menu.add_command(label="Exportar para Excel",
                         command=exportar_para_excel)
arquivo_menu.add_command(label="Importar de Excel", command=importar_de_excel)
arquivo_menu.add_command(label="Salvar em Arquivo JSON",
                         command=salvar_em_arquivo)
arquivo_menu.add_command(
    label="Carregar de Arquivo JSON", command=carregar_de_arquivo)
arquivo_menu.add_separator()
arquivo_menu.add_command(label="Alterar Wallpaper", command=selecionar_wallpaper)
arquivo_menu.add_separator()
arquivo_menu.add_command(label="Sair", command=on_closing)


editar_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Editar", menu=editar_menu)
editar_menu.add_command(label="Editar Jogo", command=editar_jogo)


filtro_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Filtro", menu=filtro_menu)
filtro_menu.add_command(label="Adicionar Filtro",
                        command=mostrar_jogos_filtrados)
filtro_menu.add_command(label="Limpar Filtros", command=limpar_filtros)

informacoes_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Informações", menu=informacoes_menu)

# Seção: Resumos e análises gerais
informacoes_menu.add_command(
    label="Tempo Total Jogado", command=calcular_tempo_total_jogado)
informacoes_menu.add_command(
    label="Jogos Mais e Menos longos", command=mostrar_jogos_longos_curto)
informacoes_menu.add_command(
    label="Jogos Zerados (Por Ano)", command=exibir_numero_jogos_zerados_por_ano)
informacoes_menu.add_separator()

# Seção: Análise de notas e plataformas
informacoes_menu.add_command(
    label="Análise de Notas", command=criar_analise_de_notas)
informacoes_menu.add_command(
    label="Jogos por Plataforma", command=criar_distribuicao_plataformas)
informacoes_menu.add_command(
    label="Notas Médias (Por Plataforma)", command=criar_media_notas_plataformas)
informacoes_menu.add_command(
    label="Tempo Jogado (Por Plataforma)", command=criar_tempo_total_plataformas)
informacoes_menu.add_separator()

# Seção: Gráficos e comparações
informacoes_menu.add_command(
    label="Gêneros Mais Jogados (Gráfico)", command=criar_grafico_generos)
informacoes_menu.add_command(
    label="Jogos Zerados ao Longo dos Anos", command=criar_grafico_jogos_por_ano)
informacoes_menu.add_command(
    label="Comparação de Gêneros (Anual)", command=criar_grafico_comparativo_generos)

# Outros comandos fora do menu de informações
menu.add_command(label="Minhas Tarefas", command=gerenciar_checklist)
menu.add_command(label="Resumo da sua Jornada", command=criar_aba_resumo)

largura_janela = 600
altura_janela = 400
centralizar_janela(root, largura_janela, altura_janela)

root.configure(bg="#808080")
root.resizable(False, False)
root.mainloop()