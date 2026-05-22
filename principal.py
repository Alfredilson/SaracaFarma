import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from admin import abrir_funcoes_admin   # importa funções administrativas

def tela_principal(perfil):
    principal = tk.Tk()
    principal.title("SaracaFarma - Tela Principal")
    principal.geometry("600x400")
    principal.configure(bg="#cce6ff")

    barra = tk.Frame(principal, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Tela Principal - SaracaFarma", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(principal, bg="#cce6ff")
    frame.pack(pady=30)

    ttk.Button(frame, text="Cadastro de Medicamentos").pack(pady=10)
    ttk.Button(frame, text="Controle de Estoque").pack(pady=10)
    ttk.Button(frame, text="Relatórios").pack(pady=10)
    ttk.Button(frame, text="Funções Administrativas", command=verificar_admin).pack(pady=10)
    principal.mainloop()

def verificar_admin():
    janela = tk.Toplevel()
    janela.title("Verificação Admin")
    janela.geometry("300x200")
    janela.configure(bg="#cce6ff")

    tk.Label(janela, text="Login Admin:", bg="#cce6ff").pack(pady=5)
    entry_login = ttk.Entry(janela, width=25)
    entry_login.pack(pady=5)

    tk.Label(janela, text="Senha:", bg="#cce6ff").pack(pady=5)
    entry_senha = ttk.Entry(janela, width=25, show="*")
    entry_senha.pack(pady=5)

    def validar_admin():
        conn = sqlite3.connect("saracaFarma.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE login=? AND senha=? AND perfil='admin'", 
                       (entry_login.get(), entry_senha.get()))
        result = cursor.fetchone()
        conn.close()
        if result:
            messagebox.showinfo("Sucesso", "Acesso administrativo liberado!")
            abrir_funcoes_admin()
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Login ou senha inválidos.")

    ttk.Button(janela, text="Entrar", command=validar_admin).pack(pady=10)
