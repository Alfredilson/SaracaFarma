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
          command=lambda: finalizar_venda(tree_venda, perfil)).pack(side="left", padx=5)



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

    conn = sqlite3.connect("saracaFarma.db")
    cursor = conn.cursor()
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

def finalizar_venda(tree_venda, id_usuario):
    conexao = sqlite3.connect("saracaFarma.db")
    cursor = conexao.cursor()
    
    if not tree_venda.get_children():
        messagebox.showwarning("Atenção", "Nenhum item na venda!")
        return

    total = 0.0
    itens_venda = []

    for item in tree_venda.get_children():
        valores = tree_venda.item(item, "values")
        codigo_barras = valores[0]
        nome = valores[1]
        lote = valores[3]
        quantidade = int(valores[4])
        preco_unitario = float(valores[5])
        subtotal = float(valores[6])

        total += subtotal
        itens_venda.append((codigo_barras, lote, quantidade, preco_unitario, subtotal))

        # Dá baixa no estoque
        cursor.execute(
            "UPDATE LoteProduto SET quantidade = quantidade - ? WHERE codigo_barras = ? AND lote = ?",
            (quantidade, codigo_barras, lote)
        )

    # Registra a venda principal
    cursor.execute(
        "INSERT INTO Venda (data, id_usuario, id_produto, quantidade, valor_total) VALUES (datetime('now'), ?, ?, ?, ?)",
        (id_usuario, itens_venda[0][0], itens_venda[0][2], total)  # usa o primeiro produto como referência
    )
    id_venda = cursor.lastrowid

    # Registra os itens da venda
    for codigo_barras, lote, quantidade, preco_unitario, subtotal in itens_venda:
        cursor.execute(
            "INSERT INTO ItensVenda (id_venda, codigo_barras, lote, quantidade, preco_unitario, subtotal) VALUES (?, ?, ?, ?, ?, ?)",
            (id_venda, codigo_barras, lote, quantidade, preco_unitario, subtotal)
        )

    conexao.commit()

    resumo = "\n".join([f"{qtd}x {codigo} - R$ {subtotal:.2f}" for (codigo, _, qtd, _, subtotal) in itens_venda])
    messagebox.showinfo("Venda Finalizada", f"Resumo da venda:\n\n{resumo}\n\nTotal: R$ {total:.2f}")

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
