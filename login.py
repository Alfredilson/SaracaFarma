import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from principal import tela_principal   # importa a tela principal

def inicializar_banco():
    conn = sqlite3.connect("saracaFarma.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    """)
    # Cria admin padrão se não existir
    cursor.execute("SELECT * FROM Usuario WHERE login='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
                       ("Administrador", "admin", "1234", "admin"))
    conn.commit()
    conn.close()

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
        root.destroy()          #Fecha a tela de login
        tela_principal(perfil)   # chama a tela principal
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")

# Tela de login
root = tk.Tk()
root.title("SaracaFarma - Login")
root.geometry("420x280")
root.configure(bg="#cce6ff")

barra = tk.Frame(root, bg="#0066cc", height=50)
barra.pack(fill="x")
titulo = tk.Label(barra, text="SaracaFarma", fg="white", bg="#0066cc", font=("Segoe UI", 16, "bold"))
titulo.pack(pady=10)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12, "bold"), foreground="#0066cc", background="#5a7d9a")
style.map("TButton",
          foreground=[("active", "white")],
          background=[("active", "#0066cc")])
style.configure("TEntry", font=("Segoe UI", 12), fieldbackground="white")

frame = tk.Frame(root, bg="#cce6ff")
frame.pack(expand=True)

ttk.Label(frame, text="Usuário:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_usuario = ttk.Entry(frame, width=28)
entry_usuario.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame, text="Senha:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_senha = ttk.Entry(frame, width=28, show="*")
entry_senha.grid(row=1, column=1, padx=10, pady=10)

ttk.Button(frame, text="Entrar", command=validar_login).grid(row=2, column=0, columnspan=2, pady=20)

inicializar_banco()
root.mainloop()
