from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import csv
import uuid
from datetime import date
from db import conexao, cursor

def normalizar_data(data_str):
    formatos = ["%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y"]
    for fmt in formatos:
        try:
            dt = datetime.strptime(data_str, fmt)
            return dt.strftime("%Y-%m-%d")  # padrão único
        except ValueError:
            continue
    raise ValueError("Formato de data inválido")

# --- CADASTRO INDIVIDUAL ---
def cadastrar_produto(perfil):
    janela = tk.Toplevel()
    janela.title("Cadastro de Produto")
    janela.state("zoomed")  # abre maximizada
    janela.configure(bg="#cce6ff")

    # --- Campos da interface ---
    ttk.Label(janela, text="Código de Barras:").pack(pady=5)
    entry_codigo = ttk.Entry(janela, width=40); entry_codigo.pack(pady=5)
    entry_codigo.pack(pady=5)
    entry_codigo.bind("<Return>", lambda event: buscar_produto_por_codigo())  # busca ao pressionar Enter

    ttk.Label(janela, text="Nome:").pack(pady=5)
    entry_nome = ttk.Entry(janela, width=40); entry_nome.pack(pady=5)

    ttk.Label(janela, text="Categoria:").pack(pady=5)
    combo_categoria = ttk.Combobox(janela, values=["Medicamento", "Armarinho"], state="readonly")
    combo_categoria.pack(pady=5)

    ttk.Label(janela, text="Apresentação:").pack(pady=5)
    entry_apresentacao = ttk.Entry(janela, width=40); entry_apresentacao.pack(pady=5)

    ttk.Label(janela, text="Dosagem:").pack(pady=5)
    entry_dosagem = ttk.Entry(janela, width=40); entry_dosagem.pack(pady=5)

    ttk.Label(janela, text="Fabricante:").pack(pady=5)
    entry_fabricante = ttk.Entry(janela, width=40); entry_fabricante.pack(pady=5)

    ttk.Label(janela, text="Lote (opcional):").pack(pady=5)
    entry_lote = ttk.Entry(janela, width=40); entry_lote.pack(pady=5)

    ttk.Label(janela, text="Validade (AAAA-MM-DD):").pack(pady=5)
    entry_validade = ttk.Entry(janela, width=40); entry_validade.pack(pady=5)

    ttk.Label(janela, text="Preço:").pack(pady=5)
    entry_preco = ttk.Entry(janela, width=40); entry_preco.pack(pady=5)

    ttk.Label(janela, text="Quantidade:").pack(pady=5)
    entry_quantidade = ttk.Entry(janela, width=40); entry_quantidade.pack(pady=5)

    status_label = ttk.Label(janela, text="", foreground="green")
    status_label.pack(pady=10)


    # --- Funções (agora os campos já existem) ---
    def buscar_produto_por_codigo():
        codigo = entry_codigo.get().strip()
        if not codigo:
            status_label.config(text=f"Informe o código de barras.", foreground="green")
            return
        cursor.execute("SELECT * FROM Produto WHERE codigo_barras = ?", (codigo,))
        produto = cursor.fetchone()
        

        if produto:
            entry_nome.delete(0, tk.END); entry_nome.insert(0, produto[1])
            combo_categoria.set(produto[2])
            entry_apresentacao.delete(0, tk.END); entry_apresentacao.insert(0, produto[3])
            entry_dosagem.delete(0, tk.END); entry_dosagem.insert(0, produto[4])
            entry_fabricante.delete(0, tk.END); entry_fabricante.insert(0, produto[5])
            status_label.config(text=f"Produto encontrado. Informe os dados do lote.", foreground="green")

        else:
            status_label.config(text=f"Produto não encontrado. Preencha todos os campos.", foreground="green")


    def salvar_produto():
     try:
        preco = float(entry_preco.get().replace(",", "."))
        quantidade = int(entry_quantidade.get())
     except ValueError:
        status_label.config(text="Erro: preço ou quantidade inválidos.", foreground="red")
        return

     codigo = entry_codigo.get().strip()
     nome = entry_nome.get().strip()
     categoria = combo_categoria.get().strip()
     apresentacao = entry_apresentacao.get().strip()
     dosagem = entry_dosagem.get().strip()
     fabricante = entry_fabricante.get().strip()
     data_atual = date.today().strftime("%Y-%m-%d")
     try:
      validade = normalizar_data(entry_validade.get().strip())
     except ValueError:
      status_label.config(text="Erro: formato de data inválido.", foreground="red")
      return
     lote = entry_lote.get().strip()

     if not lote:
        lote = "AUTO-" + str(uuid.uuid4())[:8]


     try:
        cursor.execute("SELECT * FROM Produto WHERE codigo_barras = ?", (codigo,))
        produto = cursor.fetchone()
        if not produto:
            cursor.execute("""
                INSERT INTO Produto (codigo_barras, nome, categoria, apresentacao, dosagem, fabricante)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (codigo, nome, categoria, apresentacao, dosagem, fabricante))

        cursor.execute("""
            INSERT INTO LoteProduto (codigo_barras, lote, quantidade, validade, preco)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo, lote, quantidade, validade, preco))

        cursor.execute("""
            INSERT INTO MovimentacaoEstoque (codigo_barras, lote, tipo, quantidade, data, id_usuario)
            VALUES (?, ?, 'entrada', ?, ?, ?)
        """, (codigo, lote, quantidade, data_atual, perfil))

        conexao.commit()

        # mostra mensagem na tela
        status_label.config(text=f"Produto e lote cadastrados! Lote: {lote}", foreground="green")

        # limpa os campos
        entry_codigo.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        combo_categoria.set("")
        entry_apresentacao.delete(0, tk.END)
        entry_dosagem.delete(0, tk.END)
        entry_fabricante.delete(0, tk.END)
        entry_lote.delete(0, tk.END)
        entry_validade.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)

     except Exception as e:
        status_label.config(text=f"Erro ao salvar: {e}", foreground="red")
     finally:
        conexao.close()


    # --- Botões ---
    ttk.Button(janela, text="Buscar Produto", command=buscar_produto_por_codigo).pack(pady=5)
    ttk.Button(janela, text="Salvar", command=salvar_produto).pack(pady=20)

