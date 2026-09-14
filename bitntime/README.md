# Bitntime — Monitoramento de Bitcoin

## Objetivo do projeto
- Sistema web para **monitorar o preço do Bitcoin**.
- Permite ao usuário configurar uma **variação percentual de alerta**.
- Quando a variação configurada é atingida, o sistema gera um **alerta por e-mail**.
- Os alertas ficam registrados para posterior **visualização e análise**.

## Tecnologias
- **Front-end:** HTML + CSS
- **Back-end:** Python + Flask
- **Banco de dados:** MySQL
- **API:** Binance — consulta do preço do Bitcoin
- **Versionamento:** Git/GitHub

## Desenvolvimento por Sprints

### Sprint 1 — Cadastro de usuário
- Tela de cadastro
- API para receber os dados
- Persistência dos usuários no banco

### Sprint 2 — Configuração de alertas
- Cadastro da preferência de variação do Bitcoin
- Associação do alerta ao usuário
- Persistência das configurações

### Sprint 3 — Alertas por e-mail
- Monitoramento da variação do Bitcoin
- Disparo do alerta por e-mail
- Registro dos alertas disparados

### Sprint 4 — Dashboard
- Consulta dos alertas registrados
- Visualização do histórico
- Gráfico simples de acompanhamento
- Organização final da navegação do sistema

## ⚙️ Configuração do Banco de Dados

Para rodar o projeto localmente, crie um arquivo `.env` na pasta indicada (`\Back`) com as seguintes variáveis:

```env
DB_HOST=seu_host
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=nome_do_banco