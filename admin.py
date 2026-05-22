import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def abrir_funcoes_admin():
    admin = tk.Toplevel()
    admin.title("Funções Administrativas")
    admin.geometry("420x300")
    admin.configure(bg="#cce6ff")

    barra = tk.Frame(admin, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Funções Administrativas", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(admin, bg="#cce6ff")
    frame.pack(pady=30)

    ttk.Button(frame, text="Cadastrar novo usuário", command=abrir_cadastro_usuario).pack(pady=10)
    ttk.Button(frame, text="Alterar dados do admin", command=alterar_admin).pack(pady=10)

def abrir_cadastro_usuario():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro de Usuário")
    cadastro.geometry("420x400")
    cadastro.configure(bg="#cce6ff")

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
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
                       (entry_nome.get(), entry_login.get(), entry_senha_cad.get(), entry_perfil.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        cadastro.destroy()

    ttk.Button(frame, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=2, pady=20)

def alterar_admin():
    janela = tk.Toplevel()
    janela.title("Alterar dados do Admin")
    janela.geometry("420x300")
    janela.configure(bg="#cce6ff")

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
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE Usuario SET nome=?, senha=? WHERE login='admin'",
                       (entry_nome.get(), entry_senha.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Dados do admin atualizados!")
        janela.destroy()

    ttk.Button(frame, text="Salvar", command=salvar_alteracao).grid(row=2, column=0, columnspan=2, pady=20)

    def salvar():
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
                       (entry_nome.get(), entry_login.get(), entry_senha_cad.get(), entry_perfil.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        cadastro.destroy()

    # Aqui estava o erro: faltava fechar o parêntese
    ttk.Button(frame, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=2, pady=20)
