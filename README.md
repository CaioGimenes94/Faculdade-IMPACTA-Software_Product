# Bitntime — Monitoramento de Bitcoin

Sistema web desenvolvido para monitoramento do preço do Bitcoin e geração de alertas com base em variações percentuais configuradas pelo usuário.

## 🎯 Objetivo

O Bitntime permite que o usuário acompanhe a variação do preço do Bitcoin e configure alertas personalizados.

Quando a variação definida pelo usuário é atingida, o sistema gera um alerta por e-mail. Os alertas são armazenados para permitir consultas e análises posteriores.

O projeto está sendo desenvolvido de forma incremental, utilizando quatro Sprints, nas quais novas funcionalidades são adicionadas ao sistema.

---

## 🛠️ Tecnologias

* **Front-end:** HTML + CSS
* **Back-end:** Python + Flask
* **Banco de dados:** MySQL
* **API externa:** Binance — consulta do preço do Bitcoin
* **Versionamento:** Git / GitHub

---

## 📋 Desenvolvimento por Sprints

### Sprint 1 — Cadastro de usuário

Implementação da base do sistema:

* Tela de cadastro de usuário
* API para recebimento dos dados
* Validação das informações
* Persistência dos usuários no MySQL

### Sprint 2 — Configuração de alertas

Implementação da configuração das preferências de monitoramento:

* Configuração da variação percentual do Bitcoin
* Definição da moeda de referência
* Associação da configuração ao usuário
* Persistência das configurações no banco

### Sprint 3 — Alertas por e-mail

Implementação do mecanismo de alerta:

* Monitoramento da variação do Bitcoin
* Identificação do atingimento da variação configurada
* Envio do alerta por e-mail
* Registro dos alertas disparados

### Sprint 4 — Dashboard

Implementação da visualização dos dados registrados:

* Consulta do histórico de alertas
* Visualização das informações
* Gráfico simples de acompanhamento
* Organização final da navegação do sistema

---

## 📁 Estrutura do projeto

```text
bitntime/
    ├── README.md
    ├── BD/
    |    └── CREATE TABLE.sql
    └── Back/
       ├── app.py
       ├── repository.py
       ├── validators.py
       ├── static/
       |    └── css/
       |        └── OK (AC2): style.css
       └── templates/
          ├── OK (AC2): base.html
          ├── OK (AC2): inicio.html     
          ├── OK (AC1): cadastro.html   
          ├── OK (AC2): config_alerta.html
          ├── OK (AC2): retorno_cadastro_erro.html
          ├── OK (AC2): retorno_cadastro_sucesso.html
          ├── MODIFICAR: login.html                   
          ├── FAZER: menu.html 
          └── FAZER: base_logada.html 
```

## 🔄 Evolução do sistema

O projeto segue uma evolução incremental:

```text
Sprint 1
Cadastro de usuários
        ↓
Sprint 2
Configuração de alertas
        ↓
Sprint 3
Envio e registro dos alertas
        ↓
Sprint 4
Dashboard e histórico
```

Cada entrega utiliza como base o que foi desenvolvido nas etapas anteriores, permitindo a evolução progressiva do Bitntime até sua versão final.

---

## 📌 Status

| Sprint   | Funcionalidade          | Status      |
| -------- | ----------------------- | ----------- |
| Sprint 1 | Cadastro de usuário     | ✅ Concluída |
| Sprint 2 | Configuração de alertas | ✅ Concluída |
| Sprint 3 | Alertas por e-mail      | 🔲 Pendente |
| Sprint 4 | Dashboard               | 🔲 Pendente |

---

## ⚙️ Configurações

Para rodar o projeto localmente, crie um arquivo `.env` com as seguintes variáveis:

```env
DB_HOST=seu_host
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=nome_do_banco
FLASK_SECRET_KEY=sua_senha

## 👨‍💻 Projeto acadêmico

Projeto desenvolvido como parte do curso de **Análise e Desenvolvimento de Sistemas**, utilizando uma abordagem incremental baseada em Sprints.
