import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from clinte import cadastrar_cliente
from db import conexao, cursor

def abrir_funcoes_admin(parent=None):
    if parent and parent.winfo_exists():
        parent.withdraw()

    admin = tk.Toplevel(parent)
    admin.title("Funções Administrativas")
    admin.geometry("420x300")
    admin.configure(bg="#cce6ff")

    def fechar_admin():
        if parent and parent.winfo_exists():
            parent.deiconify()
        admin.destroy()

    admin.protocol("WM_DELETE_WINDOW", fechar_admin)

    barra = tk.Frame(admin, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Funções Administrativas", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(admin, bg="#cce6ff")
    frame.pack(pady=30)

    ttk.Button(frame, text="Cadastrar novo usuário", command=lambda: abrir_cadastro_usuario(admin)).pack(pady=10)
    ttk.Button(frame, text="Alterar dados do admin", command=lambda: alterar_admin(admin)).pack(pady=10)
    ttk.Button(frame, text="Cadastrar novo cliente", command=lambda: cadastrar_cliente(admin)).pack(pady=10)

def abrir_cadastro_usuario(parent=None):
    if parent and parent.winfo_exists():
        parent.withdraw()

    cadastro = tk.Toplevel(parent)
    cadastro.title("Cadastro de Usuário")
    cadastro.geometry("420x400")
    cadastro.configure(bg="#cce6ff")

    def fechar_cadastro():
        if parent and parent.winfo_exists():
            parent.deiconify()
        cadastro.destroy()

    cadastro.protocol("WM_DELETE_WINDOW", fechar_cadastro)

    barra = tk.Frame(cadastro, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Cadastro de Usuário", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(cadastro, bg="#cce6ff")
    frame.pack(pady=20)

    ttk.Label(frame, text="Nome:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_nome = ttk.Entry(frame, width=28)
    entry_nome.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Login:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_login = ttk.Entry(frame, width=28)
    entry_login.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Senha:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_senha_cad = ttk.Entry(frame, width=28, show="*")
    entry_senha_cad.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Perfil (admin/funcionario):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_perfil = ttk.Entry(frame, width=28)
    entry_perfil.grid(row=3, column=1, padx=10, pady=10)

    def salvar():
        cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
                       (entry_nome.get(), entry_login.get(), entry_senha_cad.get(), entry_perfil.get()))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        cadastro.destroy()

    ttk.Button(frame, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=2, pady=20)

def alterar_admin(parent=None):
    if parent and parent.winfo_exists():
        parent.withdraw()

    janela = tk.Toplevel(parent)
    janela.title("Alterar dados do Admin")
    janela.geometry("420x300")
    janela.configure(bg="#cce6ff")

    def fechar_alteracao():
        if parent and parent.winfo_exists():
            parent.deiconify()
        janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", fechar_alteracao)

    barra = tk.Frame(janela, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Alterar dados do Admin", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(janela, bg="#cce6ff")
    frame.pack(pady=20)

    ttk.Label(frame, text="Novo nome:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_nome = ttk.Entry(frame, width=28)
    entry_nome.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(frame, text="Nova senha:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_senha = ttk.Entry(frame, width=28, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    def salvar_alteracao():
        cursor.execute("UPDATE Usuario SET nome=?, senha=? WHERE login='admin'",
                       (entry_nome.get(), entry_senha.get()))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Dados do admin atualizados!")
        janela.destroy()

    ttk.Button(frame, text="Salvar", command=salvar_alteracao).grid(row=2, column=0, columnspan=2, pady=20)

    def salvar():
        cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
                       (entry_nome.get(), entry_login.get(), entry_senha_cad.get(), entry_perfil.get()))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        cadastro.destroy()

    # Aqui estava o erro: faltava fechar o parêntese
    ttk.Button(frame, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=2, pady=20)
