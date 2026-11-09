# repository.py
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

def obter_conexao():
    """
    Cria e retorna uma conexão com o banco de dados MySQL
    utilizando as credenciais armazenadas de forma segura no arquivo .env.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
''' ============================== FUNÇÕES A SEREM CHAMADAS PELO app.py ============================== '''

def buscar_por_cpf(cpf):
    """
    Verifica se já existe um usuário cadastrado com o CPF informado.
    Retorna o dicionário com o ID se encontrar, ou None se não existir.
    """
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        # dictionary=True faz o MySQL retornar os dados como um dicionário Python (ex: {'id': 1})
        cursor = conexao.cursor(dictionary=True)
        
        # Query parametrizada com %s -> Proteção contra SQL Injection
        query = "SELECT id FROM usuarios WHERE cpf = %s"
        cursor.execute(query, (cpf,))
        
        usuario = cursor.fetchone()
        return usuario

    except Error as erro:
        print(f"Erro ao buscar CPF no banco de dados: {erro}")
        raise erro

    finally:
        # Garante que as conexões sejam fechadas para não sobrecarregar o banco
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def buscar_por_email(email):
    """
    Verifica se já existe um usuário cadastrado com o e-mail informado.
    Retorna o dicionário com o ID se encontrar, ou None se não existir.
    """
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        
        query = "SELECT id, nome FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        
        usuario = cursor.fetchone()
        return usuario

    except Error as erro:
        print(f"Erro ao buscar e-mail no banco de dados: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def salvar_usuario(dados_usuario):
    """
    Insere um novo usuário na tabela 'usuarios'.
    Não passamos id, created_at nem updated_at pois o MySQL cuida deles automaticamente.
    """
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        # A instrução SQL respeita exatamente a estrutura da tabela modelada
        query = """
            INSERT INTO usuarios (nome, cpf, email, data_nascimento, genero, uf)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        valores = (
            dados_usuario['nome'],
            dados_usuario['cpf'],
            dados_usuario['email'],
            dados_usuario['data_nascimento'],
            dados_usuario['genero'],
            dados_usuario['uf']
        )
        
        cursor.execute(query, valores)
        
        # O commit é obrigatório para confirmar a gravação dos dados no MySQL
        conexao.commit()
        
        # Recupera o ID gerado pelo AUTO_INCREMENT do MySQL
        novo_id = cursor.lastrowid
        
        return {"id": novo_id}

    except Error as erro:
        # Se ocorrer algum erro durante a inserção, desfaz qualquer alteração pendente
        if conexao:
            conexao.rollback()
        print(f"Erro ao salvar usuário no banco de dados: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

      
def salvar_alerta(dados_usuario):

    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        # A instrução SQL respeita exatamente a estrutura da tabela modelada
        query = """
            INSERT INTO config_alerta (usuario_id, tipo, percentual)
            VALUES (%s, %s, %s)
        """
        
        valores = (
            dados_usuario['usuario_id'],
            dados_usuario['tipo'],
            dados_usuario['percentual']
        )
        
        cursor.execute(query, valores)
        
        # O commit é obrigatório para confirmar a gravação dos dados no MySQL
        conexao.commit()
        
        # Recupera o ID gerado pelo AUTO_INCREMENT do MySQL
        novo_id = cursor.lastrowid
        
        return {"id": novo_id}

    except Error as erro:
        # Se ocorrer algum erro durante a inserção, desfaz qualquer alteração pendente
        if conexao:
            conexao.rollback()
        print(f"Erro ao salvar configuração do alerta no banco de dados: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

''' ============================== FUNÇÕES A SEREM CHAMADAS PELO WORKER_01.py ======================== '''
     
def salvar_preco_btc(dados_binance):
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        query = """
            INSERT INTO preco_btc (preco_dolar, preco_reais)
            VALUES (%s, %s)
        """
        
        valores = (
            dados_binance.get('preco_dolar'),
            dados_binance.get('preco_reais')
        )
        
        cursor.execute(query, valores)
        
        # O commit é obrigatório para confirmar a gravação dos dados no MySQL
        conexao.commit()
        
        # Recupera o ID gerado pelo AUTO_INCREMENT do MySQL
        novo_id = cursor.lastrowid
        
        return {"id": novo_id}

    except Error as erro:
        # Se ocorrer algum erro durante a inserção, desfaz qualquer alteração pendente
        if conexao:
            conexao.rollback()
        print(f"Erro ao salvar o preço no banco de dados: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


def buscar_ultimo_preco():
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        
        # Pega o registro mais recente usando o ID auto_increment
        query = "SELECT id, preco_dolar, preco_reais, created_at FROM preco_btc ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        
        resultado = cursor.fetchone()
        return resultado # Retorna o dicionário com o último preço ou None se estiver vazio

    except Error as erro:
        print(f"Erro ao buscar o último preço no banco de dados: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def buscar_todos_alertas():
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        
        query = "SELECT id, usuario_id, tipo, percentual FROM config_alerta"
        cursor.execute(query)
        
        alertas = cursor.fetchall()
        return alertas # Retorna uma lista com todos os dicionários de alertas

    except Error as erro:
        print(f"Erro ao buscar configurações de alerta: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def salvar_historico_alerta(dados_historico):
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        query = """
            INSERT INTO historico_alertas (config_alerta_id, preco_dolar, preco_reais, direcao)
            VALUES (%s, %s, %s, %s)
        """
        
        valores = (
            dados_historico['config_alerta_id'],
            dados_historico.get('preco_dolar'),
            dados_historico.get('preco_reais'),
            dados_historico['direcao']
        )
        
        cursor.execute(query, valores)
        conexao.commit()
        
        novo_id = cursor.lastrowid
        return {"id": novo_id}

    except Error as erro:
        if conexao:
            conexao.rollback()
        print(f"Erro ao salvar histórico de alerta: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def buscar_historico_por_usuario(usuario_id):
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        
        # Fazemos um JOIN para filtrar os históricos que pertencem às configs do usuario_id
        query = """
            SELECT h.id, h.config_alerta_id, h.preco_dolar, h.preco_reais, h.direcao, h.created_at
            FROM historico_alertas h
            JOIN config_alerta c ON h.config_alerta_id = c.id
            WHERE c.usuario_id = %s
            ORDER BY h.created_at DESC
        """
        cursor.execute(query, (usuario_id,))
        historico = cursor.fetchall()
        return historico

    except Error as erro:
        print(f"Erro ao buscar histórico do usuário: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def buscar_config_alerta_por_usuario(usuario_id):
    """
    Busca as configurações de alerta cadastradas para um usuário específico.
    """
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        
        query = "SELECT id, usuario_id, tipo, percentual FROM config_alerta WHERE usuario_id = %s"
        cursor.execute(query, (usuario_id,))
        
        alertas = cursor.fetchall()
        return alertas

    except Error as erro:
        print(f"Erro ao buscar configurações de alerta do usuário: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
