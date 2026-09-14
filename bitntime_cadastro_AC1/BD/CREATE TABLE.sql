-- Cria a tabela chamada 'usuarios' no banco de dados
CREATE TABLE usuarios (
    -- Chave primária: ID único inteiro que incrementa automaticamente a cada novo registro
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Nome do usuário: Texto de até 150 caracteres, de preenchimento obrigatório
    nome VARCHAR(150) NOT NULL,
    
    -- CPF: Texto fixo de 11 caracteres, obrigatório e sem duplicidade entre usuários
    cpf CHAR(11) NOT NULL UNIQUE,
    
    -- E-mail: Texto de até 255 caracteres, obrigatório e sem duplicidade entre usuários
    email VARCHAR(255) NOT NULL UNIQUE,
    
    -- Data de nascimento: Armazena data (AAAA-MM-DD), de preenchimento obrigatório
    data_nascimento DATE NOT NULL,
    
    -- Gênero: Permite apenas um dos valores definidos ('F', 'M' ou 'O'), obrigatório
    genero ENUM('F', 'M', 'O') NOT NULL,
    
    -- UF (Estado): Permite apenas uma das siglas dos 26 estados ou DF, obrigatório
    uf ENUM(
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
        'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
        'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ) NOT NULL,
    
    -- Data/hora de criação: Define automaticamente o momento do cadastro do registro
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Data/hora de atualização: Atualiza automaticamente a cada alteração no registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);