import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Função para validar login
def validar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    conn = sqlite3.connect("saracaFarma.db")
    cursor = conn.cursor()
    cursor.execute("SELECT perfil FROM Usuario WHERE login=? AND senha=?", (usuario, senha))
    result = cursor.fetchone()
    conn.close()
    if result:
        perfil = result[0]
        messagebox.showinfo("Login", f"Bem-vindo, perfil: {perfil}")
        if perfil == "admin":
            abrir_menu_admin()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")

# Função para salvar novo usuário
def salvar_usuario(nome, login, senha, perfil):
    try:
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
                       (nome, login, senha, perfil))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao cadastrar usuário: {e}")

# Tela de cadastro de usuário
def abrir_cadastro_usuario():
    cadastro = tk.Toplevel(root)
    cadastro.title("Cadastro de Usuário")
    cadastro.configure(bg="#cce6ff")

    barra = tk.Frame(cadastro, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Cadastro de Usuário", fg="white", bg="#0066cc", font=("Arial", 14, "bold")).pack(pady=5)

    tk.Label(cadastro, text="Nome:", bg="#cce6ff", font=("Arial", 12)).pack(pady=5)
    entry_nome = ttk.Entry(cadastro, width=30)
    entry_nome.pack(pady=5)

    tk.Label(cadastro, text="Login:", bg="#cce6ff", font=("Arial", 12)).pack(pady=5)
    entry_login = ttk.Entry(cadastro, width=30)
    entry_login.pack(pady=5)

    tk.Label(cadastro, text="Senha:", bg="#cce6ff", font=("Arial", 12)).pack(pady=5)
    entry_senha_cad = ttk.Entry(cadastro, width=30, show="*")
    entry_senha_cad.pack(pady=5)

    tk.Label(cadastro, text="Perfil (admin/funcionario):", bg="#cce6ff", font=("Arial", 12)).pack(pady=5)
    entry_perfil = ttk.Entry(cadastro, width=30)
    entry_perfil.pack(pady=5)

    def salvar():
        salvar_usuario(entry_nome.get(), entry_login.get(), entry_senha_cad.get(), entry_perfil.get())

    ttk.Button(cadastro, text="Salvar", command=salvar).pack(pady=10)

# Tela de alteração de dados do admin
def alterar_admin():
    janela = tk.Toplevel(root)
    janela.title("Alterar dados do Admin")
    janela.configure(bg="#cce6ff")

    barra = tk.Frame(janela, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Alterar dados do Admin", fg="white", bg="#0066cc", font=("Arial", 14, "bold")).pack(pady=5)

    tk.Label(janela, text="Novo nome:", bg="#cce6ff", font=("Arial", 12)).pack(pady=5)
    entry_nome = ttk.Entry(janela, width=30)
    entry_nome.pack(pady=5)

    tk.Label(janela, text="Nova senha:", bg="#cce6ff", font=("Arial", 12)).pack(pady=5)
    entry_senha = ttk.Entry(janela, width=30, show="*")
    entry_senha.pack(pady=5)

    def salvar_alteracao():
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE Usuario SET nome=?, senha=? WHERE login='admin'",
                       (entry_nome.get(), entry_senha.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Dados do admin atualizados!")
        janela.destroy()

    ttk.Button(janela, text="Salvar", command=salvar_alteracao).pack(pady=10)

# Menu do admin
def abrir_menu_admin():
    menu = tk.Toplevel(root)
    menu.title("Menu do Admin")
    menu.configure(bg="#cce6ff")

    barra = tk.Frame(menu, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Menu do Admin", fg="white", bg="#0066cc", font=("Arial", 14, "bold")).pack(pady=5)

    ttk.Button(menu, text="Cadastrar novo usuário", command=abrir_cadastro_usuario).pack(pady=10)
    ttk.Button(menu, text="Alterar meus dados", command=alterar_admin).pack(pady=10)

# Tela principal de login
root = tk.Tk()
root.title("SaracaFarma - Login")
root.geometry("400x300")
root.configure(bg="#cce6ff")

# Barra superior azul
barra = tk.Frame(root, bg="#0066cc", height=50)
barra.pack(fill="x")
titulo = tk.Label(barra, text="SaracaFarma", fg="white", bg="#0066cc", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Estilos
style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), foreground="#0066cc", background="#5a7d9a")  # texto azul da barra
style.configure("TEntry", font=("Arial", 12), fieldbackground="white")

# Layout com grid
frame = tk.Frame(root, bg="#cce6ff")
frame.pack(pady=30)

ttk.Label(frame, text="Usuário:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_usuario = ttk.Entry(frame, width=25)
entry_usuario.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame, text="Senha:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_senha = ttk.Entry(frame, width=25, show="*")
entry_senha.grid(row=1, column=1, padx=10, pady=10)

ttk.Button(frame, text="Entrar", command=validar_login).grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()
