# app.py

'''
# app.py: 
/ orquestra a aplicação WEB
/ cria o fluxo apartado de acionamento do worker (a ser implementado agora)
'''
from flask import Flask, request, redirect, url_for, render_template, session
import os
from dotenv import load_dotenv

# ''' COMENTADO PARA EVITAR FICAR CHAMANDO O WORKER ATOA ENQUANTO IMPLEMENTO O MENU
import threading
from worker_01 import iniciar_monitoramento 
# '''
import validators
import repository

''' ================================ Configs ================================ '''

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

def retornar_erro_cadastro(mensagem):
    return render_template(
        'retorno_cadastro_erro.html',
        erro=mensagem
    )

def retorno_cadastro_logado(mensagem):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))
    
    return render_template(
        'retorno_cadastro_erro_logado.html',
        erro=mensagem
    )

def retornar_erro_login(mensagem):
    return render_template(
        'retorno_login_erro.html',
        erro=mensagem
    )

''' ====================================================================
    ============================= GET templates ========================
    ====================================================================
'''

@app.route('/', methods=['GET'])
def inicio():
    return render_template('inicio.html')

@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/cadastro-alerta', methods=['GET'])
def cadastro_alerta():
    return render_template('config_alerta.html')
    
''' ====================================================================
    ============================= POSTs ================================ 
    ====================================================================
'''

''' ===== CADASTRO USUARIO ===== '''

@app.route('/cadastrar-usuario', methods=['POST'])
def cadastrar_usuario():
    # 1. Extração dos dados enviados pelo formulário HTML (request.form)
    nome = request.form.get('nome', '').strip()
    cpf_bruto = request.form.get('cpf', '').strip()
    email_bruto = request.form.get('email', '').strip()
    data_nasc = request.form.get('data_nascimento', '').strip()
    genero = request.form.get('genero', '').strip().upper()
    uf = request.form.get('uf', '').strip().upper()

    # 2. Validação de campos obrigatórios genéricos
    if not all([nome, cpf_bruto, email_bruto, data_nasc, genero, uf]):

        return retornar_erro_cadastro(
            "Todos os campos são obrigatorios."
        )
    
    if len(nome) < 3:
        return retornar_erro_cadastro(
            "O nome deve ter pelo menos 3 caracteres."
        )

    # 3. Validações de Regra de Negócio (Usando nosso validators.py)
    is_cpf_valido, msg_cpf = validators.validar_cpf(cpf_bruto)
    if not is_cpf_valido:
        return retornar_erro_cadastro(
            msg_cpf
        )
    
    cpf_limpo = validators.limpar_cpf(cpf_bruto) # Normalizamos o CPF para o banco

    is_email_valido, msg_email = validators.validar_email(email_bruto)
    if not is_email_valido:
        return retornar_erro_cadastro(
            msg_email
        )

    is_idade_valida, msg_idade = validators.validar_idade(data_nasc)
    if not is_idade_valida:
        return retornar_erro_cadastro(
            msg_idade
        )

    if genero not in validators.GENEROS_VALIDOS:
        return retornar_erro_cadastro(
            "Gênero inválido. Use F, M ou O."
        )

    if uf not in validators.UFS_VALIDAS:
        return retornar_erro_cadastro(
            "UF inválida."
        )

    # 4. Checagem de Conflitos (Regras de unicidade no Banco)
    if repository.buscar_por_cpf(cpf_limpo):
        return retornar_erro_cadastro(
            "Este CPF já esta cadastrado."
        )
        
    if repository.buscar_por_email(email_bruto.lower()):
        return retornar_erro_cadastro(
            "Este e-mail já esta cadastrado."
        )  

    # 5. Persistência
    dados_para_salvar = {
        'nome': nome,
        'cpf': cpf_limpo,
        'email': email_bruto,
        'data_nascimento': data_nasc,
        'genero': genero,
        'uf': uf
    }
    
    usuario_salvo = repository.salvar_usuario(dados_para_salvar)

    session['usuario_id'] = usuario_salvo['id']
    return redirect(url_for('cadastro_alerta'))


@app.route('/atualizar_cadastro', methods=['POST'])
def alterar_dados_usuario():

    # herdando o id do usuário gerado no cadastro
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))
    
    # 1. Extração dos dados enviados pelo formulário HTML (request.form)
    email_bruto = request.form.get('email', '').strip()
    uf = request.form.get('uf', '').strip().upper()

    # 2. Validação de campos obrigatórios genéricos
    if not all([email_bruto, uf]):
        return retorno_cadastro_logado(
            "Todos os campos são obrigatorios."
        )
    
    is_email_valido, msg_email = validators.validar_email(email_bruto)
    if not is_email_valido:
        return retorno_cadastro_logado(
            msg_email
        )
    if uf not in validators.UFS_VALIDAS:
        return retorno_cadastro_logado(
            "UF inválida."
        )
    '''    
    if repository.buscar_por_email(email_bruto.lower()):
        # checar se é o email é o do usuário logado:
            # se sim: posso fazer update em cima do email atual?
            # else: retorno_cadastro_logado(mensagem)

        

        return retorno_cadastro_logado(
            "Este e-mail já esta cadastrado."
        )
    '''
    usuario_existente = repository.buscar_por_email(email_bruto.lower())
    if usuario_existente and usuario_existente.get('id') != usuario_id:
        return retorno_cadastro_logado(
            "Este e-mail já esta cadastrado."
        )
    # 5. Persistência
    dados_para_salvar = {
        'usuario_id': usuario_id,        
        'email': email_bruto,
        'uf': uf
    }

    usuario_atualizado = repository.atualizar_cadastro_usuario(dados_para_salvar)

    return redirect(url_for('alterar_cadastro'))


