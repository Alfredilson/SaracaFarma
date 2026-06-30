import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import ttk
import sqlite3
from admin import abrir_funcoes_admin
from produto import cadastrar_produto
from produto import cadastrar_produtos_treeview 
#---from produto import cadastrar_produtos_csv
from produto import cadastrar_produtos_fornecedor
from tkinter import filedialog
from controle_estoque import tela_estoque, tela_relatorio
import datetime

def cadastrar_lista_produtos():
    # Função placeholder para cadastro em lote
    arquivo = filedialog.askopenfilename(title="Selecionar arquivo de produtos", filetypes=[("CSV", "*.csv"), ("Todos", "*")])
    if arquivo:
        messagebox.showinfo("Cadastro em Lote", f"Arquivo selecionado: {arquivo}\nFuncionalidade ainda não implementada.")

def tela_principal(perfil):
    principal = tk.Tk()
    principal.title("SaracaFarma - Tela Principal")
    principal.geometry("600x400")
    principal.configure(bg="#cce6ff")

     # Faz a janela abrir maximizada
    principal.state("zoomed")   # no Windows
    # ou, se quiser ocupar toda a tela em qualquer sistema:
    # principal.attributes("-fullscreen", True)
       

    # Criar barra de menu
    menubar = tk.Menu(principal)

      # Menu Cadastro
    menu_cadastro = tk.Menu(menubar, tearoff=0)
    #Chamada direta da função de cadastro de produto.
    menu_cadastro.add_command(label="Cadastro Individual", command=lambda: cadastrar_produto(perfil))
    menu_cadastro.add_command(label="Cadastro em Lote (Treeview)", command=lambda: cadastrar_produtos_treeview(perfil))
    #---menu_cadastro.add_command(label="Cadastro em Lote (CSV)", command=lambda: cadastrar_produtos_csv(perfil))
    menu_cadastro.add_command(label="Cadastro em Lote via Fornecedor", command=lambda: cadastrar_produtos_fornecedor(perfil))


    menubar.add_cascade(label="Cadastro", menu=menu_cadastro)

     # Menu Estoque
    menu_estoque = tk.Menu(menubar, tearoff=0)
    menu_estoque.add_command(label="Controle de Estoque", command=lambda: tela_estoque(perfil)) # Placeholder para função de relatório
    menu_estoque.add_command(label="Controlar Relatorio", command=tela_relatorio) # Placeholder para função de relatório
    menu_estoque.add_command(label="Consultar Saldo",)
    menubar.add_cascade(label="Estoque", menu=menu_estoque)

    # Menu Administração (somente se perfil for admin)
    if perfil == "admin":
        menu_admin = tk.Menu(menubar, tearoff=0)
        menu_admin.add_command(label="Funções Administrativas", command=abrir_funcoes_admin)
        menubar.add_cascade(label="Administração", menu=menu_admin)
    
       # Menu Sair
    menu_sair = tk.Menu(menubar, tearoff=0)
    menu_sair.add_command(label="Encerrar", command=principal.quit)
    menubar.add_cascade(label="Sair", menu=menu_sair)

    barra = tk.Frame(principal, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Tela Principal - SaracaFarma", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(principal, bg="#cce6ff")
    frame.pack(pady=30)

    
    # Associar menu à janela
    principal.config(menu=menubar)


    style = ttk.Style()
    style.theme_use("default")

    # Estilo da Treeview (linhas)
    style.configure("Treeview",
        background="#e6f2ff",       # azul claro para fundo das linhas
        foreground="black",
        rowheight=25,
        fieldbackground="#e6f2ff"
    )

    style.map("Treeview",
        background=[("selected", "#3399ff")],
        foreground=[("selected", "white")]
    )

    # Estilo do cabeçalho (descrição das colunas)
    style.configure("Treeview.Heading",
        background="#0066cc",   # azul forte
        foreground="silver",    # texto em tom prata
        font=("Segoe UI", 11, "bold")
)


    
      # Frame de vendas
    frame_vendas = tk.Frame(principal, bg="#cce6ff")
    frame_vendas.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(frame_vendas, text="Vendas", font=("Segoe UI", 16, "bold"), bg="#cce6ff").pack(pady=10)

    # Treeview de itens da venda
    colunas = ("codigo_barras", "nome", "dosagem", "lote", "quantidade", "preco_unitario", "subtotal")

    nomes_colunas = {
       "codigo_barras": "CÓDIGO DE BARRAS",
       "nome": "NOME",
       "dosagem": "DOSAGEM",
       "lote": "LOTE",
       "quantidade": "QUANTIDADE",
       "preco_unitario": "PREÇO UNITÁRIO",
       "subtotal": "SUBTOTAL"
   }
    tree_venda = ttk.Treeview(frame_vendas, columns=colunas, show="headings")
    tree_venda.column("codigo_barras", anchor="center", width=150)
    tree_venda.column("nome", anchor="center", width=200)
    tree_venda.column("dosagem", anchor="center", width=120)
    tree_venda.column("lote", anchor="center", width=100)
    tree_venda.column("quantidade", anchor="center", width=100)
    tree_venda.column("preco_unitario", anchor="center", width=120)
    tree_venda.column("subtotal", anchor="center", width=120)

    for col in colunas:
        tree_venda.heading(col, text=nomes_colunas[col])
    tree_venda.pack(fill="both", expand=True)

    # Botões de ação
    botoes = tk.Frame(frame_vendas, bg="#cce6ff")
    botoes.pack(pady=10)

    tk.Button(botoes, text="Adicionar Item",
          bg="#4CAF50",        # verde
          fg="white",          # texto branco
          activebackground="#45a049",  # cor ao clicar
          activeforeground="white",
          command=lambda: adicionar_item(tree_venda)).grid(row=0, column=0, padx=5)

    tk.Button(botoes, text="Remover Item",
          bg="#f44336",        # vermelho
          fg="white",
          activebackground="#d32f2f",
          activeforeground="white",
          command=lambda: remover_item(tree_venda)).grid(row=0, column=1, padx=5)

    tk.Button(botoes, text="Finalizar Venda",
          bg="#0066cc",        # azul
          fg="white",
          activebackground="#004c99",
          activeforeground="white",
          command=lambda: finalizar_venda(tree_venda, perfil)).grid(row=0, column=2, padx=5)



    principal.mainloop()

def verificar_admin():

    janela = tk.Toplevel()
    janela.title("Verificação Admin")
    janela.geometry("300x200")
    janela.configure(bg="#cce6ff")

    tk.Label(janela, text="Login Admin:", bg="#cce6ff").pack(pady=5)
    entry_login = ttk.Entry(janela, width=25)
    entry_login.pack(pady=5)

    tk.Label(janela, text="Senha:", bg="#cce6ff").pack(pady=5)
    entry_senha = ttk.Entry(janela, width=25, show="*")
    entry_senha.pack(pady=5)

    def validar_admin():
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE login=? AND senha=? AND perfil='admin'", 
                       (entry_login.get(), entry_senha.get()))
        result = cursor.fetchone()
        conn.close()
        if result:
            messagebox.showinfo("Sucesso", "Acesso administrativo liberado!")
            abrir_funcoes_admin()
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Login ou senha inválidos.")

    ttk.Button(janela, text="Entrar", command=validar_admin).pack(pady=10)

