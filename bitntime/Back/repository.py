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
        
        query = "SELECT id FROM usuarios WHERE email = %s"
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
            