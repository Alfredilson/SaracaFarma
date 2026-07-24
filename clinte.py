import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from db import conexao, cursor


class ClienteCadastro:
    def __init__(self, master=None, cliente_id=None, on_saved=None, on_close=None):
        self.master = master
        self.cliente_id = cliente_id
        self.on_saved = on_saved
        self.on_close = on_close
        self.janela = tk.Toplevel(master)
        self.janela.title("Editar Cliente" if cliente_id else "Cadastro de Cliente")
        self.janela.geometry("420x380")
        self.janela.configure(bg="#cce6ff")
        self.janela.state("zoomed")

        self._build_interface()
        self.janela.protocol("WM_DELETE_WINDOW", self._on_close)
        if self.cliente_id:
            self._carregar_cliente()

    def _build_interface(self):
        barra = tk.Frame(self.janela, bg="#0066cc", height=45)
        barra.pack(fill="x")
        tk.Label(barra, text="Editar Cliente" if self.cliente_id else "Cadastro de Cliente", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

        frame = tk.Frame(self.janela, bg="#cce6ff")
        frame.pack(pady=(20, 10), padx=30, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

        tk.Label(frame, text="Nome:", bg="#cce6ff").grid(row=0, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_nome = ttk.Entry(frame)
        self.entry_nome.grid(row=0, column=1, pady=10, sticky="ew")

        tk.Label(frame, text="CPF:", bg="#cce6ff").grid(row=1, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_cpf = ttk.Entry(frame)
        self.entry_cpf.grid(row=1, column=1, pady=10, sticky="ew")

        tk.Label(frame, text="Telefone:", bg="#cce6ff").grid(row=2, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_telefone = ttk.Entry(frame)
        self.entry_telefone.grid(row=2, column=1, pady=10, sticky="ew")

        tk.Label(frame, text="Email:", bg="#cce6ff").grid(row=3, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_email = ttk.Entry(frame)
        self.entry_email.grid(row=3, column=1, pady=10, sticky="ew")

        tk.Label(frame, text="Endereço:", bg="#cce6ff").grid(row=4, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_endereco = ttk.Entry(frame)
        self.entry_endereco.grid(row=4, column=1, pady=10, sticky="ew")

        spacer = tk.Frame(self.janela, bg="#cce6ff")
        spacer.pack(fill="both", expand=True)

        button_frame = tk.Frame(self.janela, bg="#cce6ff", bd=1, relief="raised")
        button_frame.pack(fill="x", side="bottom")

        self.btn_salvar = tk.Button(button_frame, text="Atualizar" if self.cliente_id else "Salvar", bg="#4CAF50", fg="white", command=self.salvar_cliente)
        self.btn_salvar.pack(side="right", padx=12, pady=10, ipadx=10)
        tk.Button(button_frame, text="Voltar", bg="#f44336", fg="white", command=self._on_close).pack(side="right", padx=12, pady=10, ipadx=10)

    def _on_close(self):
        if self.on_close:
            try:
                self.on_close()
            except Exception:
                pass
        if self.master and self.master.winfo_exists():
            try:
                self.master.deiconify()
            except Exception:
                pass
        self.janela.destroy()

    def _carregar_cliente(self):
        cursor.execute("SELECT nome, cpf, telefone, email, endereco FROM Cliente WHERE id_cliente = ?", (self.cliente_id,))
        cliente = cursor.fetchone()
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            self.janela.destroy()
            return

        nome, cpf, telefone, email, endereco = cliente
        self.entry_nome.insert(0, nome)
        self.entry_cpf.insert(0, cpf)
        self.entry_telefone.insert(0, telefone)
        self.entry_email.insert(0, email)
        self.entry_endereco.insert(0, endereco)

    def salvar_cliente(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not nome or not cpf:
            messagebox.showwarning("Erro", "Nome e CPF são obrigatórios!")
            return

        try:
            if self.cliente_id:
                cursor.execute("SELECT id_cliente FROM Cliente WHERE cpf = ? AND id_cliente <> ?", (cpf, self.cliente_id))
                if cursor.fetchone():
                    messagebox.showerror("Erro", "CPF já cadastrado para outro cliente!")
                    return

                cursor.execute("""
                    UPDATE Cliente
                       SET nome = ?, cpf = ?, telefone = ?, email = ?, endereco = ?
                     WHERE id_cliente = ?
                """, (nome, cpf, telefone, email, endereco, self.cliente_id))
                conexao.commit()
                messagebox.showinfo("Sucesso", f"Cliente {nome} atualizado com sucesso.")
            else:
                cursor.execute("""
                    INSERT INTO Cliente (nome, cpf, telefone, email, endereco)
                    VALUES (?, ?, ?, ?, ?)
                """, (nome, cpf, telefone, email, endereco))
                conexao.commit()
                messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado com sucesso.")
                self._limpar_campos()

            if self.on_saved:
                self.on_saved()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado!")

    def _limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)


def cadastrar_cliente(master=None):
    if master and master.winfo_exists():
        master.withdraw()
    ClienteCadastro(master, on_close=lambda: master.deiconify() if master and master.winfo_exists() else None)


def editar_cliente(master=None, cliente_id=None, on_saved=None):
    if cliente_id is None:
        return
    if master and master.winfo_exists():
        master.withdraw()
    ClienteCadastro(master, cliente_id, on_saved=on_saved, on_close=lambda: master.deiconify() if master and master.winfo_exists() else None)


def listar_clientes(master=None):
    if master and master.winfo_exists():
        master.withdraw()

    janela = tk.Toplevel(master)
    janela.title("Lista de Clientes")
    janela.geometry("760x420")
    janela.configure(bg="#cce6ff")
    janela.state("zoomed")

    def fechar_e_voltar():
        if master and master.winfo_exists():
            master.deiconify()
        janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", fechar_e_voltar)

    barra = tk.Frame(janela, bg="#0066cc", height=45)
    barra.pack(fill="x")
    tk.Label(barra, text="Lista de Clientes", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(janela, bg="#cce6ff")
    frame.pack(fill="both", expand=True, padx=30, pady=20)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    style = ttk.Style(janela)
    style.configure("Cliente.Treeview", background="#f7fbff", foreground="black", fieldbackground="#f7fbff")
    style.map("Cliente.Treeview", background=[("selected", "#3399ff")], foreground=[("selected", "white")])

    colunas = ("id_cliente", "nome", "cpf", "telefone", "email", "endereco")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=14, style="Cliente.Treeview")
    tree.heading("id_cliente", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("cpf", text="CPF")
    tree.heading("telefone", text="Telefone")
    tree.heading("email", text="Email")
    tree.heading("endereco", text="Endereço")

    tree.column("id_cliente", width=80, anchor="center", stretch=True)
    tree.column("nome", width=220, stretch=True)
    tree.column("cpf", width=140, anchor="center", stretch=True)
    tree.column("telefone", width=140, anchor="center", stretch=True)
    tree.column("email", width=220, stretch=True)
    tree.column("endereco", width=220, stretch=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    cursor.execute("SELECT id_cliente, nome, cpf, telefone, email, endereco FROM Cliente")
    for idx, cliente in enumerate(cursor.fetchall()):
        tag = "par" if idx % 2 == 0 else "impar"
        tree.insert("", "end", values=cliente, tags=(tag,))

    tree.tag_configure("par", background="#ffffff")
    tree.tag_configure("impar", background="#e8f2ff")

    def obter_cliente_selecionado():
        selecionado = tree.selection()
        if not selecionado:
            return None
        return tree.item(selecionado[0], "values")[0]

    def atualizar_botao_editar(event=None):
        if obter_cliente_selecionado():
            btn_editar.config(state="normal")
        else:
            btn_editar.config(state="disabled")

    def refresh_clientes():
        tree.delete(*tree.get_children())
        cursor.execute("SELECT id_cliente, nome, cpf, telefone, email, endereco FROM Cliente")
        for idx, cliente in enumerate(cursor.fetchall()):
            tag = "par" if idx % 2 == 0 else "impar"
            tree.insert("", "end", values=cliente, tags=(tag,))

    def abrir_edicao():
        cliente_id = obter_cliente_selecionado()
        if not cliente_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para editar.")
            return
        editar_cliente(janela, cliente_id, on_saved=refresh_clientes)

    def excluir_cliente():
        cliente_id = obter_cliente_selecionado()
        if not cliente_id:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
            return

        confirmacao = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este cliente?")
        if not confirmacao:
            return

        try:
            cursor.execute("DELETE FROM Cliente WHERE id_cliente = ?", (cliente_id,))
            conexao.commit()
            for item in tree.get_children():
                if tree.item(item, "values")[0] == cliente_id:
                    tree.delete(item)
                    break
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")
            btn_editar.config(state="disabled")
            btn_excluir.config(state="disabled")
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Não foi possível excluir o cliente.\n{erro}")

    def atualizar_botoes(event=None):
        if obter_cliente_selecionado():
            btn_editar.config(state="normal")
            btn_excluir.config(state="normal")
        else:
            btn_editar.config(state="disabled")
            btn_excluir.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", atualizar_botoes)
    tree.bind("<Double-1>", lambda event: abrir_edicao())

    spacer = tk.Frame(janela, bg="#cce6ff")
    spacer.pack(fill="both", expand=True)

    botao_frame = tk.Frame(janela, bg="#cce6ff", bd=1, relief="raised")
    botao_frame.pack(fill="x", side="bottom")
    btn_excluir = tk.Button(botao_frame, text="Excluir", bg="#f44336", fg="white", command=excluir_cliente, state="disabled")
    btn_excluir.pack(side="left", padx=12, pady=10, ipadx=10)
    btn_editar = tk.Button(botao_frame, text="Atualizar", bg="#4CAF50", fg="white", command=abrir_edicao, state="disabled")
    btn_editar.pack(side="left", padx=12, pady=10, ipadx=10)
    tk.Button(botao_frame, text="Voltar", bg="#0066cc", fg="white", command=fechar_e_voltar).pack(side="right", padx=12, pady=10)
