# Bitntime — Sprint 1

## 📌 Objetivo da Sprint

Implementar o fluxo inicial do cadastro de usuários do projeto Bitntime, cobrindo a integração de ponta a ponta entre a interface do usuário (Front-end em HTML/CSS), o processamento de regras de negócio e validações de dados (Back-end em Python/Flask) e a persistência dos registros em banco de dados (MySQL).

---

## 🛠️ Estrutura e Configuração do Ambiente

### Pre-requisitos

* **Python** 3.x instalado


* **MySQL** instalado e em execução

---

### 1. Banco de Dados (MySQL)

1. Certifique-se de que o servidor MySQL esteja rodando.
2. Execute o scripts SQL fornecido no projeto (`..\BD\CREATE TABLE.sql`) para criar a tabela de usuários.

---

### 2. Back-end (Python / Flask)

1. Caso não tenha, instale as dependências necessárias do projet, por exemplo:
```bash
pip install flask mysql-connector-python
```

2. Crie um arquivo `.env` na pasta indicada (`\Back`) com as seguintes variáveis:

```bash
DB_HOST=seu_host
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=nome_do_banco
```



3. Inicie o servidor da API Flask:
```bash
python app.py
```


*A API estará acessível por padrão em: `http://localhost:5000` (ou na rota configurada `/api/usuarios`)*.



---

### 3. Front-end (HTML / CSS)

1. O Front-end é composto por arquivos estáticos.


2. Abra o arquivo `index.html` diretamente em qualquer navegador moderno para acessar e utilizar o formulário de cadastro.
