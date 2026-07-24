import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from db import conexao, cursor


def cadastrar_cliente():
    janela_cliente = tk.Toplevel()
    janela_cliente.title("Cadastro de Cliente")
    janela_cliente.geometry("400x350")
    janela_cliente.configure(bg="#f0f8ff")

    # Campos
    tk.Label(janela_cliente, text="Nome:", bg="#f0f8ff").pack()
    entry_nome = ttk.Entry(janela_cliente)
    entry_nome.pack(pady=5)

    tk.Label(janela_cliente, text="CPF:", bg="#f0f8ff").pack()
    entry_cpf = ttk.Entry(janela_cliente)
    entry_cpf.pack(pady=5)

    tk.Label(janela_cliente, text="Telefone:", bg="#f0f8ff").pack()
    entry_telefone = ttk.Entry(janela_cliente)
    entry_telefone.pack(pady=5)

    tk.Label(janela_cliente, text="Email:", bg="#f0f8ff").pack()
    entry_email = ttk.Entry(janela_cliente)
    entry_email.pack(pady=5)

    tk.Label(janela_cliente, text="Endereço:", bg="#f0f8ff").pack()
    entry_endereco = ttk.Entry(janela_cliente)
    entry_endereco.pack(pady=5)

    def salvar_cliente():
        nome = entry_nome.get().strip()
        cpf = entry_cpf.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()
        endereco = entry_endereco.get().strip()

        if not nome or not cpf:
            messagebox.showwarning("Erro", "Nome e CPF são obrigatórios!")
            return

        try:
            cursor.execute("""
                INSERT INTO Cliente (nome, cpf, telefone, email, endereco)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, cpf, telefone, email, endereco))
            conexao.commit()
            messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado com sucesso.")
            janela_cliente.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado!")

    tk.Button(janela_cliente, text="Salvar", bg="#4CAF50", fg="white",
              command=salvar_cliente).pack(pady=15)
