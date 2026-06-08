import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from admin import abrir_funcoes_admin
from produto import cadastrar_produto
from produto import cadastrar_produtos_treeview 
#---from produto import cadastrar_produtos_csv
from produto import cadastrar_produtos_fornecedor
from tkinter import filedialog
from controle_estoque import tela_estoque, tela_relatorio

def cadastrar_lista_produtos():
    # Função placeholder para cadastro em lote
    arquivo = filedialog.askopenfilename(title="Selecionar arquivo de produtos", filetypes=[("CSV", "*.csv"), ("Todos", "*")])
    if arquivo:
        messagebox.showinfo("Cadastro em Lote", f"Arquivo selecionado: {arquivo}\nFuncionalidade ainda não implementada.")

def tela_principal(perfil):
    principal = tk.Tk()
    principal.title("SaracaFarma - Tela Principal")
    principal.geometry("600x400")
    principal.configure(bg="#cce6ff")

     # Faz a janela abrir maximizada
    principal.state("zoomed")   # no Windows
    # ou, se quiser ocupar toda a tela em qualquer sistema:
    # principal.attributes("-fullscreen", True)
       

    # Criar barra de menu
    menubar = tk.Menu(principal)

      # Menu Cadastro
    menu_cadastro = tk.Menu(menubar, tearoff=0)
    #Chamada direta da função de cadastro de produto.
    menu_cadastro.add_command(label="Cadastro Individual", command=lambda: cadastrar_produto(perfil))
    menu_cadastro.add_command(label="Cadastro em Lote (Treeview)", command=lambda: cadastrar_produtos_treeview(perfil))
    #---menu_cadastro.add_command(label="Cadastro em Lote (CSV)", command=lambda: cadastrar_produtos_csv(perfil))
    menu_cadastro.add_command(label="Cadastro em Lote via Fornecedor", command=lambda: cadastrar_produtos_fornecedor(perfil))


    menubar.add_cascade(label="Cadastro", menu=menu_cadastro)

     # Menu Estoque
    menu_estoque = tk.Menu(menubar, tearoff=0)
    menu_estoque.add_command(label="Controle de Estoque", command=lambda: tela_estoque(perfil)) # Placeholder para função de relatório
    menu_estoque.add_command(label="Controlar Relatorio", command=tela_relatorio) # Placeholder para função de relatório
    menu_estoque.add_command(label="Consultar Saldo",)
    menubar.add_cascade(label="Estoque", menu=menu_estoque)

    # Menu Administração (somente se perfil for admin)
    if perfil == "admin":
        menu_admin = tk.Menu(menubar, tearoff=0)
        menu_admin.add_command(label="Funções Administrativas", command=abrir_funcoes_admin)
        menubar.add_cascade(label="Administração", menu=menu_admin)
    
       # Menu Sair
    menu_sair = tk.Menu(menubar, tearoff=0)
    menu_sair.add_command(label="Encerrar", command=principal.quit)
    menubar.add_cascade(label="Sair", menu=menu_sair)

    barra = tk.Frame(principal, bg="#0066cc", height=40)
    barra.pack(fill="x")
    tk.Label(barra, text="Tela Principal - SaracaFarma", fg="white", bg="#0066cc", font=("Segoe UI", 14, "bold")).pack(pady=5)

    frame = tk.Frame(principal, bg="#cce6ff")
    frame.pack(pady=30)

    
    # Associar menu à janela
    principal.config(menu=menubar)
    
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
