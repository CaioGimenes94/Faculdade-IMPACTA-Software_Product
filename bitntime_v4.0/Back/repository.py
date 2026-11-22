# repository.py
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

def atualizar_alerta(dados_usuario):
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        # A instrução SQL respeita exatamente a estrutura da tabela modelada
        query = """
            UPDATE config_alerta SET  tipo = %s, percentual = %s WHERE usuario_id = %s
        """
        
        valores = (
            dados_usuario['tipo'],
            dados_usuario['percentual'],
            dados_usuario['usuario_id']
        )
        
        cursor.execute(query, valores)
        
        # O commit é obrigatório para confirmar a gravação dos dados no MySQL
        conexao.commit()
        
        return {"status": "sucesso", "usuario_id": dados_usuario['usuario_id']}

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

def buscar_config_usuario(usuario_id):
    """
    Busca as configurações do usuário.
    """
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        
        query = "SELECT id, email, uf FROM usuarios WHERE id = %s"
        cursor.execute(query, (usuario_id,))
        
        usuario = cursor.fetchall()
        return usuario

    except Error as erro:
        print(f"Erro ao buscar configurações do usuário: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def atualizar_cadastro_usuario(dados_usuario):
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        query = """
            UPDATE usuarios SET email = %s, uf = %s WHERE id = %s
        """
        
        valores = (
            dados_usuario['email'],
            dados_usuario['uf'],
            dados_usuario['usuario_id']
        )
        
        cursor.execute(query, valores)
        
        # O commit é obrigatório para confirmar a gravação dos dados no MySQL
        conexao.commit()
        
        return {"status": "sucesso", "usuario_id": dados_usuario['usuario_id']}

    except Error as erro:
        # Se ocorrer algum erro durante a inserção, desfaz qualquer alteração pendente
        if conexao:
            conexao.rollback()
        print(f"Erro ao alterar os dados do usuário no banco de dados: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

def ultimo_preco_e_alerta(usuario_id):
    # 1. Pega o último preço do Bitcoin salvo pelo worker
    ultimo_preco = buscar_ultimo_preco() # Retorna {'preco_reais': ..., 'preco_dolar': ...} ou None

    # 2. Pega as configurações de alerta do usuário para saber se ele usa REAIS ou DOLAR
    alertas_usuario = buscar_config_alerta_por_usuario(usuario_id) 
    tipo_moeda = alertas_usuario[0]['tipo'] if alertas_usuario else 'REAIS' # Padrão Reais se não tiver

    # 3. Pega o histórico de alertas disparados para este usuário
    historico_usuario = buscar_historico_por_usuario(usuario_id)
    ultimo_alerta = historico_usuario[0] if historico_usuario else None
    
    return(
        ultimo_preco,
        tipo_moeda,
        ultimo_alerta
    )


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

''' ============================== aba histórico ======================== '''

CONFIG_PERIODO_HISTORICO = {
    '24h': {'delta': timedelta(hours=24), 'passo_minutos': 15, 'formato_label': '%H:%M'},
    '7d': {'delta': timedelta(days=7), 'passo_minutos': 60, 'formato_label': '%d/%m %H:%M'},
    '30d': {'delta': timedelta(days=30), 'passo_minutos': 240, 'formato_label': '%d/%m %H:%M'},
}


def _calcular_variacao_pct(preco_atual, preco_inicial):
    """Calcula ((preco_atual / preco_inicial) - 1) * 100 com segurança."""
    if preco_inicial is None or preco_atual is None or float(preco_inicial) == 0:
        return 0.0
    return round(((float(preco_atual) / float(preco_inicial)) - 1.0) * 100.0, 2)


def _amostrar_serie_por_intervalo(registros, passo_minutos, formato_label):
    """
    Seleciona no máximo um registro por janela de `passo_minutos` a partir
    do primeiro registro da série, preservando a tendência.
    """
    if not registros:
        return []

    amostra = []
    primeiro_dt = registros[0]['created_at']
    proximo_bucket_min = 0

    for reg in registros:
        dt = reg['created_at']
        minutos_desde_inicio = (dt - primeiro_dt).total_seconds() / 60.0

        if minutos_desde_inicio >= proximo_bucket_min:
            amostra.append({
                'label': dt.strftime(formato_label),
                'preco_reais': float(reg['preco_reais']),
                'preco_dolar': float(reg['preco_dolar']),
            })
            # Avança o bucket para o próximo múltiplo de passo_minutos
            buckets_passados = int(minutos_desde_inicio // passo_minutos)
            proximo_bucket_min = (buckets_passados + 1) * passo_minutos

    return amostra


def buscar_serie_preco_historico(periodo='24h'):
    """
    Retorna os dados da Seção 1 para o período ('24h', '7d' ou '30d'):
    - labels: lista de horários/datas amostrados
    - variacao_brl: lista de variações % (base 0% no primeiro ponto)
    - variacao_usd: lista de variações % (base 0% no primeiro ponto)
    - variacao_total_brl: variação % final no período
    - variacao_total_usd: variação % final no período
    - tem_dados: bool indicando se há cotações no período
    """
    cfg = CONFIG_PERIODO_HISTORICO.get(periodo, CONFIG_PERIODO_HISTORICO['24h'])
    data_limite = datetime.now() - cfg['delta']

    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)

        query = """
            SELECT id, preco_dolar, preco_reais, created_at
            FROM preco_btc
            WHERE created_at >= %s
              AND preco_dolar IS NOT NULL
              AND preco_reais IS NOT NULL
            ORDER BY created_at ASC, id ASC
        """
        cursor.execute(query, (data_limite,))
        registros = cursor.fetchall()

    except Error as erro:
        print(f"Erro ao buscar série histórica de preços: {erro}")
        raise erro

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

    pontos = _amostrar_serie_por_intervalo(
        registros,
        passo_minutos=cfg['passo_minutos'],
        formato_label=cfg['formato_label'],
    )

    if not pontos:
        return {
            'labels': [],
            'variacao_brl': [],
            'variacao_usd': [],
            'variacao_total_brl': 0.0,
            'variacao_total_usd': 0.0,
            'tem_dados': False,
        }

    base_brl = pontos[0]['preco_reais']
    base_usd = pontos[0]['preco_dolar']

    labels = [p['label'] for p in pontos]
    variacao_brl = [_calcular_variacao_pct(p['preco_reais'], base_brl) for p in pontos]
    variacao_usd = [_calcular_variacao_pct(p['preco_dolar'], base_usd) for p in pontos]

    return {
        'labels': labels,
        'variacao_brl': variacao_brl,
        'variacao_usd': variacao_usd,
        'variacao_total_brl': variacao_brl[-1],
        'variacao_total_usd': variacao_usd[-1],
        'tem_dados': True,
    }


def buscar_ultimos_alertas_formatados(usuario_id, limite=10):
    """
    Retorna os últimos `limite` alertas do usuário logado para a Seção 2,
    exibindo apenas a moeda configurada em config_alerta.tipo (BRL ou USD).
    """
    alertas_raw = buscar_historico_por_usuario(usuario_id)[:limite]
    configs = buscar_config_alerta_por_usuario(usuario_id)

    # Mapeia config_alerta.id -> 'BRL' ou 'USD'
    moeda_por_config = {}
    for cfg in configs:
        tipo_db = (cfg.get('tipo') or '').upper()
        moeda_por_config[cfg['id']] = 'USD' if tipo_db == 'DOLAR' else 'BRL'

    alertas_formatados = []
    for item in alertas_raw:
        moeda = moeda_por_config.get(item['config_alerta_id'], 'BRL')
        cotacao = item['preco_dolar'] if moeda == 'USD' else item['preco_reais']
        created_at = item.get('created_at')
        data_formatada = (
            created_at.strftime('%d/%m/%Y %H:%M:%S')
            if hasattr(created_at, 'strftime')
            else str(created_at)
        )

        alertas_formatados.append({
            'id': item['id'],
            'data_hora': data_formatada,
            'direcao': item['direcao'],
            'moeda': moeda,
            'cotacao': float(cotacao) if cotacao is not None else None,
        })

    return alertas_formatados