''' ===== CADASTRO ALERTA ===== '''

@app.route('/configurar-alerta', methods=['POST'])
def config_alerta ():
    # herdando o id do usuário gerado no cadastro
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    tipo = request.form.get('tipo', '').strip().upper()
    percentual = float(request.form.get('pct', 0)) / 100

    # Verifica se já existe configuração para este usuário
    alerta_existente = repository.buscar_config_alerta_por_usuario(usuario_id)

    dados = {
        'usuario_id': usuario_id,
        'tipo': tipo,
        'percentual': percentual
    }
    if alerta_existente:
        repository.atualizar_alerta(dados)
        return redirect(url_for('alterar_alerta'))
    else: 
        alerta_salvo = repository.salvar_alerta(dados) 
        return redirect(url_for('login'))


''' ========== LOGIN ========== '''

@app.route('/fazer-login', methods=['POST'])
def fazer_login():
    session.clear()
    email_bruto = request.form.get('email', '').strip()
    # ... (suas validações de e-mail e busca de usuário continuam iguais) ...

    usuario = repository.buscar_por_email(email_bruto.lower())
    if not usuario:
        return retornar_erro_login("E-mail não encontrado no sistema.")

    usuario_id = usuario.get('id')
    session['usuario_id'] = usuario_id

    return redirect(url_for('menu'))


''' ========== MENU ========== '''

@app.route('/menu', methods=['GET'])
def menu():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    # Chamando a função auxiliar e desempacotando de uma vez só!
    ultimo_preco, tipo_moeda, ultimo_alerta = repository.ultimo_preco_e_alerta(usuario_id)
    configs = repository.buscar_config_alerta_por_usuario(usuario_id)
    config_alerta = configs[0] if configs else None
    return render_template(
        'menu.html',
        ultimo_preco=ultimo_preco,
        tipo_moeda=tipo_moeda,
        ultimo_alerta=ultimo_alerta,
        config_alerta=config_alerta        
    )


@app.route('/sair', methods=['POST'])
def sair():   
    session.clear()

    return redirect(url_for('inicio'))

@app.route('/alterar-alerta', methods=['GET'])
def alterar_alerta():
    
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))
    
    # Chamando a função auxiliar e desempacotando de uma vez só!
    ultimo_preco, tipo_moeda, ultimo_alerta = repository.ultimo_preco_e_alerta(usuario_id)
    configs = repository.buscar_config_alerta_por_usuario(usuario_id)
    config_alerta = configs[0] if configs else None    
    
    return render_template(
        'config_alerta_logado.html',
        ultimo_preco=ultimo_preco,
        tipo_moeda=tipo_moeda,
        ultimo_alerta=ultimo_alerta,
        config_alerta=config_alerta 
    )

@app.route('/alterar-cadastro', methods=['GET'])
def alterar_cadastro():
    
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))
    
    # Chamando a função auxiliar e desempacotando de uma vez só!
    ultimo_preco, tipo_moeda, ultimo_alerta = repository.ultimo_preco_e_alerta(usuario_id)
    
    # ''' EM IMPLEMENTACAO
    configs = repository.buscar_config_usuario(usuario_id)
    config_usuario = configs[0] if configs else None    
    # '''

    '''
    return render_template(
        'config_cadastro_logado.html',
        ultimo_preco=ultimo_preco,
        tipo_moeda=tipo_moeda,
        ultimo_alerta=ultimo_alerta
    )
    '''

    
    # print(
    #     f"\n"
    #     f"Retorno das variáveis:\n"
    #     f"    configs = repository.buscar_config_usuario(usuario_id)\n"
    #     f"      {configs}\n"
    #     f"\n"
    #     f"    config_alerta = configs[0] if configs else None:\n"
    #     f"      {config_usuario}\n"
    #     f""
    # )
    
    return render_template(
        'config_cadastro_logado.html',
        ultimo_preco=ultimo_preco,
        tipo_moeda=tipo_moeda,
        ultimo_alerta=ultimo_alerta,
        config_usuario=config_usuario 
    )
    


@app.route('/historico', methods=['GET'])
def historico_alertas():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))

    ultimo_preco, tipo_moeda, ultimo_alerta = repository.ultimo_preco_e_alerta(usuario_id)

    periodo_selecionado = validators.normalizar_periodo(request.args.get('periodo'))
    serie_preco = repository.buscar_serie_preco_historico(periodo_selecionado)
    alertas_historico = repository.buscar_ultimos_alertas_formatados(usuario_id, limite=10)

    return render_template(
        'historico.html',
        periodo_selecionado=periodo_selecionado,
        serie_preco=serie_preco,
        alertas_historico=alertas_historico,
        ultimo_preco=ultimo_preco,
        tipo_moeda=tipo_moeda,
        ultimo_alerta=ultimo_alerta
    )

''' ====================================================================
    ====================== INICIALIZAÇÃO DO WORKER ===================== 
    ====================================================================
'''

def iniciar_worker_background():
    # Evita que o worker duplique threads por causa do reloader do Flask (Werkzeug)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        worker_thread = threading.Thread(target=iniciar_monitoramento, daemon=True)
        worker_thread.start()

if __name__ == '__main__':
    # ''' COMENTADO PARA EVITAR FICAR CHAMANDO O WORKER ATOA ENQUANTO IMPLEMENTO O MENU  
    # Dispara a thread em paralelo antes de ligar o servidor web
    iniciar_worker_background()

    # Inicia o servidor web do Flask
    app.run(debug=True, port=5000)
