# app.py

'''
# app.py: 
/ orquestra a aplicação WEB
/ cria o fluxo apartado de acionamento do worker (a ser implementado agora)
'''
from flask import Flask, request, jsonify, render_template, session
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

    return render_template(
        'config_alerta.html',
        email = email_bruto,
        nome = nome)

''' ===== CADASTRO ALERTA ===== '''

@app.route('/configurar-alerta', methods=['POST'])
def config_alerta ():
    tipo = request.form.get('tipo', '').strip().upper()
    pct = float(request.form.get('pct', 0))
    percentual = float(pct / 100)

    # herdando o id do usuário gerado no cadastro
    usuario_id = session.get('usuario_id')

    dados_para_salvar = {
        'usuario_id': usuario_id,
        'tipo': tipo,
        'percentual': percentual
    }

    alerta_salvo = repository.salvar_alerta(dados_para_salvar)

    
    return render_template('retorno_cadastro_sucesso.html')

''' ========== LOGIN ========== '''

@app.route('/fazer-login', methods=['POST'])
def fazer_login():
    email_bruto = request.form.get('email', '').strip()
    # ... (suas validações de e-mail e busca de usuário continuam iguais) ...

    usuario = repository.buscar_por_email(email_bruto.lower())
    if not usuario:
        return retornar_erro_login("E-mail não encontrado no sistema.")

    usuario_id = usuario.get('id')
    nome = usuario.get('nome')
    session['usuario_id'] = usuario_id

    # ---- NOVO: Buscando os dados para injetar no menu ----
    # 1. Pega o último preço do Bitcoin salvo pelo worker
    ultimo_preco = repository.buscar_ultimo_preco() # Retorna {'preco_reais': ..., 'preco_dolar': ...} ou None

    # 2. Pega as configurações de alerta do usuário para saber se ele usa REAIS ou DOLAR
    alertas_usuario = repository.buscar_config_alerta_por_usuario(usuario_id) 
    tipo_moeda = alertas_usuario[0]['tipo'] if alertas_usuario else 'REAIS' # Padrão Reais se não tiver

    # 3. Pega o histórico de alertas disparados para este usuário
    historico_usuario = repository.buscar_historico_por_usuario(usuario_id)
    ultimo_alerta = historico_usuario[0] if historico_usuario else None

    return render_template(
        'menu.html',
        nome=nome,
        ultimo_preco=ultimo_preco,
        tipo_moeda=tipo_moeda,
        ultimo_alerta=ultimo_alerta
    )


''' ====================================================================
    ====================== INICIALIZAÇÃO DO WORKER ===================== 
    ====================================================================
'''

# ''' COMENTADO PARA EVITAR FICAR CHAMANDO O WORKER ATOA ENQUANTO IMPLEMENTO O MENU
def iniciar_worker_background():
    # Evita que o worker duplique threads por causa do reloader do Flask (Werkzeug)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        worker_thread = threading.Thread(target=iniciar_monitoramento, daemon=True)
        worker_thread.start()
# '''

if __name__ == '__main__':
    # ''' COMENTADO PARA EVITAR FICAR CHAMANDO O WORKER ATOA ENQUANTO IMPLEMENTO O MENU  
    # Dispara a thread em paralelo antes de ligar o servidor web
    iniciar_worker_background()
    # '''

    # Inicia o servidor web do Flask
    app.run(debug=True, port=5000)
