'''
# worker_01.py: 
/ acionado quando o app.py iniciar
/ roda em loop fazendo pooling na binance para obter o preco do btc em Reais e Dolar 
/ chama a função que na tabela de histório de preços do btc
/ verifica a tabela de config de alerta dos usuarios e grava os alertas que foram atingidos na tabela de alertas do usuario
'''
import time
import requests
import repository

def consultar_binance():
    """
    Consulta o preço atual do Bitcoin (BRL e USD) na API da Binance com tratamento de erros.
    Retorna um dicionário com os dados ou None em caso de falha.
    """
    url_brl = "https://api.binance.com/api/v3/ticker/price?symbol=BTCBRL"
    url_usd = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDC"
    tentativas = 3
    
    for tentativa in range(tentativas):
        try:
            resposta_brl = requests.get(url_brl, timeout=10)
            resposta_usd = requests.get(url_usd, timeout=10)

            resposta_brl.raise_for_status()
            resposta_usd.raise_for_status()
            
            preco_reais = float(resposta_brl.json()['price'])
            preco_usd = float(resposta_usd.json()['price'])
            
            return {
                'preco_reais': preco_reais,
                'preco_dolar': preco_usd 
            }
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {tentativa + 1} falhou ao acessar a Binance: {e}")
            time.sleep(10)  # Aguarda 10 segundos antes de tentar novamente
            
    print("Falha ao obter o preço da Binance após várias tentativas.")
    return None

def verificar_e_disparar_alertas(preco_atual, preco_anterior):
    """
    Busca todas as configurações de alerta e compara a variação com o preço atual.
    Se a condição for atingida, grava um registro em historico_alertas.
    """
    if not preco_anterior:
        return # Se não temos um preço anterior para comparar, encerra esta checagem

    alertas = repository.buscar_todos_alertas()
    if not alertas:
        return

    for alerta in alertas:
        alerta_id = alerta['id']
        tipo_alerta = alerta['tipo']        # 'REAIS' ou 'DOLAR'
        percentual_alvo = float(alerta['percentual'])  # Ex: 0.05 para 5%
        
        # Define qual moeda estamos analisando com base na configuração do usuário
        if tipo_alerta == 'REAIS':
            atual = preco_atual['preco_reais']
            anterior = preco_anterior['preco_reais']
        elif tipo_alerta == 'DOLAR':
            atual = preco_atual['preco_dolar']
            anterior = preco_anterior['preco_dolar']
        else:
            continue

        if not anterior or not atual:
            continue

        # Calcula a variação com sinal (positivo = subiu, negativo = caiu)
        variacao_com_sinal = (atual - anterior) / anterior
        variacao_absoluta = abs(variacao_com_sinal)

        if variacao_absoluta >= percentual_alvo:
            # Descobre a direção com base no sinal
            direcao = "ALTA" if variacao_com_sinal > 0 else "QUEDA"
            
            # print(f"[ALERTA DE {direcao}!] Variação de {variacao_com_sinal*100:.2f}%")
            
            dados_gatilho = {
                'config_alerta_id': alerta_id,
                'preco_reais': preco_atual['preco_reais'],
                'preco_dolar': preco_atual['preco_dolar'],
                'direcao': direcao # <--- Você poderia salvar isso no banco também se quiser!
            }
            repository.salvar_historico_alerta(dados_gatilho)

def iniciar_monitoramento():
    """
    Loop principal que roda em background, consultando a Binance periodicamente.
    """
    # print(">>> Worker de monitoramento do Bitcoin iniciado. (Pressione Ctrl + C para parar)")
    preco_anterior = None
    
    try:
        while True:
            # 1. Consulta o preço na API
            dados_preco = consultar_binance()
            
            if dados_preco:
                # 2. Salva o preço na tabela preco_btc usando o repositório
                repository.salvar_preco_btc(dados_preco)
                print(f"[Worker] Preço atualizado: R$ {dados_preco['preco_reais']} | US$ {dados_preco['preco_dolar']}")
                
                # 3. Verifica se algum alerta deve ser disparado com base na variação
                verificar_e_disparar_alertas(dados_preco, preco_anterior)
                
                # 4. Atualiza o preço anterior para o próximo ciclo
                preco_anterior = dados_preco
            
            # 5. Aguarda o intervalo (ex: 10 segundos para o teste)
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n>>> [Worker] Interrompido pelo usuário com segurança. Encerrando...")

# if __name__ == "__main__":
#     iniciar_monitoramento()