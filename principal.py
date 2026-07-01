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
from db import conexao, cursor


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

   # Frame superior (campos de entrada)
    frame_campos = tk.Frame(principal, bg="#cce6ff")
    frame_campos.pack(fill="x", padx=20, pady=10)

    #campo para codigo de barras
    tk.Label(frame_campos, text="Código de Barras:", bg="#cce6ff").pack(side="left", padx=5)
    global entry_codigo
    entry_codigo = ttk.Entry(frame_campos, width=20)
    entry_codigo.pack(side="left", padx=5)
    entry_codigo.focus_set()

    # 🔑 Quando apertar Enter no código → vai para quantidade
    entry_codigo.bind("<Return>", lambda event: entry_quantidade.focus_set())

    #campo para quantidade
    tk.Label(frame_campos, text="Quantidade:", bg="#cce6ff").pack(side="left", padx=5)
    global entry_quantidade
    entry_quantidade = ttk.Entry(frame_campos, width=10)
    entry_quantidade.pack(side="left", padx=5)

    # 🔑 Quando apertar Enter na quantidade → chama adicionar_item
    entry_quantidade.bind("<Return>", lambda event: adicionar_item(tree_venda))

    # Frame de vendas (Treeview + total)
    frame_vendas = tk.Frame(principal, bg="#cce6ff")
    frame_vendas.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(frame_vendas, text="Vendas", font=("Segoe UI", 16, "bold"), bg="#cce6ff").pack(pady=10)

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

    global tree_venda
    tree_venda = ttk.Treeview(frame_vendas, columns=colunas, show="headings")
    for col in colunas:
      tree_venda.heading(col, text=nomes_colunas[col])
    tree_venda.pack(fill="both", expand=True)
    tree_venda.bind("<<TreeviewSelect>>", preencher_campos)


    # Label do total
    global label_total
    label_total = tk.Label(frame_vendas, text="Total: R$ 0.00", font=("Arial", 14, "bold"), bg="#cce6ff")
    label_total.pack(pady=10)

    # Frame de botões
    frame_botoes = tk.Frame(principal, bg="#cce6ff")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Adicionar Item", bg="#4CAF50", fg="white",
           command=lambda: adicionar_item(tree_venda)).pack(side="left", padx=5)

    tk.Button(frame_botoes, text="Remover Item", bg="#f44336", fg="white",
             command=lambda: remover_item(tree_venda)).pack(side="left", padx=5)

    tk.Button(frame_botoes, text="Finalizar Venda", bg="#0066cc", fg="white",
          command=lambda: escolher_pagamento(tree_venda, perfil)).pack(side="left", padx=5)

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
        cursor.execute("SELECT * FROM Usuario WHERE login=? AND senha=? AND perfil='admin'", 
                       (entry_login.get(), entry_senha.get()))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Sucesso", "Acesso administrativo liberado!")
            abrir_funcoes_admin()
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Login ou senha inválidos.")

    ttk.Button(janela, text="Entrar", command=validar_admin).pack(pady=10)

def adicionar_item(tree_venda):
    codigo = entry_codigo.get().strip()
    quantidade = entry_quantidade.get().strip()

    # Validação dos campos
    if not codigo:
        messagebox.showwarning("Atenção", "Digite o código de barras antes de adicionar!")
        return
    if not quantidade.isdigit():
        messagebox.showwarning("Atenção", "Digite uma quantidade válida!")
        return

    quantidade = int(quantidade)

    cursor.execute("""
      SELECT p.nome, p.dosagem, lp.lote, lp.preco
        FROM LoteProduto lp
       JOIN Produto p ON lp.codigo_barras = p.codigo_barras
        WHERE lp.codigo_barras = ?
    """, (codigo,))
    produto = cursor.fetchone()

    if produto:
        nome, dosagem, lote, preco = produto
        subtotal = quantidade * preco
        
        selecionado = tree_venda.selection()
        if selecionado:
            # Atualiza item existente
            tree_venda.item(selecionado, values=(codigo, nome, dosagem, lote, quantidade, preco, subtotal))
        else:
            # Insere novo item
            tree_venda.insert("", "end", values=(codigo, nome, dosagem, lote, quantidade, preco, subtotal))

        atualizar_total(tree_venda, label_total)

        # Limpa campos
        entry_codigo.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
        entry_codigo.focus_set()
        # 🔑 Limpa a seleção para permitir novo item
        tree_venda.selection_remove(tree_venda.selection())
    else:
        messagebox.showerror("Erro", "Produto não encontrado!")

