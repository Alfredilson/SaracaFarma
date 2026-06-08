import sqlite3
import tkinter as tk
from tkinter import ttk
from produto import cadastrar_produto, cadastrar_produtos_fornecedor
import datetime

# Função para consultar o estoque e atualizar a Treeview
def consultar_estoque(tree, status_label):
    try:
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()

        # Consulta todos os produtos cadastrados
        cursor.execute("""
            SELECT DISTINCT p.codigo_barras, p.nome, p.categoria, p.apresentacao, p.dosagem, p.fabricante,
                            l.lote, l.quantidade, l.validade, l.preco
            FROM Produto p
            JOIN LoteProduto l ON p.codigo_barras = l.codigo_barras
            WHERE l.quantidade > 0
        """)
        registros = cursor.fetchall()

        # Limpa a Treeview antes de atualizar
        for item in tree.get_children():
            tree.delete(item)

        # Insere os registros na Treeview
        for registro in registros:
            tree.insert("", tk.END, values=registro)

        # Mensagem de sucesso exibida na própria tela
        status_label.config(text="Estoque atualizado com sucesso!", foreground="green")

        conn.close()
    except Exception as e:
        # Mensagem de erro exibida na própria tela
        status_label.config(text=f"Erro ao consultar estoque: {e}", foreground="red")



def baixa_estoque(tree, status_label, id_usuario=None):
    itens = tree.selection()
    if not itens:
        status_label.config(text="Selecione um ou mais produtos para dar baixa.", fg="red")
        return

    janela_baixa = tk.Toplevel()
    janela_baixa.title("Baixa de Estoque")
    janela_baixa.configure(bg="#cce6ff")

    tk.Label(janela_baixa, text="Quantidade a dar baixa:", bg="#cce6ff").pack(pady=5)
    entry_qtd = ttk.Entry(janela_baixa)
    entry_qtd.pack(pady=5)

    def confirmar_baixa():
        try:
            qtd_baixa = int(entry_qtd.get())
        except ValueError:
            status_label.config(text="Erro: informe um número válido.", fg="red")
            return

        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        erros, sucessos = [], []

        for item in itens:
            valores = tree.item(item, "values")
            codigo_barras = valores[0]
            lote = valores[6]

            cursor.execute("SELECT quantidade FROM LoteProduto WHERE codigo_barras=? AND lote=?",
                           (codigo_barras, lote))
            atual = cursor.fetchone()

            if atual and atual[0] >= qtd_baixa:
                nova_qtd = atual[0] - qtd_baixa

                if nova_qtd == 0:
                    cursor.execute("DELETE FROM LoteProduto WHERE codigo_barras=? AND lote=?",
                                   (codigo_barras, lote))
                else:
                    cursor.execute("UPDATE LoteProduto SET quantidade=? WHERE codigo_barras=? AND lote=?",
                                   (nova_qtd, codigo_barras, lote))

                # Registrar movimentação
                cursor.execute("""
                    INSERT INTO MovimentacaoEstoque (codigo_barras, lote, tipo, quantidade, data, id_usuario)
                    VALUES (?, ?, 'baixa', ?, ?, ?)
                """, (codigo_barras, lote, qtd_baixa, datetime.date.today(), id_usuario))

                sucessos.append(f"{valores[1]} - Lote {lote}")
            else:
                erros.append(f"{valores[1]} - Lote {lote}")

        conn.commit()
        conn.close()

        if sucessos:
            status_label.config(text=f"Baixa realizada: {', '.join(sucessos)}", fg="green")
        if erros:
            status_label.config(text=f"Erro: estoque insuficiente em {', '.join(erros)}", fg="red")

        consultar_estoque(tree, status_label)
        janela_baixa.destroy()

    ttk.Button(janela_baixa, text="Confirmar", command=confirmar_baixa).pack(pady=10)

