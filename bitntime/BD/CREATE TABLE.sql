-- Criação da tabela da AC1
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    genero ENUM('F', 'M', 'O') NOT NULL,
    uf ENUM(
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
        'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
        'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ) NOT NULL,
   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Criação da tabela da AC2
CREATE TABLE config_alerta (
    id INT AUTO_INCREMENT PRIMARY KEY,     -- Identificador da configuração.
    usuario_id INT NOT NULL,     -- FK da tabela usuario: Identificador do usuário associado.
    tipo ENUM('REAIS', 'DOLAR') NOT NULL,    -- Moeda de referência (reais ou dólares).
    percentual DECIMAL(5, 4) NOT NULL,    -- Percentual de variação desejado.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- Data/hora de criação: Define automaticamente o momento do cadastro do registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,    -- Data/hora de atualização: Atualiza automaticamente a cada alteração no registro

    CONSTRAINT fk_config_alerta_usuario 
        FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) 
        ON DELETE CASCADE
);