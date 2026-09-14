# validators.py
import re
from datetime import datetime

# Constantes para validação
UFS_VALIDAS = {
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
}
GENEROS_VALIDOS = {'F', 'M', 'O'}

def limpar_cpf(cpf):
    """Remove pontuações do CPF, deixando apenas números."""
    return re.sub(r'[^0-9]', '', str(cpf))

def validar_cpf(cpf):
    """Valida o formato e os dígitos verificadores do CPF."""
    cpf = limpar_cpf(cpf)
    
    if len(cpf) != 11:
        return False, "O CPF deve conter exatamente 11 números."

    
    # Evita CPFs com todos os números iguais (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        return False, "CPF inválido."

# Cálculo matemático dos dígitos verificadores (Regra oficial do CPF) 
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if str(digito) != cpf[i]:
            return False, "CPF inválido (dígitos verificadores não conferem)."
            
              
    return True, ""
    

def validar_idade(data_nascimento_str):
    """Verifica se a data é válida e se a pessoa tem 18 anos ou mais."""
    try:
        # Tenta converter a string 'YYYY-MM-DD' que vem do HTML5 para data no Python
        data_nasc = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
    except ValueError:
        return False, "Formato de data inválido. Use AAAA-MM-DD."

    hoje = datetime.today().date()
    
    # Calcula a idade
    idade = hoje.year - data_nasc.year
    # Subtrai 1 ano se o aniversário ainda não ocorreu neste ano
    if (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day):
        idade -= 1
        
    if idade < 18:
        return False, "Usuario deve ter pelo menos 18 anos."
        
    return True, ""

def validar_email(email):
    """Validação básica de formato de e-mail"""
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(padrao, email):
        return False, "Formato de e-mail inválido."
    return True, ""