def adicionar_item(tree_venda):
    janela = tk.Toplevel()
    janela.title("Adicionar Item")
    janela.geometry("400x500")
    janela.configure(bg="#cce6ff")

    tk.Label(janela, text="Digite Nome ou Código:", bg="#cce6ff").pack(pady=5)
    entry_busca = ttk.Entry(janela, width=40)
    entry_busca.pack(pady=5)

    #Permitir busca aotomatica ao precionar enter (leitor codigo de barras)
    entry_busca.bind("<Return>", lambda event: buscar_produto())

    # Lista de sugestões
    lista_sugestoes = tk.Listbox(janela, width=40, height=5)
    lista_sugestoes.pack(pady=5)

    def atualizar_sugestoes(event):
        termo = entry_busca.get()
        lista_sugestoes.delete(0, tk.END)

        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, codigo_barras FROM Produto WHERE nome LIKE ? OR codigo_barras LIKE ?", 
                       (f"%{termo}%", f"%{termo}%"))
        resultados = cursor.fetchall()
        conn.close()

        for nome, codigo in resultados:
            lista_sugestoes.insert(tk.END, f"{nome} - {codigo}")

    entry_busca.bind("<KeyRelease>", atualizar_sugestoes)

    # Função para selecionar sugestão da lista
    def selecionar_sugestao(event):
        selecao = lista_sugestoes.get(lista_sugestoes.curselection())
        termo = selecao.split(" - ")[1]  # pega o código de barras
        entry_busca.delete(0, tk.END)
        entry_busca.insert(0, termo)
        lista_sugestoes.delete(0, tk.END)  # limpa a lista
        buscar_produto()

    lista_sugestoes.bind("<<ListboxSelect>>", selecionar_sugestao)

    # Campos de exibição
    entry_codigo = ttk.Entry(janela, width=40)
    entry_nome = ttk.Entry(janela, width=40)
    entry_dosagem = ttk.Entry(janela, width=40)
    entry_lote = ttk.Entry(janela, width=40)
    entry_preco = ttk.Entry(janela, width=40)
    entry_qtd_estoque = ttk.Entry(janela, width=40)

    for campo in [entry_codigo, entry_nome, entry_dosagem, entry_lote, entry_preco, entry_qtd_estoque]:
        campo.pack(pady=3)

    tk.Label(janela, text="Quantidade a vender:", bg="#cce6ff").pack(pady=5)
    entry_quantidade_venda = ttk.Entry(janela, width=40)
    entry_quantidade_venda.pack(pady=5)

    def buscar_produto():
        termo = entry_busca.get()
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.codigo_barras, p.nome, p.dosagem, lp.lote, lp.preco, lp.quantidade, lp.validade
            FROM Produto p
            JOIN LoteProduto lp ON p.codigo_barras = lp.codigo_barras
         WHERE p.codigo_barras=? OR p.nome LIKE ?
        """, (termo, f"%{termo}%"))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            codigo, nome, dosagem, lote, preco, qtd, validade = resultado
            # preencher campos...
            entry_codigo.delete(0, tk.END); entry_codigo.insert(0, codigo)
            entry_nome.delete(0, tk.END); entry_nome.insert(0, nome)
            entry_dosagem.delete(0, tk.END); entry_dosagem.insert(0, dosagem)
            entry_lote.delete(0, tk.END); entry_lote.insert(0, lote)
            entry_preco.delete(0, tk.END); entry_preco.insert(0, preco)
            entry_qtd_estoque.delete(0, tk.END); entry_qtd_estoque.insert(0, qtd)

            # Verificações
            hoje = datetime.date.today()
            validade_dt = datetime.datetime.strptime(validade, "%Y-%m-%d").date()
            aviso = ""
            if validade_dt < hoje:
                aviso += "⚠ Produto VENCIDO!\n"
            elif (validade_dt - hoje).days <= 30:
                aviso += "⚠ Validade próxima!\n"
            if qtd == 0:
                aviso += "⚠ Estoque zerado!\n"
            elif qtd < 5:
                aviso += "⚠ Estoque baixo!\n"

            if aviso:
                messagebox.showwarning("Atenção", aviso)
        else:
            messagebox.showerror("Erro", "Produto não encontrado!")


    ttk.Button(janela, text="Buscar", width=20, command=buscar_produto).pack(pady=10)

    def salvar_item():
        try:
            codigo = entry_codigo.get()
            nome = entry_nome.get()
            dosagem = entry_dosagem.get()
            lote = entry_lote.get()
            preco_unitario = float(entry_preco.get())
            quantidade_venda = int(entry_quantidade_venda.get())
            subtotal = quantidade_venda * preco_unitario

            tree_venda.insert("", "end", values=(codigo, nome, dosagem, lote, quantidade_venda, preco_unitario, subtotal))
            janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Informe uma quantidade válida!")

    ttk.Button(janela, text="Adicionar", width=20, command=salvar_item).pack(pady=10)