#função para atualizar o total da venda
def atualizar_total(tree_venda, total_label):
    total = 0.0
    for item in tree_venda.get_children():
        subtotal = float(tree_venda.item(item, "values")[6])  # índice 6 é o subtotal
        total += subtotal
    total_label.config(text=f"Total: R$ {total:.2f}")

def remover_item(tree_venda):
    selecionado = tree_venda.selection()
    if selecionado:
        valores = tree_venda.item(selecionado, "values")
        nome_produto = valores[1]  # coluna do nome (ajuste se necessário)

        resposta = messagebox.askyesno(
            "Confirmação",
            f"Deseja realmente remover {nome_produto} da lista?"
        )
        if resposta:
            tree_venda.delete(selecionado)
            atualizar_total(tree_venda, label_total)
    else:
        messagebox.showwarning("Atenção", "Selecione um item para remover!")

def finalizar_venda(tree_venda, perfil, forma_pagamento, janela_pagamento=None):

    cursor = sqlite3.connect("saracaFarma.db").cursor()

    if not tree_venda.get_children():
        messagebox.showwarning("Atenção", "Nenhum item na venda!")
        return

    total = 0.0
    itens_venda = []

    for item in tree_venda.get_children():
        valores = tree_venda.item(item, "values")
        codigo_barras = valores[0]
        quantidade = int(valores[4])
        preco_unitario = float(valores[5])
        subtotal = float(valores[6])
        total += subtotal
        itens_venda.append((codigo_barras, quantidade, preco_unitario, subtotal))

        # Atualiza estoque
        cursor.execute("UPDATE LoteProduto SET quantidade = quantidade - ? WHERE codigo_barras = ?", (quantidade, codigo_barras))

    # Registra venda com forma de pagamento
    cursor.execute("INSERT INTO Venda (data, id_usuario, id_produto, quantidade, valor_total) VALUES (datetime('now'), ?, ?, ?, ?)",
                   (perfil, itens_venda[0][0], itens_venda[0][1], total))
    id_venda = cursor.lastrowid

    # Registra itens
    for codigo_barras, quantidade, preco_unitario, subtotal in itens_venda:
        cursor.execute("INSERT INTO ItensVenda (id_venda, codigo_barras, lote, quantidade, preco_unitario, subtotal) VALUES (?, ?, '', ?, ?, ?)",
                       (id_venda, codigo_barras, quantidade, preco_unitario, subtotal))

    conexao.commit()

    resumo = "\n".join([f"{qtd}x {codigo} - R$ {subtotal:.2f}" for (codigo, qtd, _, subtotal) in itens_venda])
    messagebox.showinfo("Venda Finalizada", f"Resumo da venda:\n\n{resumo}\n\nTotal: R$ {total:.2f}\nPagamento: {forma_pagamento}")

    # Fecha janela de pagamento
    if janela_pagamento:
        janela_pagamento.destroy()

    # Limpa tela
    tree_venda.delete(*tree_venda.get_children())
    label_total.config(text="Total: R$ 0.00")


def preencher_campos(event):
    selecionado = tree_venda.selection()
    if selecionado:
        valores = tree_venda.item(selecionado, "values")
        codigo = valores[0]
        quantidade = valores[4]

        # Preenche os campos
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, codigo)

        entry_quantidade.delete(0, tk.END)
        entry_quantidade.insert(0, quantidade)

def foco_quantidade(event=None):
    entry_quantidade.focus_set()

