# Documentação do Sistema SaracaFarma

## 1. Introdução
O SaracaFarma é um sistema de controle de farmácia desenvolvido em Python com interface gráfica (Tkinter) e banco de dados SQLite.  
O objetivo é facilitar o gerenciamento de usuários, medicamentos, estoque e relatórios.

---

## 2. Estrutura do Projeto
- **login.py** → Tela de login e inicialização do banco.
- **principal.py** → Tela principal do sistema, acessada após login.
- **admin.py** → Funções administrativas (cadastro de usuários, alteração de dados do admin).
- **saracaFarma.db** → Banco de dados SQLite.

---

## 3. Fluxo de Login
- Usuário informa **login** e **senha**.
- O sistema valida os dados na tabela `Usuario`.
- Se válidos:
  - Fecha a tela de login.
  - Abre a **tela principal**.
- Se inválidos:
  - Exibe mensagem de erro.

**Regras de negócio:**
- Usuário `admin` é criado automaticamente na primeira execução.
- Perfil `admin` tem acesso às funções administrativas.
- Perfis comuns acessam apenas funções padrão.

---

## 4. Tela Principal
Após login, o usuário acessa a tela principal, que contém:
- Botão **Cadastro de Medicamentos** (em desenvolvimento).
- Botão **Controle de Estoque** (em desenvolvimento).
- Botão **Relatórios** (em desenvolvimento).
- Botão **Funções Administrativas** → exige login e senha do admin.

---

## 5. Banco de Dados
### Tabela `Usuario`
- `id_usuario` (INTEGER, PK, AUTOINCREMENT)
- `nome` (TEXT)
- `login` (TEXT, único)
- `senha` (TEXT)
- `perfil` (TEXT: `admin` ou `funcionario`)

---

## 6. Próximos Módulos
- Cadastro de Medicamentos
- Controle de Estoque
- Relatórios