# --- CADASTRO EM LOTE VIA TREEVIEW ---
def cadastrar_produtos_treeview(perfil):
    janela = tk.Toplevel()
    janela.title("Cadastro em Lote - Treeview")
    janela.state("zoomed")  # abre maximizada
    janela.configure(bg="#cce6ff")

    # --- Formulário de entrada ---
    form_frame = tk.Frame(janela, bg="#cce6ff")
    form_frame.pack(fill="x", pady=10)

    labels = [
        "Código de Barras", "Nome", "Categoria", "Apresentação", "Dosagem",
        "Fabricante", "Validade (AAAA-MM-DD)", "Preço", "Quantidade", "Lote"
    ]
    entries = {}

    for i, label in enumerate(labels):
        ttk.Label(form_frame, text=label+":").grid(row=i, column=0, sticky="e", padx=5, pady=3)
        if label == "Categoria":
           entry = ttk.Combobox(
              form_frame,
              values=["Medicamento", "Armarinho", "Cosmético", "Perfume", "Higiene"],
              state="readonly",
             width=30
            )
        else:
            entry = ttk.Entry(form_frame, width=32)
        entry.grid(row=i, column=1, padx=5, pady=3)
        entries[label] = entry

    # --- Treeview ---
    colunas = ("codigo_barras", "nome", "categoria", "apresentacao", "dosagem", "fabricante", "validade", "preco", "quantidade", "lote")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=100)

    tree.pack(fill="both", expand=True, pady=10)

    # --- Label de status ---
    status_label = ttk.Label(janela, text="", foreground="green", background="#cce6ff")
    status_label.pack(pady=5)

    # --- Funções ---
    def buscar_produto_por_codigo():
        codigo = entries["Código de Barras"].get().strip()
        if not codigo:
            status_label.config(text="Informe o código de barras.", foreground="red")
            return
        
        cursor.execute("SELECT * FROM Produto WHERE codigo_barras = ?", (codigo,))
        produto = cursor.fetchone()
        

        if produto:
            entries["Nome"].delete(0, tk.END); entries["Nome"].insert(0, produto[1])
            entries["Categoria"].set(produto[2])
            entries["Apresentação"].delete(0, tk.END); entries["Apresentação"].insert(0, produto[3])
            entries["Dosagem"].delete(0, tk.END); entries["Dosagem"].insert(0, produto[4])
            entries["Fabricante"].delete(0, tk.END); entries["Fabricante"].insert(0, produto[5])
            status_label.config(text="Produto encontrado. Informe os dados do lote.", foreground="green")
        else:
            status_label.config(text="Produto não encontrado. Preencha todos os campos.", foreground="red")

    def adicionar_produto():
        try:
            preco = float(entries["Preço"].get().replace(",", "."))
            quantidade = int(entries["Quantidade"].get())
        except ValueError:
            status_label.config(text="Erro: preço ou quantidade inválidos.", foreground="red")
            return


        try:
         validade = normalizar_data(entries["Validade (AAAA-MM-DD)"].get().strip())
        except ValueError:
         status_label.config(text="Erro: formato de data inválido.", foreground="red")
         return

        valores = (
            entries["Código de Barras"].get(),
            entries["Nome"].get(),
            entries["Categoria"].get(),
            entries["Apresentação"].get(),
            entries["Dosagem"].get(),
            entries["Fabricante"].get(),
            validade,
            preco,
            quantidade,
            entries["Lote"].get() if entries["Lote"].get() else "AUTO-" + str(uuid.uuid4())[:8]
        )

        if not valores[0] or not valores[1] or not valores[2]:
            status_label.config(text="Preencha os campos obrigatórios!", foreground="red")
            return
        
        

        tree.insert("", tk.END, values=valores)

        # limpa os campos
        for entry in entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)

        status_label.config(text="Produto adicionado à lista.", foreground="green")

    def salvar_todos():
        erros = []
        for item in tree.get_children():
            valores = tree.item(item)["values"]
            try:
                codigo, nome, categoria, apresentacao, dosagem, fabricante, validade, preco, quantidade, lote = valores

                # cadastra produto se não existir
                cursor.execute("SELECT * FROM Produto WHERE codigo_barras = ?", (codigo,))
                produto = cursor.fetchone()
                if not produto:
                    cursor.execute("""
                        INSERT INTO Produto (codigo_barras, nome, categoria, apresentacao, dosagem, fabricante)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (codigo, nome, categoria, apresentacao, dosagem, fabricante))

                # cadastra lote
                cursor.execute("""
                    INSERT INTO LoteProduto (codigo_barras, lote, quantidade, validade, preco)
                    VALUES (?, ?, ?, ?, ?)
                """, (codigo, lote, int(quantidade), validade, float(preco)))
                cursor.execute("""
                    INSERT INTO MovimentacaoEstoque (codigo_barras, lote, tipo, quantidade, data, id_usuario)
                    VALUES (?, ?, 'entrada', ?, ?, ?)
                """, (codigo, lote, int(quantidade), date.today(), perfil))

            except Exception as e:
                erros.append(f"{nome}: {e}")

       

        if erros:
            status_label.config(text=f"Erros ao salvar: {', '.join(erros)}", foreground="red")
        else:
            status_label.config(text="Todos os produtos foram cadastrados com sucesso!", foreground="green")
            # limpa a treeview após salvar
            for item in tree.get_children():
             tree.delete(item)


    def editar_produto():
     selecionado = tree.selection()
     if not selecionado:
        status_label.config(text="Selecione um produto para editar.", foreground="red")
        return
     item = selecionado[0]
     valores = tree.item(item)["values"]

     # Janela de edição
     edit_win = tk.Toplevel(janela)
     edit_win.title("Editar Produto")
     edit_win.geometry("400x500")
     edit_win.configure(bg="#cce6ff")

     novos_valores = []
     for i, campo in enumerate(labels):
         ttk.Label(edit_win, text=campo).grid(row=i, column=0, padx=5, pady=5)
         entry = ttk.Entry(edit_win, width=30)
         entry.insert(0, valores[i])
         entry.grid(row=i, column=1, padx=5, pady=5)
         novos_valores.append(entry)

     def salvar_edicao():
        atualizados = [e.get() for e in novos_valores]
        tree.item(item, values=atualizados)
        edit_win.destroy()
        status_label.config(text="Produto atualizado na lista.", foreground="green")

     ttk.Button(edit_win, text="Salvar Alterações", command=salvar_edicao).grid(row=len(labels), columnspan=2, pady=10)
     
    # --- Botões ---
    botoes_frame = tk.Frame(janela, bg="#cce6ff")
    botoes_frame.pack(fill="x", pady=10)

    ttk.Button(botoes_frame, text="Buscar Produto", command=buscar_produto_por_codigo).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="Adicionar Produto", command=adicionar_produto).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="Salvar Todos", command=salvar_todos).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="Editar Produto", command=editar_produto).pack(side="left", padx=10)

        # --- Integração com leitor de código de barras ---
    # Quando o leitor enviar ENTER, chama a busca automaticamente
    entries["Código de Barras"].bind("<Return>", lambda event: buscar_produto_por_codigo())

#--- CADASTRO EM LOTE VIA CSV DO FORNECEDOR (COM PREÇO DE CUSTO E VENDA) ---
def cadastrar_produtos_fornecedor(perfil):
    janela = tk.Toplevel()
    janela.title("Cadastro via Fornecedor - CSV")
    janela.state("zoomed")

    status_label = ttk.Label(janela, text="", foreground="green")
    status_label.pack(pady=5)

    # --- Treeview com coluna extra de preço de custo e preço de venda ---
    colunas = ("codigo_barras", "nome", "categoria", "apresentacao", "dosagem",
               "fabricante", "lote", "quantidade", "validade", "preco_custo", "preco_venda")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True, pady=10)

    # --- Importar CSV do fornecedor ---
    def importar_csv():
        arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not arquivo:
            return
        try:
            with open(arquivo, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  # pula cabeçalho
                for row in reader:
                    if not row or all(c.strip() == "" for c in row):
                        continue
                    # fornecedor manda preco_custo, preco_venda inicial = preco_custo
                    row.append(row[-1])  # duplica preco_custo como preco_venda
                    tree.insert("", tk.END, values=row)

            status_label.config(text="Produtos importados do fornecedor!", foreground="green")

            #---Força o foco de volta para a janela de cadastro---
            janela.lift()  # traz a janela para frente
            janela.focus_force()

        except Exception as e:
            status_label.config(text=f"Erro ao importar CSV: {e}", foreground="red")

    def editar_produto():
        selecionado = tree.selection()
        if not selecionado:
            status_label.config(text="Selecione um produto para editar.", foreground="red")
            return
        item = selecionado[0]
        valores = tree.item(item)["values"]

        # Janela de edição
        edit_win = tk.Toplevel(janela)
        edit_win.title("Editar Produto Fornecedor")
        edit_win.geometry("500x600")
        edit_win.configure(bg="#cce6ff")

        novos_valores = []
        for i, col in enumerate(colunas):
            ttk.Label(edit_win, text=col.capitalize()).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(edit_win, width=30)
            entry.insert(0, valores[i])
            entry.grid(row=i, column=1, padx=5, pady=5)
            novos_valores.append(entry)

        def salvar_edicao():
            atualizados = [e.get() for e in novos_valores]
            tree.item(item, values=atualizados)
            edit_win.destroy()
            status_label.config(text="Produto atualizado na lista.", foreground="green")

        ttk.Button(edit_win, text="Salvar Alterações", command=salvar_edicao).grid(row=len(colunas), columnspan=2, pady=10)


    # --- Aplicar margem de lucro ---
    def definir_margem():
        # Janela para o usuário digitar a porcentagem
        margem_win = tk.Toplevel(janela)
        margem_win.title("Definir Margem de Lucro")
        margem_win.geometry("300x150")
        margem_win.configure(bg="#cce6ff")

        ttk.Label(margem_win, text="Informe a margem (%)").pack(pady=10)
        entry_margem = ttk.Entry(margem_win, width=10)
        entry_margem.pack(pady=5)

        def aplicar():
            try:
                valor = float(entry_margem.get())
                for item in tree.get_children():
                    valores = list(tree.item(item)["values"])
                    preco_custo = float(str(valores[-2]).replace(",", ".").strip())
                    preco_venda = preco_custo * (1 + valor/100)
                    valores[-1] = round(preco_venda, 2)
                    tree.item(item, values=valores)
                status_label.config(text=f"Margem de {valor}% aplicada com sucesso!", foreground="green")
                margem_win.destroy()
            except Exception as e:
                status_label.config(text=f"Erro ao aplicar margem: {e}", foreground="red")

        ttk.Button(margem_win, text="Aplicar", command=aplicar).pack(pady=10)


    # --- Salvar no banco (sem preço de custo) ---
    def salvar_todos():
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        erros = []
        for item in tree.get_children():
            valores = tree.item(item)["values"]
            try:
                (
                    codigo_barras, nome, categoria, apresentacao,
                    dosagem, fabricante, lote, quantidade,
                    validade, preco_custo, preco_venda
                ) = valores

                codigo_barras = str(codigo_barras).strip()
                nome = str(nome).strip()
                categoria = str(categoria).strip()
                apresentacao = str(apresentacao).strip()
                dosagem = str(dosagem).strip()
                fabricante = str(fabricante).strip()
                lote = str(lote).strip()
                validade = str(validade).strip()
                quantidade = int(str(quantidade).strip()) if quantidade else 0
                preco_venda = float(str(preco_venda).replace(",", ".").strip()) if preco_venda else 0.0

                # cadastra produto se não existir
                cursor.execute("SELECT * FROM Produto WHERE codigo_barras = ?", (codigo_barras,))
                produto = cursor.fetchone()
                if not produto:
                    cursor.execute("""
                        INSERT INTO Produto (codigo_barras, nome, categoria, apresentacao, dosagem, fabricante)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (codigo_barras, nome, categoria, apresentacao, dosagem, fabricante))

                # cadastra lote (usando preco_venda, não preco_custo)
                cursor.execute("""
                    INSERT INTO LoteProduto (codigo_barras, lote, quantidade, validade, preco)
                    VALUES (?, ?, ?, ?, ?)
                """, (codigo_barras, lote, quantidade, validade, preco_venda))
                cursor.execute("""
                    INSERT INTO MovimentacaoEstoque (codigo_barras, lote, tipo, quantidade, data, id_usuario)
                    VALUES (?, ?, 'entrada', ?, ?, ?)
                """, (codigo_barras, lote, quantidade, date.today(), perfil))

            except Exception as e:
                erros.append(f"{nome}: {e}")

        conn.commit()
        conn.close()

        if erros:
            status_label.config(text=f"Erros ao salvar: {', '.join(erros)}", foreground="red")
        else:
            status_label.config(text="Todos os produtos foram cadastrados com sucesso!", foreground="green")
            for item in tree.get_children():
                tree.delete(item)

    # --- Botões ---
    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(fill="x", pady=10)

    ttk.Button(botoes_frame, text="Selecionar Arquivo Fornecedor", command=importar_csv).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="Salvar Todos", command=salvar_todos).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="Editar Produto", command=editar_produto).pack(side="left", padx=10)

    # Botões para aplicar margem
    ttk.Button(botoes_frame, text="Definir Margem de Lucro", command=definir_margem).pack(side="left", padx=10)


def normalizar_preco(valor):
    try:
        valor = valor.replace(",", ".")
        partes = valor.split(".")
        if len(partes) == 1:  # só inteiro
            return f"{int(partes[0])}.00"
        elif len(partes) == 2:
            if len(partes[1]) == 1:  # apenas uma casa decimal
                return f"{partes[0]}.{partes[1]}0"
            elif len(partes[1]) == 2:  # já está correto
                return f"{partes[0]}.{partes[1]}"
            else:
                raise ValueError("Preço inválido. Use o formato 5.20")
        else:
            raise ValueError("Preço inválido. Use o formato 5.20")
    except:
        raise ValueError("Preço inválido. Use o formato 5.20")

def validar_quantidade(valor):
    try:
        valor = valor.replace(",", ".")
        if "." in valor:  # não aceita decimais
            raise ValueError("Quantidade inválida. Use apenas números inteiros (ex: 10)")
        return int(valor)
    except:
        raise ValueError("Quantidade inválida. Use apenas números inteiros (ex: 10)")