def consultar_saldo(tree):
    conn = sqlite3.connect("saracaFarma.db")
    cursor = conn.cursor()

    query = """
        SELECT codigo_barras, lote,
               SUM(CASE WHEN tipo='entrada' THEN quantidade
                        WHEN tipo='baixa' THEN -quantidade END) AS saldo
        FROM MovimentacaoEstoque
        GROUP BY codigo_barras, lote
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    # Limpar Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Ajustar colunas para saldo
    tree["columns"] = ("codigo_barras", "lote", "saldo")
    for col in ("codigo_barras", "lote", "saldo"):
        tree.heading(col, text=col)

    # Inserir resultados
    for row in resultados:
        tree.insert("", "end", values=row)

    conn.close()

def consultar_relatorio(tree, entry_data_inicial, entry_data_final, entry_usuario):
    conn = sqlite3.connect("saracaFarma.db")
    cursor = conn.cursor()

    data_inicial = entry_data_inicial.get().strip()
    data_final = entry_data_final.get().strip()
    usuario = entry_usuario.get().strip()

    query = """
        SELECT codigo_barras, lote, tipo, quantidade, data, id_usuario
        FROM MovimentacaoEstoque
        WHERE 1=1
    """
    params = []

    if data_inicial and data_final:
        query += " AND data BETWEEN ? AND ?"
        params.extend([data_inicial, data_final])

    if usuario:
        query += " AND id_usuario = ?"
        params.append(usuario)

    query += " ORDER BY data"

    cursor.execute(query, params)
    resultados = cursor.fetchall()

    # Limpar Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Ajustar colunas para relatório detalhado
    tree["columns"] = ("codigo_barras", "lote", "tipo", "quantidade", "data", "id_usuario")
    for col in tree["columns"]:
        tree.heading(col, text=col)

    # Inserir resultados
    for row in resultados:
        tree.insert("", "end", values=row)

    conn.close()

def tela_relatorio():
    janela = tk.Toplevel()
    janela.title("Relatório de Movimentações")

    tk.Label(janela, text="Data Inicial (YYYY-MM-DD)").grid(row=0, column=0)
    entry_data_inicial = tk.Entry(janela)
    entry_data_inicial.grid(row=0, column=1)

    tk.Label(janela, text="Data Final (YYYY-MM-DD)").grid(row=1, column=0)
    entry_data_final = tk.Entry(janela)
    entry_data_final.grid(row=1, column=1)

    tk.Label(janela, text="Usuário (ID)").grid(row=2, column=0)
    entry_usuario = tk.Entry(janela)
    entry_usuario.grid(row=2, column=1)

    tree = ttk.Treeview(janela, show="headings")
    tree.grid(row=4, column=0, columnspan=2)

    tk.Button(
        janela,
        text="Consultar Relatório",
        command=lambda: consultar_relatorio(tree, entry_data_inicial, entry_data_final, entry_usuario)
    ).grid(row=3, column=0, columnspan=2)

    tk.Button(
        janela,
        text="Consultar Saldo",
        command=lambda: consultar_saldo(tree)
    ).grid(row=5, column=0, columnspan=2)


# Função principal para montar a tela de estoque
def tela_estoque(perfil):
    # Cria a janela principal da tela de estoque
    janela = tk.Tk()
    janela.title("Controle de Estoque")
    janela.state("zoomed")  # Abre a janela maximizada
    janela.configure(bg="#cce6ff")#Define a cor de fundo da janela
    #Barra superior azul escuro
    barra = tk.Frame(janela, bg="#0066cc", height=50)
    barra.pack(fill="x")
    tk.Label(barra, text="Controle de Estoque - SaracaFarma", fg="white", bg="#0066cc", font=("Segoe UI", 16, "bold")).pack(pady=10)

    # Frame superior com botões
    frame_top = tk.Frame(janela, bg="#cce6ff")
    frame_top.pack(fill="x", padx=10, pady=5)

    # Treeview central para listar os produtos
    colunas = (
        "Código de Barras", "Nome", "Categoria", "Apresentação", "Dosagem", "Fabricante",
    "Lote", "Quantidade", "Validade", "Preço"
    )
    tree = ttk.Treeview(janela, columns=colunas, show="headings")

    # Configura os títulos das colunas
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Label inferior para mensagens de status
    status_label = tk.Label(janela, text="", anchor="w", fg="blue")
    status_label.pack(fill="x", padx=10, pady=5)

    # Botões principais
    btn_atualizar = tk.Button(frame_top, text="Atualizar Estoque",
                              command=lambda: consultar_estoque(tree, status_label))
    btn_atualizar.pack(side="left", padx=5)

     # Botão Entrada de Estoque com submenu
    menu_entrada = tk.Menu(janela, tearoff=0)
    menu_entrada.add_command(label="Cadastro Individual",
                             command=lambda: [cadastrar_produto(perfil), consultar_estoque(tree, status_label)])
    menu_entrada.add_command(label="Cadastro via Fornecedor",
                             command=lambda: [cadastrar_produtos_fornecedor(perfil), consultar_estoque(tree, status_label)])

    btn_entrada = ttk.Menubutton(frame_top, text="Entrada de Estoque", menu=menu_entrada)
    btn_entrada.pack(side="left", padx=5)

    btn_baixa = ttk.Button(frame_top, text="Baixa de Estoque",
                       command=lambda: baixa_estoque(tree, status_label, perfil))
    btn_baixa.pack(side="left", padx=5)

    btn_relatorios = tk.Button(frame_top, text="Relatórios",
                               command=lambda: status_label.config(text="Função de relatórios ainda não implementada", fg="orange"))
    btn_relatorios.pack(side="left", padx=5)

    # Inicia a janela
    janela.mainloop()



