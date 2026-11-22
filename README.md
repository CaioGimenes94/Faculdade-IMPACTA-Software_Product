# BiTnTime — Monitoramento de Bitcoin

Sistema web desenvolvido para monitoramento do preço do Bitcoin e geração de alertas com base em variações percentuais configuradas pelo usuário.

## 🎯 Objetivo

O Bitntime permite que o usuário acompanhe a variação do preço do Bitcoin e configure alertas personalizados.

Quando a variação definida pelo usuário é atingida, o sistema gera um alerta visual diretamente na interface web. Os alertas são armazenados para permitir consultas e análises posteriores.

O projeto foi desenvolvido de forma incremental, utilizando quatro Sprints, nas quais novas funcionalidades foram adicionadas ao sistema.

---

## 🛠️ Tecnologias

* **Front-end:** HTML + CSS, JavaScript (Chart.js)
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

### Sprint 3 — Alertas

Implementação do mecanismo de alerta:

* Monitoramento da variação do Bitcoin
* Identificação do atingimento da variação configurada
* Exibição do último alerta na tela inicial do usuário.
* Exibição do preço atual do bitcoin na tela inicial do usuário.
* Registro em BD dos alertas disparados

### Sprint 4 — Dashboard

Implementação da visualização dos dados registrados:

* Consulta do histórico de alertas
* Visualização das informações
* Gráfico de acompanhamento do preço do BTC em BRL e USD
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
       ├── worker_01.py OK (AC3)
       ├── static/
       |    ├── js/
       |    |    └── OK (PROVA): chart.umd.min.js
       |    └── css/
       |        └── OK (AC2): style.css
       └── templates/
          ├── OK (AC2): base.html
          ├── OK (AC2): inicio.html     
          ├── OK (AC1): cadastro.html   
          ├── OK (AC2): config_alerta.html
          ├── OK (AC2): retorno_cadastro_erro.html
          ├── OK (AC2): retorno_cadastro_sucesso.html
          ├── OK (AC3): retorno_login_erro.html
          ├── OK (AC3): login.html                   
          ├── OK (AC3): menu.html 
          ├── OK (AC3): base_logada.html
          ├── OK (PROVA): config_alerta_logado.html
          ├── OK (PROVA): retorno_cadastro_erro_logado.html
          ├── OK (PROVA): config_cadastro_logado.html
          ├── OK (PROVA): historico.html
          └── OK (PROVA): retorno_cadastro_erro_logado.html
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
Exibição e registro dos alertas
        ↓
Sprint 4
Histórico (Preço BTC e Alertas) e Atualizações (Alerta e cadastrais)
```

Cada entrega utiliza como base o que foi desenvolvido nas etapas anteriores, permitindo a evolução progressiva do Bitntime até sua versão final.

---

## 📌 Status

| Sprint   | Funcionalidade          | Status      |
| -------- | ----------------------- | ----------- |
| Sprint 1 | Cadastro de usuário     | ✅ Concluída |
| Sprint 2 | Configuração de alertas | ✅ Concluída |
| Sprint 3 | Alertas na web          | ✅ Concluída |
| Sprint 4 | Histórico BTC e alertas do usuário, atulização de dados do cadastro e do alerta   | ✅ Pendente |

---

## ⚙️ Configurações
Para rodar o projeto localmente: 
1. Certifique-se que tenha o Mysql e o Python instalados e configurados;
2. Instale todas as bibliotecas necessárias no Python;
3. Certifique-se que o código do Chart.js e coloque na pasta indicada do projeto.
4. Crie um arquivo `.env` com as seguintes variáveis:

```env
DB_HOST=seu_host
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=nome_do_banco
FLASK_SECRET_KEY=sua_senha
```

## 👨‍💻 Projeto acadêmico

Projeto desenvolvido como parte do curso de **Análise e Desenvolvimento de Sistemas**, utilizando uma abordagem incremental baseada em Sprints.
