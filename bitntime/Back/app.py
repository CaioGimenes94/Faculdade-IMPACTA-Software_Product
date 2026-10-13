# app.py
from flask import Flask, request, jsonify, render_template, session
import os
from dotenv import load_dotenv
import validators
import repository

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

''' ================================ GET templates ================================ '''


@app.route('/', methods=['GET'])
def inicio():
    return render_template('inicio.html')

@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/login', methods=['GET'])
def tela_login():
    return render_template('login.html')


''' ================================ CADASTRO USUARIO ================================ '''

@app.route('/api/usuarios', methods=['POST'])
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
        # HTTP 400 = Bad Request (O cliente enviou dados incompletos)
        # return jsonify({"erro": "Todos os campos são obrigatorios."}), 400
        return render_template(
        'retorno_cadastro_erro.html',
        erro = "Todos os campos são obrigatorios."
        )
    
    if len(nome) < 3:
        #return jsonify({"erro": "O nome deve ter pelo menos 3 caracteres."}), 400
        return render_template(
        'retorno_cadastro_erro.html',
        erro = "O nome deve ter pelo menos 3 caracteres."
        )

    # 3. Validações de Regra de Negócio (Usando nosso validators.py)
    is_cpf_valido, msg_cpf = validators.validar_cpf(cpf_bruto)
    if not is_cpf_valido:
        #return jsonify({"erro": msg_cpf}), 400
        return render_template(
        'retorno_cadastro_erro.html',
        erro = msg_cpf
        )
    
    cpf_limpo = validators.limpar_cpf(cpf_bruto) # Normalizamos o CPF para o banco

    is_email_valido, msg_email = validators.validar_email(email_bruto)
    if not is_email_valido:
        #return jsonify({"erro": msg_email}), 400
        return render_template(
        'retorno_cadastro_erro.html',
        erro = msg_email
        )

    is_idade_valida, msg_idade = validators.validar_idade(data_nasc)
    if not is_idade_valida:
        # return jsonify({"erro": msg_idade}), 400
        return render_template(
        'retorno_cadastro_erro.html',
        erro = msg_idade
        )

    if genero not in validators.GENEROS_VALIDOS:
        # return jsonify({"erro": "Gênero inválido. Use F, M ou O."}), 400
        return render_template(
        'retorno_cadastro_erro.html',
        erro = "Gênero inválido. Use F, M ou O."
        )

    if uf not in validators.UFS_VALIDAS:
        # return jsonify({"erro": "UF inválida."}), 400
        return render_template(
        'retorno_cadastro_erro.html',
        erro = "UF inválida."
        )

    # 4. Checagem de Conflitos (Regras de unicidade no Banco)
    if repository.buscar_por_cpf(cpf_limpo):
        # HTTP 409 = Conflict (O dado já existe)
        # return jsonify({"erro": "Este CPF ja esta cadastrado."}), 409
        return render_template(
        'retorno_cadastro_erro.html',
        erro = "Este CPF já esta cadastrado."
        )
        
    if repository.buscar_por_email(email_bruto.lower()):
        # return jsonify({"erro": "Este e-mail ja esta cadastrado."}), 409
        return render_template(
        'retorno_cadastro_erro.html',
        erro = "Este e-mail já esta cadastrado."
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

    # 6. Resposta de Sucesso
    # HTTP 201 = Created (Recurso criado com sucesso)
    '''
    return jsonify({
        "mensagem": "Usuario cadastrado com sucesso!",
        "usuario_id": usuario_salvo['id']
    }), 201
    '''
    id = usuario_salvo['id']
    return render_template(
        'config_alerta.html',
        email = email_bruto,
        nome = nome)

''' ================================ CADASTRO ALERTA ================================ '''

@app.route('/api/config_alerta', methods=['POST'])
def config_alerta ():
    tipo = request.form.get('tipo', '').strip().upper()
    pct = float(request.form.get('pct', 0))
    
    percentual = float(pct / 100)

    usuario_id = session.get('usuario_id')

    print(percentual)

    # '''
    dados_para_salvar = {
        'usuario_id': usuario_id,
        'tipo': tipo,
        'percentual': percentual
    }

    alerta_salvo = repository.salvar_alerta(dados_para_salvar)

    # '''
    return render_template('menu.html')

''' ================================ LOGIN ================================ '''


@app.route('/api/login', methods=['POST'])
def fazer_login():

    email_bruto = request.form.get('email', '').strip()

    if not email_bruto:
        return jsonify({"erro": "O campo de e-mail é obrigatório."}), 400
    
    is_email_valido, msg_email = validators.validar_email(email_bruto)
    if not is_email_valido:
        return jsonify({"erro": msg_email}), 400
 
    # Busca o usuário no banco pelo e-mail
    usuario = repository.buscar_por_email(email_bruto.lower())

    if not usuario:
        return jsonify({
            "erro": "E-mail não encontrado no sistema."
        }), 404

    # Recupera os dados do usuário
    nome = usuario.get('nome')

    # Retorna a página com os dados do usuário
    return render_template(
        'menu.html',
        nome=nome
    )



if __name__ == '__main__':
    # Rodando o servidor local na porta 5000
    app.run(debug=True, port=5000)
    