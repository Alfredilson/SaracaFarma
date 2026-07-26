import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import ttk
import sqlite3
from admin import abrir_funcoes_admin
from clinte import cadastrar_cliente, listar_clientes
from produto import cadastrar_produto
from produto import cadastrar_produtos_treeview 
#---from produto import cadastrar_produtos_csvgit
from produto import cadastrar_produtos_fornecedor
from tkinter import filedialog
from controle_estoque import tela_estoque, tela_relatorio
import datetime
from db import conexao, cursor
from ui_theme import apply_theme, styled_button, PRIMARY_BG, HEADER_BG, HEADER_FG, SECONDARY_BG, INFO_FG, TREE_BG, TREE_SEL_BG, TREE_HEADING_FG, TEXT_PRIMARY_FG, BUTTON_TEXT_FG

def cadastrar_lista_produtos():
    # Função placeholder para cadastro em lote
    arquivo = filedialog.askopenfilename(title="Selecionar arquivo de produtos", filetypes=[("CSV", "*.csv"), ("Todos", "*")])
    if arquivo:
        messagebox.showinfo("Cadastro em Lote", f"Arquivo selecionado: {arquivo}\nFuncionalidade ainda não implementada.")

def tela_principal(id_usuario):
    # obtém o perfil (admin/funcionario) do usuário logado
    cursor.execute("SELECT perfil FROM Usuario WHERE id_usuario = ?", (id_usuario,))
    row = cursor.fetchone()
    perfil = row[0] if row else None

    principal = tk.Tk()
    principal.title("SaracaFarma - Tela Principal")
    apply_theme(principal)

    # Faz a janela abrir maximizada em todas as plataformas
    try:
        principal.state("zoomed")
    except Exception:
        pass
    try:
        principal.attributes("-zoomed", True)
    except Exception:
        pass
    # Fallback: se não foi possível maximizar, ajustar para o tamanho da tela
    try:
        # Alguns backends não respeitam 'zoomed' — definir geometry como fallback
        if principal.wm_state() not in ("zoomed", "iconic"):
            principal.geometry(f"{principal.winfo_screenwidth()}x{principal.winfo_screenheight()}+0+0")
    except Exception:
        pass

    # Fechamento seguro
    def fechar_programa():
        from db import conexao
        conexao.close()
        principal.destroy()

    principal.protocol("WM_DELETE_WINDOW", fechar_programa)

    # Criar barra de menu
    menubar = tk.Menu(principal)

      # Menu Cadastro
    menu_cadastro = tk.Menu(menubar, tearoff=0)
    # Chamada direta da função de cadastro de produto (passa janela principal e id do usuário)
    menu_cadastro.add_command(label="Cadastro Individual", command=lambda: cadastrar_produto(principal, id_usuario))
    menu_cadastro.add_command(label="Cadastro em Lote (Treeview)", command=lambda: cadastrar_produtos_treeview(principal, id_usuario))
    #---menu_cadastro.add_command(label="Cadastro em Lote (CSV)", command=lambda: cadastrar_produtos_csv(principal, id_usuario))
    menu_cadastro.add_command(label="Cadastro em Lote via Fornecedor", command=lambda: cadastrar_produtos_fornecedor(principal, id_usuario))


    menubar.add_cascade(label="Cadastro", menu=menu_cadastro)

     # Menu Estoque
    menu_estoque = tk.Menu(menubar, tearoff=0)
    menu_estoque.add_command(label="Controle de Estoque", command=lambda: tela_estoque(principal, id_usuario))
    menu_estoque.add_command(label="Controlar Relatorio", command=lambda: tela_relatorio(principal))
    menu_estoque.add_command(label="Consultar Saldo",)
    menubar.add_cascade(label="Estoque", menu=menu_estoque)

    # Menu Cliente
    menu_cliente = tk.Menu(menubar, tearoff=0)
    menu_cliente.add_command(label="Cadastro de Cliente", command=lambda: cadastrar_cliente(principal))
    menu_cliente.add_command(label="Lista de Clientes", command=lambda: listar_clientes(principal))
    menubar.add_cascade(label="Cliente", menu=menu_cliente)

    # Menu Administração (somente se perfil for admin)
    if perfil == "admin":
        menu_admin = tk.Menu(menubar, tearoff=0)
        menu_admin.add_command(label="Funções Administrativas", command=lambda: abrir_funcoes_admin(principal))
        menubar.add_cascade(label="Administração", menu=menu_admin)
    
       # Menu Sair
    menu_sair = tk.Menu(menubar, tearoff=0)
    menu_sair.add_command(label="Encerrar", command=principal.quit)
    menubar.add_cascade(label="Sair", menu=menu_sair)

    barra = tk.Frame(principal, bg=HEADER_BG, height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Tela Principal - SaracaFarma", fg=HEADER_FG, bg=HEADER_BG, font=("Segoe UI", 14, "bold")).pack(pady=5)

   
   
    frame = tk.Frame(principal, bg=PRIMARY_BG)
    frame.pack(pady=30)

    
    
    # Associar menu à janela
    principal.config(menu=menubar)


    style = ttk.Style()
    style.theme_use("default")

    # Estilo da Treeview (linhas)
    style.configure("Treeview",
        background=TREE_BG,
        foreground=TEXT_PRIMARY_FG,
        rowheight=25,
        fieldbackground=TREE_BG
    )

    style.map("Treeview",
        background=[("selected", TREE_SEL_BG)],
        foreground=[("selected", BUTTON_TEXT_FG)]
    )

    # Estilo do cabeçalho (descrição das colunas)
    style.configure("Treeview.Heading",
        background=HEADER_BG,
        foreground=TREE_HEADING_FG,
        font=("Segoe UI", 11, "bold")
)

   # Frame superior (campos de entrada)
    frame_campos = tk.Frame(principal, bg=PRIMARY_BG)
    frame_campos.pack(fill="x", padx=20, pady=10)

    #campo para codigo de barras
    tk.Label(frame_campos, text="Código de Barras:", bg=PRIMARY_BG).pack(side="left", padx=5)
    global entry_codigo
    entry_codigo = ttk.Entry(frame_campos, width=20)
    entry_codigo.pack(side="left", padx=5)
    entry_codigo.focus_set()

    # 🔑 Quando apertar Enter no código → vai para quantidade
    entry_codigo.bind("<Return>", lambda event: entry_quantidade.focus_set())

    #campo para quantidade
    tk.Label(frame_campos, text="Quantidade:", bg=PRIMARY_BG).pack(side="left", padx=5)
    global entry_quantidade
    entry_quantidade = ttk.Entry(frame_campos, width=10)
    entry_quantidade.pack(side="left", padx=5)

    # 🔑 Quando apertar Enter na quantidade → chama adicionar_item
    entry_quantidade.bind("<Return>", lambda event: adicionar_item(tree_venda))

    cliente_map = {}
    cliente_id_selecionado = {"id": None}

    def carregar_clientes_venda():
        cliente_map.clear()
        valores = ["Nenhum"]
        cursor.execute("SELECT id_cliente, nome, cpf FROM Cliente ORDER BY nome")
        for id_cliente, nome, cpf in cursor.fetchall():
            display = f"{nome} - {cpf}"
            cliente_map[display] = id_cliente
            valores.append(display)
        combo_cliente['values'] = valores
        combo_cliente.set("Nenhum")
        cliente_id_selecionado["id"] = None

    def atualizar_cliente_selecionado(event=None):
        display = combo_cliente.get()
        if display == "Nenhum":
            cliente_id_selecionado["id"] = None
        else:
            cliente_id_selecionado["id"] = cliente_map.get(display)

    def limpar_cliente():
        combo_cliente.set("Nenhum")
        cliente_id_selecionado["id"] = None

    frame_cliente = tk.Frame(principal, bg=PRIMARY_BG)
    frame_cliente.pack(fill="x", padx=20, pady=(10, 0))
    tk.Label(frame_cliente, text="Cliente (opcional):", bg=PRIMARY_BG).pack(side="left", padx=5)
    combo_cliente = ttk.Combobox(frame_cliente, width=40, state="readonly")
    combo_cliente.pack(side="left", padx=5)
    combo_cliente.bind("<<ComboboxSelected>>", atualizar_cliente_selecionado)
    styled_button(frame_cliente, text="Limpar cliente", kind="primary", command=limpar_cliente).pack(side="left", padx=5)
    carregar_clientes_venda()

    # Frame de vendas (Treeview + total)
    frame_vendas = tk.Frame(principal, bg=PRIMARY_BG)
    frame_vendas.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(frame_vendas, text="Vendas", font=("Segoe UI", 16, "bold"), bg=PRIMARY_BG).pack(pady=10)

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
    label_total = tk.Label(frame_vendas, text="Total: R$ 0.00", font=("Arial", 14, "bold"), bg=PRIMARY_BG)
    label_total.pack(pady=10)

    # Frame de botões
    frame_botoes = tk.Frame(principal, bg=PRIMARY_BG)
    frame_botoes.pack(pady=10)

    styled_button(frame_botoes, text="Adicionar Item", kind="secondary",
           command=lambda: adicionar_item(tree_venda)).pack(side="left", padx=5)

    styled_button(frame_botoes, text="Remover Item", kind="danger",
             command=lambda: remover_item(tree_venda)).pack(side="left", padx=5)

    styled_button(frame_botoes, text="Finalizar Venda", kind="primary",
          command=lambda: escolher_pagamento(tree_venda, id_usuario, cliente_id_selecionado["id"])).pack(side="left", padx=5)

    principal.mainloop()

def verificar_admin():

    janela = tk.Toplevel()
    janela.title("Verificação Admin")
    janela.geometry("300x200")
    janela.configure(bg=PRIMARY_BG)

    tk.Label(janela, text="Login Admin:", bg=PRIMARY_BG).pack(pady=5)
    entry_login = ttk.Entry(janela, width=25)
    entry_login.pack(pady=5)

    tk.Label(janela, text="Senha:", bg=PRIMARY_BG).pack(pady=5)
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

    styled_button(janela, text="Entrar", command=validar_admin).pack(pady=10)

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

def finalizar_venda(tree_venda, perfil, forma_pagamento, janela_pagamento, id_cliente=None):
    # perfil aqui representa o id do usuário que efetuou a venda
    if not tree_venda.get_children():
        messagebox.showwarning("Atenção", "Nenhum item na venda!")
        return

    total = 0.0
    itens_venda = []

    # Primeiro: validar se há estoque suficiente para todos os itens
    for item in tree_venda.get_children():
        valores = tree_venda.item(item, "values")
        codigo_barras = valores[0]
        lote = valores[3]
        quantidade = int(valores[4])
        preco_unitario = float(valores[5])
        subtotal = float(valores[6])
        total += subtotal
        itens_venda.append((codigo_barras, lote, quantidade, preco_unitario, subtotal))

    # checar estoque por lote antes de aplicar alterações
    for codigo_barras, lote, quantidade, _, _ in itens_venda:
        cursor.execute("SELECT quantidade FROM LoteProduto WHERE codigo_barras = ? AND lote = ?", (codigo_barras, lote))
        row = cursor.fetchone()
        if not row or row[0] < quantidade:
            messagebox.showwarning("Estoque insuficiente", f"Estoque insuficiente para {codigo_barras} (lote {lote}). Disponível: {row[0] if row else 0}, necessário: {quantidade}.")
            return

    # Atualiza estoque por lote (já validado)
    for codigo_barras, lote, quantidade, _, _ in itens_venda:
        cursor.execute("UPDATE LoteProduto SET quantidade = quantidade - ? WHERE codigo_barras = ? AND lote = ?", (quantidade, codigo_barras, lote))

    # calcula quantidade total vendida
    quantidade_total = sum(i[2] for i in itens_venda)

    # normalize forma_pagamento para os valores aceitos pelo schema
    fp = str(forma_pagamento).lower()
    if "pix" in fp:
        forma = "pix"
    elif "fiado" in fp:
        forma = "fiado"
    elif "cart" in fp or "cartão" in fp or "cartao" in fp:
        if "débito" in fp or "debito" in fp or "débito" in forma_pagamento:
            forma = "cartao_debito"
        else:
            forma = "cartao_credito"
    else:
        forma = "dinheiro"

    # Registra venda (usa primeiro produto como referência em id_produto)
    primeiro_produto = itens_venda[0][0] if itens_venda else None
    cursor.execute(
        "INSERT INTO Venda (data, id_usuario, id_produto, quantidade, valor_total, forma_pagamento, id_cliente) VALUES (datetime('now'), ?, ?, ?, ?, ?, ?)",
        (perfil, primeiro_produto, quantidade_total, total, forma, id_cliente)
    )
    id_venda = cursor.lastrowid

    # Registra itens corretamente
    for codigo_barras, lote, quantidade, preco_unitario, subtotal in itens_venda:
        cursor.execute(
            "INSERT INTO ItensVenda (id_venda, codigo_barras, lote, quantidade, preco_unitario, subtotal) VALUES (?, ?, ?, ?, ?, ?)",
            (id_venda, codigo_barras, lote, quantidade, preco_unitario, subtotal)
        )

    conexao.commit()

    resumo = "\n".join([f"{qtd}x {codigo} - R$ {subtotal:.2f}" for (codigo, lote, qtd, _, subtotal) in itens_venda])
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

def escolher_pagamento(tree_venda, perfil, id_cliente=None):
    # Janela popup
    janela_pagamento = tk.Toplevel()
    janela_pagamento.title("Forma de Pagamento")
    janela_pagamento.geometry("300x250")
    apply_theme(janela_pagamento)
    janela_pagamento.configure(bg=PRIMARY_BG)

    tk.Label(janela_pagamento, text="Selecione a forma de pagamento:", 
             font=("Segoe UI", 12, "bold"), bg=PRIMARY_BG).pack(pady=10)

    forma_pagamento = tk.StringVar(value="dinheiro")

    # Opções
    tk.Radiobutton(janela_pagamento, text="Dinheiro", variable=forma_pagamento, value="dinheiro", bg=PRIMARY_BG).pack(anchor="w", padx=20)
    tk.Radiobutton(janela_pagamento, text="Cartão", variable=forma_pagamento, value="cartao", bg=PRIMARY_BG).pack(anchor="w", padx=20)
    tk.Radiobutton(janela_pagamento, text="Fiado (Crédito)", variable=forma_pagamento, value="fiado", bg=PRIMARY_BG).pack(anchor="w", padx=20)
    tk.Radiobutton(janela_pagamento, text="Pix", variable=forma_pagamento, value="pix", bg=PRIMARY_BG).pack(anchor="w", padx=20)

    # Botão confirmar
    def confirmar():
        total = calcular_total(tree_venda)  # função que soma subtotais
        janela_pagamento.destroy()

        if forma_pagamento.get() == "dinheiro":
            pagamento_dinheiro(total, perfil, tree_venda, id_cliente=id_cliente)
        elif forma_pagamento.get() == "cartao":
            pagamento_cartao(total, perfil, tree_venda, id_cliente=id_cliente)
        elif forma_pagamento.get() == "fiado":
            pagamento_fiado(total, perfil, tree_venda, id_cliente=id_cliente)
        else:
            finalizar_venda(tree_venda, perfil, forma_pagamento.get(), janela_pagamento, id_cliente=id_cliente)

    styled_button(janela_pagamento, text="Confirmar", kind="secondary",
              command=confirmar).pack(pady=15)


def pagamento_dinheiro(total, perfil, tree_venda, id_cliente=None):
    janela_dinheiro = tk.Toplevel()
    janela_dinheiro.title("Pagamento em Dinheiro")
    janela_dinheiro.geometry("350x300")
    apply_theme(janela_dinheiro)
    janela_dinheiro.configure(bg=SECONDARY_BG)

    tk.Label(janela_dinheiro, text=f"Total da compra: R$ {total:.2f}", 
             font=("Segoe UI", 12, "bold"), bg=SECONDARY_BG).pack(pady=10)

    # Campo para valor recebido
    tk.Label(janela_dinheiro, text="Valor recebido:", bg=SECONDARY_BG).pack()
    entry_valor = ttk.Entry(janela_dinheiro)
    entry_valor.pack(pady=5)

    # Campo para desconto
    tk.Label(janela_dinheiro, text="Desconto (R$ ou %):", bg=SECONDARY_BG).pack()
    entry_desconto = ttk.Entry(janela_dinheiro)
    entry_desconto.pack(pady=5)

    resultado_label = tk.Label(janela_dinheiro, text="", bg=SECONDARY_BG, fg=INFO_FG)
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
                resultado_label.config(text=f"Valor insuficiente! Faltam R$ {-troco:.2f}", fg=ERROR_FG)
                confirmar_btn.config(state="disabled")
            else:
                resultado_label.config(text=f"Troco: R$ {troco:.2f}", fg=SUCCESS_FG)
                confirmar_btn.config(state="normal")
        except ValueError:
            messagebox.showwarning("Erro", "Digite valores válidos!")

    def confirmar_pagamento():
        # Só confirma se o botão estiver habilitado
        finalizar_venda(tree_venda, perfil, "dinheiro", janela_dinheiro, id_cliente=id_cliente)

    styled_button(janela_dinheiro, text="Calcular Troco", kind="info", command=calcular_troco).pack(pady=10)

    confirmar_btn = styled_button(janela_dinheiro, text="Confirmar Pagamento",
                              kind="secondary",
                              command=confirmar_pagamento, state="disabled")
    confirmar_btn.pack(pady=15)

def calcular_total(tree_venda):
    total = 0.0
    for item in tree_venda.get_children():
        valores = tree_venda.item(item, "values")
        subtotal = float(valores[6])  # coluna do subtotal
        total += subtotal
    return total

def pagamento_cartao(total, perfil, tree_venda, id_cliente=None):
    janela_cartao = tk.Toplevel()
    janela_cartao.title("Pagamento com Cartão")
    janela_cartao.geometry("350x250")
    apply_theme(janela_cartao)
    janela_cartao.configure(bg=SECONDARY_BG)

    tk.Label(janela_cartao, text=f"Total da compra: R$ {total:.2f}",
             font=("Segoe UI", 12, "bold"), bg=SECONDARY_BG).pack(pady=10)

    # Escolha do tipo de cartão
    tk.Label(janela_cartao, text="Selecione o tipo de cartão:", bg=SECONDARY_BG).pack()
    tipo_cartao = tk.StringVar(value="crédito")
    tk.Radiobutton(janela_cartao, text="Crédito", variable=tipo_cartao, value="crédito",
                   bg=SECONDARY_BG, activebackground=SECONDARY_BG, selectcolor=SECONDARY_BG).pack()
    tk.Radiobutton(janela_cartao, text="Débito", variable=tipo_cartao, value="débito",
                   bg=SECONDARY_BG, activebackground=SECONDARY_BG, selectcolor=SECONDARY_BG).pack()

    # Campo opcional para código de autorização
    tk.Label(janela_cartao, text="Código de autorização (opcional):", bg=SECONDARY_BG).pack()
    entry_codigo = ttk.Entry(janela_cartao)
    entry_codigo.pack(pady=5)

    def confirmar_pagamento():
        codigo = entry_codigo.get().strip()
        forma = f"cartão {tipo_cartao.get()}"
        if codigo:
            messagebox.showinfo("Pagamento aprovado", f"Compra registrada com {forma}.\nAutorização: {codigo}")
        else:
            messagebox.showinfo("Pagamento aprovado", f"Compra registrada com {forma}.")
        finalizar_venda(tree_venda, perfil, forma, janela_cartao, id_cliente=id_cliente)

    styled_button(janela_cartao, text="Confirmar Pagamento", kind="secondary",
              command=confirmar_pagamento).pack(pady=15)

def pagamento_fiado(total, perfil, tree_venda, id_cliente=None):
    janela_fiado = tk.Toplevel()
    janela_fiado.title("Pagamento Fiado")
    janela_fiado.geometry("450x320")
    apply_theme(janela_fiado)
    janela_fiado.configure(bg=SECONDARY_BG)

    tk.Label(janela_fiado, text=f"Total da compra: R$ {total:.2f}",
             font=("Segoe UI", 12, "bold"), bg=SECONDARY_BG).pack(pady=10)

    cliente_id = {"id": id_cliente}

    label_cliente = tk.Label(janela_fiado, text="Cliente não selecionado", bg=SECONDARY_BG)
    label_cliente.pack(pady=5)

    if cliente_id["id"]:
        cursor.execute("SELECT nome, cpf FROM Cliente WHERE id_cliente = ?", (cliente_id["id"],))
        row = cursor.fetchone()
        if row:
            label_cliente.config(text=f"Cliente selecionado: {row[0]} - {row[1]}")

    tk.Label(janela_fiado, text="Cliente (nome ou CPF):", bg=SECONDARY_BG).pack()
    entry_cliente = ttk.Entry(janela_fiado, width=40)
    entry_cliente.pack(pady=5)

    def buscar_cliente_por_texto():
        busca = entry_cliente.get().strip()
        if not busca:
            messagebox.showwarning("Erro", "Informe o nome ou CPF do cliente!")
            return

        cursor.execute("SELECT id_cliente, nome, cpf FROM Cliente WHERE nome = ? OR cpf = ?", (busca, busca))
        resultado = cursor.fetchone()
        if resultado:
            cliente_id["id"] = resultado[0]
            label_cliente.config(text=f"Cliente selecionado: {resultado[1]} - {resultado[2]}")
        else:
            messagebox.showwarning("Erro", "Cliente não encontrado! Cadastre primeiro.")

    def selecionar_cliente_popup():
        popup = tk.Toplevel(janela_fiado)
        popup.title("Selecionar Cliente para Fiado")
        popup.geometry("560x380")
        apply_theme(popup)
        popup.configure(bg=PRIMARY_BG)
        popup.transient(janela_fiado)
        popup.grab_set()

        frame = tk.Frame(popup, bg=PRIMARY_BG)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id_cliente", "nome", "cpf")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        tree.heading("id_cliente", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("cpf", text="CPF")
        tree.column("id_cliente", width=80, anchor="center")
        tree.column("nome", width=260)
        tree.column("cpf", width=180, anchor="center")
        tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        cursor.execute("SELECT id_cliente, nome, cpf FROM Cliente ORDER BY nome")
        for cliente in cursor.fetchall():
            tree.insert("", "end", values=cliente)

        def confirmar_selecao():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Atenção", "Selecione um cliente.")
                return
            valores = tree.item(sel[0], "values")
            cliente_id["id"] = int(valores[0])
            label_cliente.config(text=f"Cliente selecionado: {valores[1]} - {valores[2]}")
            popup.destroy()

        styled_button(popup, text="Selecionar", kind="secondary", command=confirmar_selecao).pack(pady=10)
        popup.wait_window()

    def confirmar_fiado():
        if cliente_id["id"] is None:
            buscar_cliente_por_texto()
            if cliente_id["id"] is None:
                return

        # Finaliza venda com forma_pagamento = fiado
        finalizar_venda(tree_venda, perfil, "fiado", janela_fiado, id_cliente=cliente_id["id"])

    frame_actions = tk.Frame(janela_fiado, bg=SECONDARY_BG)
    frame_actions.pack(pady=10)
    styled_button(frame_actions, text="Buscar Cliente", kind="primary", command=buscar_cliente_por_texto).pack(side="left", padx=5)
    styled_button(frame_actions, text="Selecionar Cliente", kind="primary", command=selecionar_cliente_popup).pack(side="left", padx=5)

    styled_button(janela_fiado, text="Confirmar Fiado", kind="secondary",
              command=confirmar_fiado).pack(pady=15)