def escolher_pagamento(tree_venda, perfil):
    # Janela popup
    janela_pagamento = tk.Toplevel()
    janela_pagamento.title("Forma de Pagamento")
    janela_pagamento.geometry("300x250")
    janela_pagamento.configure(bg="#cce6ff")

    tk.Label(janela_pagamento, text="Selecione a forma de pagamento:", 
             font=("Segoe UI", 12, "bold"), bg="#cce6ff").pack(pady=10)

    forma_pagamento = tk.StringVar(value="dinheiro")

    # Opções
    tk.Radiobutton(janela_pagamento, text="Dinheiro", variable=forma_pagamento, value="dinheiro", bg="#cce6ff").pack(anchor="w", padx=20)
    tk.Radiobutton(janela_pagamento, text="Cartão Crédito", variable=forma_pagamento, value="cartao_credito", bg="#cce6ff").pack(anchor="w", padx=20)
    tk.Radiobutton(janela_pagamento, text="Cartão Débito", variable=forma_pagamento, value="cartao_debito", bg="#cce6ff").pack(anchor="w", padx=20)
    tk.Radiobutton(janela_pagamento, text="Fiado (Crédito)", variable=forma_pagamento, value="fiado", bg="#cce6ff").pack(anchor="w", padx=20)
    tk.Radiobutton(janela_pagamento, text="Pix", variable=forma_pagamento, value="pix", bg="#cce6ff").pack(anchor="w", padx=20)

    # Botão confirmar
    def confirmar():
        total = calcular_total(tree_venda)  # função que soma subtotais
        janela_pagamento.destroy()

        if forma_pagamento.get() == "dinheiro":
            pagamento_dinheiro(total, perfil, tree_venda)
        else:
            finalizar_venda(tree_venda, perfil, forma_pagamento.get())

    tk.Button(janela_pagamento, text="Confirmar", bg="#4CAF50", fg="white",
              command=confirmar).pack(pady=15)


def pagamento_dinheiro(total, perfil, tree_venda):
    janela_dinheiro = tk.Toplevel()
    janela_dinheiro.title("Pagamento em Dinheiro")
    janela_dinheiro.geometry("350x300")
    janela_dinheiro.configure(bg="#f0f8ff")

    tk.Label(janela_dinheiro, text=f"Total da compra: R$ {total:.2f}", 
             font=("Segoe UI", 12, "bold"), bg="#f0f8ff").pack(pady=10)

    # Campo para valor recebido
    tk.Label(janela_dinheiro, text="Valor recebido:", bg="#f0f8ff").pack()
    entry_valor = ttk.Entry(janela_dinheiro)
    entry_valor.pack(pady=5)

    # Campo para desconto
    tk.Label(janela_dinheiro, text="Desconto (R$ ou %):", bg="#f0f8ff").pack()
    entry_desconto = ttk.Entry(janela_dinheiro)
    entry_desconto.pack(pady=5)

    resultado_label = tk.Label(janela_dinheiro, text="", bg="#f0f8ff", fg="blue")
    resultado_label.pack(pady=10)

    def calcular_troco():
        try:
            valor_recebido = float(entry_valor.get())
            desconto = entry_desconto.get().strip()

            # Aplica desconto
            valor_final = total
            if desconto.endswith("%"):
                perc = float(desconto[:-1])
                valor_final -= (valor_final * perc / 100)
            elif desconto:
                valor_final -= float(desconto)

            troco = valor_recebido - valor_final
            if troco < 0:
                resultado_label.config(text=f"Valor insuficiente! Faltam R$ {-troco:.2f}", fg="red")
            else:
                resultado_label.config(text=f"Troco: R$ {troco:.2f}", fg="green")
                # Aqui chamamos finalizar_venda com forma_pagamento = 'dinheiro'
                finalizar_venda(tree_venda, perfil, "dinheiro", janela_dinheiro)
        except ValueError:
            messagebox.showwarning("Erro", "Digite valores válidos!")

    tk.Button(janela_dinheiro, text="Confirmar Pagamento", bg="#4CAF50", fg="white",
              command=calcular_troco).pack(pady=15)

def calcular_total(tree_venda):
    total = 0.0
    for item in tree_venda.get_children():
        valores = tree_venda.item(item, "values")
        subtotal = float(valores[6])  # coluna do subtotal
        total += subtotal
    return total