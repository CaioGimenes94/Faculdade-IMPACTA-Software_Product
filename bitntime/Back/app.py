# app.py
from flask import Flask, request, jsonify, render_template
import validators
import repository

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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
        return jsonify({"erro": "Todos os campos são obrigatorios."}), 400
    
    if len(nome) < 3:
        return jsonify({"erro": "O nome deve ter pelo menos 3 caracteres."}), 400

    # 3. Validações de Regra de Negócio (Usando nosso validators.py)
    is_cpf_valido, msg_cpf = validators.validar_cpf(cpf_bruto)
    if not is_cpf_valido:
        return jsonify({"erro": msg_cpf}), 400
    cpf_limpo = validators.limpar_cpf(cpf_bruto) # Normalizamos o CPF para o banco

    is_email_valido, msg_email = validators.validar_email(email_bruto)
    if not is_email_valido:
        return jsonify({"erro": msg_email}), 400

    is_idade_valida, msg_idade = validators.validar_idade(data_nasc)
    if not is_idade_valida:
        return jsonify({"erro": msg_idade}), 400

    if genero not in validators.GENEROS_VALIDOS:
        return jsonify({"erro": "Gênero inválido. Use F, M ou O."}), 400

    if uf not in validators.UFS_VALIDAS:
        return jsonify({"erro": "UF inválida."}), 400

    # 4. Checagem de Conflitos (Regras de unicidade no Banco)
    if repository.buscar_por_cpf(cpf_limpo):
        # HTTP 409 = Conflict (O dado já existe)
        return jsonify({"erro": "Este CPF ja esta cadastrado."}), 409
        
    if repository.buscar_por_email(email_bruto.lower()):
        return jsonify({"erro": "Este e-mail ja esta cadastrado."}), 409

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

    # 6. Resposta de Sucesso
    # HTTP 201 = Created (Recurso criado com sucesso)
    return jsonify({
        "mensagem": "Usuario cadastrado com sucesso!",
        "usuario_id": usuario_salvo['id']
    }), 201

if __name__ == '__main__':
    # Rodando o servidor local na porta 5000
    app.run(debug=True, port=5000)