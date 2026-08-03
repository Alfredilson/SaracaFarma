import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from db import conexao, cursor
from ui_theme import apply_theme, styled_button, maximize_window, restore_window, remember_window_state, PRIMARY_BG, HEADER_BG, HEADER_FG, SECONDARY_BG, TREE_ALT_BG, TEXT_PRIMARY_FG, TREE_SEL_BG, BUTTON_TEXT_FG, ROW_BG, TREE_BG


class ClienteCadastro:
    def __init__(self, master=None, cliente_id=None, on_saved=None, on_close=None):
        self.master = master
        self.cliente_id = cliente_id
        self.on_saved = on_saved
        self.on_close = on_close
        self.janela = tk.Toplevel(master)
        self.janela.title("Editar Cliente" if cliente_id else "Cadastro de Cliente")
        self.janela.geometry("420x380")
        apply_theme(self.janela)
        maximize_window(self.janela)

        self._build_interface()
        self.janela.protocol("WM_DELETE_WINDOW", self._on_close)
        if self.cliente_id:
            self._carregar_cliente()

    def _build_interface(self):
        barra = tk.Frame(self.janela, bg=HEADER_BG, height=45)
        barra.pack(fill="x")
        tk.Label(barra, text="Editar Cliente" if self.cliente_id else "Cadastro de Cliente", fg=HEADER_FG, bg=HEADER_BG, font=("Segoe UI", 14, "bold")).pack(pady=5)

        frame = tk.Frame(self.janela, bg=PRIMARY_BG)
        frame.pack(pady=(20, 10), padx=30, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

        tk.Label(frame, text="Nome:", bg=PRIMARY_BG).grid(row=0, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_nome = ttk.Entry(frame)
        self.entry_nome.grid(row=0, column=1, pady=10, sticky="ew")

        tk.Label(frame, text="CPF:", bg=PRIMARY_BG).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_cpf = ttk.Entry(frame)
        self.entry_cpf.grid(row=1, column=1, pady=10, sticky="ew")

        tk.Label(frame, text="Telefone:", bg=PRIMARY_BG).grid(row=2, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_telefone = ttk.Entry(frame)
        self.entry_telefone.grid(row=2, column=1, pady=10, sticky="ew")

        tk.Label(frame, text="Email:", bg=PRIMARY_BG).grid(row=3, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_email = ttk.Entry(frame)
        self.entry_email.grid(row=3, column=1, pady=10, sticky="ew")

        tk.Label(frame, text="Endereço:", bg=PRIMARY_BG).grid(row=4, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_endereco = ttk.Entry(frame)
        self.entry_endereco.grid(row=4, column=1, pady=10, sticky="ew")

        self.permite_fiado_var = tk.IntVar(value=0)
        ttk.Checkbutton(frame, text="Permite fiado", variable=self.permite_fiado_var, onvalue=1, offvalue=0).grid(row=5, column=0, columnspan=2, sticky="w", pady=10)

        tk.Label(frame, text="Limite de fiado (R$):", bg=PRIMARY_BG).grid(row=6, column=0, sticky="w", pady=10, padx=(0, 12))
        self.entry_limite_fiado = ttk.Entry(frame)
        self.entry_limite_fiado.grid(row=6, column=1, pady=10, sticky="ew")

        spacer = tk.Frame(self.janela, bg=PRIMARY_BG)
        spacer.pack(fill="both", expand=True)

        button_frame = tk.Frame(self.janela, bg=PRIMARY_BG, bd=1, relief="raised")
        button_frame.pack(fill="x", side="bottom")

        self.btn_salvar = styled_button(button_frame, text="Atualizar" if self.cliente_id else "Salvar", kind="secondary", command=self.salvar_cliente)
        self.btn_salvar.pack(side="right", padx=12, pady=10, ipadx=10)
        styled_button(button_frame, text="Voltar", kind="danger", command=self._on_close).pack(side="right", padx=12, pady=10, ipadx=10)

    def _on_close(self):
        if self.on_close:
            try:
                self.on_close()
            except Exception:
                pass
        if self.master and self.master.winfo_exists():
            try:
                restore_window(self.master)
            except Exception:
                pass
        self.janela.destroy()

    def _carregar_cliente(self):
        cursor.execute("SELECT nome, cpf, telefone, email, endereco, permite_fiado, limite_fiado FROM Cliente WHERE id_cliente = ?", (self.cliente_id,))
        cliente = cursor.fetchone()
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            self.janela.destroy()
            return

        nome, cpf, telefone, email, endereco, permite_fiado, limite_fiado = cliente
        self.entry_nome.insert(0, nome)
        self.entry_cpf.insert(0, cpf)
        self.entry_telefone.insert(0, telefone)
        self.entry_email.insert(0, email)
        self.entry_endereco.insert(0, endereco)
        self.permite_fiado_var.set(permite_fiado or 0)
        self.entry_limite_fiado.insert(0, str(limite_fiado or 0.0))

    def salvar_cliente(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        endereco = self.entry_endereco.get().strip()
        permite_fiado = int(self.permite_fiado_var.get())
        limite_fiado_text = self.entry_limite_fiado.get().strip() or "0"

        if not nome or not cpf:
            messagebox.showwarning("Erro", "Nome e CPF são obrigatórios!")
            return

        try:
            limite_fiado = float(limite_fiado_text.replace(",", "."))
        except ValueError:
            messagebox.showwarning("Erro", "Limite de fiado inválido!")
            return

        try:
            if self.cliente_id:
                cursor.execute("SELECT id_cliente FROM Cliente WHERE cpf = ? AND id_cliente <> ?", (cpf, self.cliente_id))
                if cursor.fetchone():
                    messagebox.showerror("Erro", "CPF já cadastrado para outro cliente!")
                    return

                cursor.execute("""
                    UPDATE Cliente
                       SET nome = ?, cpf = ?, telefone = ?, email = ?, endereco = ?, permite_fiado = ?, limite_fiado = ?
                     WHERE id_cliente = ?
                """, (nome, cpf, telefone, email, endereco, permite_fiado, limite_fiado, self.cliente_id))
                conexao.commit()
                messagebox.showinfo("Sucesso", f"Cliente {nome} atualizado com sucesso.")
                # Se um callback on_saved foi fornecido (ex.: listagem), atualiza a lista
                if self.on_saved:
                    try:
                        self.on_saved()
                    except Exception:
                        pass
                # Fecha a janela de edição e restaura a janela pai
                try:
                    self._on_close()
                except Exception:
                    pass
            else:
                cursor.execute("""
                    INSERT INTO Cliente (nome, cpf, telefone, email, endereco, permite_fiado, limite_fiado)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (nome, cpf, telefone, email, endereco, permite_fiado, limite_fiado))
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
        self.permite_fiado_var.set(0)
        self.entry_limite_fiado.delete(0, tk.END)


def cadastrar_cliente(master=None):
    if master and master.winfo_exists():
        remember_window_state(master)
        master.withdraw()
    ClienteCadastro(master, on_close=lambda: restore_window(master) if master and master.winfo_exists() else None)


def editar_cliente(master=None, cliente_id=None, on_saved=None):
    if cliente_id is None:
        return
    if master and master.winfo_exists():
        remember_window_state(master)
        master.withdraw()
    ClienteCadastro(master, cliente_id, on_saved=on_saved, on_close=lambda: restore_window(master) if master and master.winfo_exists() else None)


def listar_clientes(master=None):
    if master and master.winfo_exists():
        remember_window_state(master)
        master.withdraw()

    janela = tk.Toplevel(master)
    janela.title("Lista de Clientes")
    janela.geometry("760x420")
    apply_theme(janela)
    maximize_window(janela)

    def fechar_e_voltar():
        if master and master.winfo_exists():
            restore_window(master)
        janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", fechar_e_voltar)

    barra = tk.Frame(janela, bg=HEADER_BG, height=45)
    barra.pack(fill="x")
    tk.Label(barra, text="Lista de Clientes", fg=HEADER_FG, bg=HEADER_BG, font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(janela, bg=PRIMARY_BG)
    frame.pack(fill="both", expand=True, padx=30, pady=20)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    style = ttk.Style(janela)
    style.configure("Cliente.Treeview", background=TREE_ALT_BG, foreground=TEXT_PRIMARY_FG, fieldbackground=TREE_ALT_BG)
    style.map("Cliente.Treeview", background=[("selected", TREE_SEL_BG)], foreground=[("selected", BUTTON_TEXT_FG)])

    colunas = ("id_cliente", "nome", "cpf", "telefone", "email", "endereco", "permite_fiado", "limite_fiado")
    tree = ttk.Treeview(frame, columns=colunas, show="headings", height=14, style="Cliente.Treeview")
    tree.heading("id_cliente", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("cpf", text="CPF")
    tree.heading("telefone", text="Telefone")
    tree.heading("email", text="Email")
    tree.heading("endereco", text="Endereço")
    tree.heading("permite_fiado", text="Fiado")
    tree.heading("limite_fiado", text="Limite R$")

    tree.column("id_cliente", width=80, anchor="center", stretch=True)
    tree.column("nome", width=220, stretch=True)
    tree.column("cpf", width=140, anchor="center", stretch=True)
    tree.column("telefone", width=140, anchor="center", stretch=True)
    tree.column("email", width=180, stretch=True)
    tree.column("endereco", width=180, stretch=True)
    tree.column("permite_fiado", width=80, anchor="center", stretch=True)
    tree.column("limite_fiado", width=110, anchor="center", stretch=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    cursor.execute("SELECT id_cliente, nome, cpf, telefone, email, endereco, permite_fiado, limite_fiado FROM Cliente")
    for idx, cliente in enumerate(cursor.fetchall()):
        tag = "par" if idx % 2 == 0 else "impar"
        cliente_display = list(cliente)
        cliente_display[6] = "Sim" if cliente[6] else "Não"
        cliente_display[7] = f"R$ {cliente[7]:.2f}"
        tree.insert("", "end", values=cliente_display, tags=(tag,))

    tree.tag_configure("par", background=ROW_BG)
    tree.tag_configure("impar", background=TREE_BG)

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
        cursor.execute("SELECT id_cliente, nome, cpf, telefone, email, endereco, permite_fiado, limite_fiado FROM Cliente")
        for idx, cliente in enumerate(cursor.fetchall()):
            tag = "par" if idx % 2 == 0 else "impar"
            cliente_display = list(cliente)
            cliente_display[6] = "Sim" if cliente[6] else "Não"
            cliente_display[7] = f"R$ {cliente[7]:.2f}"
            tree.insert("", "end", values=cliente_display, tags=(tag,))

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

    spacer = tk.Frame(janela, bg=PRIMARY_BG)
    spacer.pack(fill="both", expand=True)

    botao_frame = tk.Frame(janela, bg=PRIMARY_BG, bd=1, relief="raised")
    botao_frame.pack(fill="x", side="bottom")
    btn_excluir = styled_button(botao_frame, text="Excluir", kind="danger", command=excluir_cliente, state="disabled")
    btn_excluir.pack(side="left", padx=12, pady=10, ipadx=10)
    btn_editar = styled_button(botao_frame, text="Atualizar", kind="secondary", command=abrir_edicao, state="disabled")
    btn_editar.pack(side="left", padx=12, pady=10, ipadx=10)
    styled_button(botao_frame, text="Voltar", kind="primary", command=fechar_e_voltar).pack(side="right", padx=12, pady=10)
