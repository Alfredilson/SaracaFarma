import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from principal import tela_principal   # importa a tela principal
import os
from db import conexao, cursor
from ui_theme import apply_theme, styled_button, PRIMARY_BG, HEADER_BG, HEADER_FG, BUTTON_TEXT_FG, BUTTON_PRIMARY_BG, BUTTON_SECONDARY_BG, INPUT_BG

def inicializar_banco():
    db_file = "saracaFarma.db"
    schema_file = "schema.sql"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Executa o schema.sql (garante que todas as tabelas existam)
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)

    # Garante que o admin exista
    cursor.execute("SELECT * FROM Usuario WHERE perfil='admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO Usuario (nome, login, senha, perfil) VALUES (?, ?, ?, ?)",
            ("Administrador", "admin", "1234", "admin")
        )

    # Atualiza o esquema caso o banco já exista sem as colunas novas
    cursor.execute("PRAGMA table_info(Cliente)")
    colunas_cliente = [col[1] for col in cursor.fetchall()]
    if "permite_fiado" not in colunas_cliente:
        cursor.execute("ALTER TABLE Cliente ADD COLUMN permite_fiado INTEGER NOT NULL DEFAULT 0")
    if "limite_fiado" not in colunas_cliente:
        cursor.execute("ALTER TABLE Cliente ADD COLUMN limite_fiado REAL NOT NULL DEFAULT 0.0")
    conn.commit()
    conn.close()



def validar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    cursor.execute("SELECT id_usuario, perfil FROM Usuario WHERE login=? AND senha=?", (usuario, senha))
    result = cursor.fetchone()
    if result:
        id_usuario, perfil = result
        root.destroy()          # Fecha a tela de login
        tela_principal(id_usuario)   # chama a tela principal com o id do usuário
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")



# Tela de login
root = tk.Tk()
root.title("SaracaFarma - Login")
root.geometry("420x280")
apply_theme(root)

barra = tk.Frame(root, bg=HEADER_BG, height=50)
barra.pack(fill="x")
titulo = tk.Label(barra, text="SaracaFarma", fg=HEADER_FG, bg=HEADER_BG, font=("Segoe UI", 16, "bold"))
titulo.pack(pady=10)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12, "bold"), foreground=BUTTON_TEXT_FG, background=BUTTON_PRIMARY_BG)
style.map("TButton",
          foreground=[("active", BUTTON_TEXT_FG)],
          background=[("active", BUTTON_SECONDARY_BG)])
style.configure("TEntry", font=("Segoe UI", 12), fieldbackground=BUTTON_TEXT_FG)

frame = tk.Frame(root, bg=PRIMARY_BG)
frame.pack(expand=True)

ttk.Label(frame, text="Usuário:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_usuario = ttk.Entry(frame, width=28)
entry_usuario.grid(row=0, column=1, padx=10, pady=10)

# Foco inicial no campo Usuário e binding Enter -> ir para Senha
entry_usuario.focus_set()
entry_usuario.bind("<Return>", lambda event: entry_senha.focus_set())

ttk.Label(frame, text="Senha:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_senha = ttk.Entry(frame, width=28, show="*")
entry_senha.grid(row=1, column=1, padx=10, pady=10)

# Binding Enter em Senha -> executar validação/login
entry_senha.bind("<Return>", lambda event: validar_login())

styled_button(frame, text="Entrar", command=validar_login).grid(row=2, column=0, columnspan=2, pady=20)

inicializar_banco()
root.mainloop()
