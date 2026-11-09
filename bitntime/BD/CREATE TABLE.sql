
-- -- -- -- -- -- -- -- -- -- -- -- SPRINT 1 -- -- -- -- -- -- -- -- -- -- -- --

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

-- -- -- -- -- -- -- -- -- -- -- -- SPRINT 2 -- -- -- -- -- -- -- -- -- -- -- --


CREATE TABLE config_alerta (
    id INT AUTO_INCREMENT PRIMARY KEY,     -- Identificador da configuração.
    usuario_id INT NOT NULL,     -- FK da tabela usuario: Identificador do usuário associado.
    tipo ENUM('REAIS', 'DOLAR') NOT NULL,    -- Moeda de referência (reais ou dólares).
    percentual DECIMAL(5, 4) NOT NULL,    -- Percentual de variação desejado.
    -- preco_base DECIMAL(18, 8) NULL,       -- Preço de referência atual para o cálculo da variação -- coluna implementada na sprint 3 com ALTER TABLE 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- Data/hora de criação: Define automaticamente o momento do cadastro do registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,    -- Data/hora de atualização: Atualiza automaticamente a cada alteração no registro

    CONSTRAINT fk_config_alerta_usuario 
        FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) 
        ON DELETE CASCADE
);
-- -- -- -- -- -- -- -- -- -- -- -- SPRINT 3 -- -- -- -- -- -- -- -- -- -- -- --

ALTER TABLE projeto_bitntime.config_alerta 
ADD COLUMN preco_base DECIMAL(18, 8) NULL AFTER percentual;

CREATE TABLE historico_alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,     -- Identificador da configuração.
    config_alerta_id INT NOT NULL,     -- FK da tabela config_alerta: Identificador da configuração dos alertas do usuário associado.
    preco_dolar DECIMAL(18, 8) NULL,      -- Aceita NULL caso não seja consultado o par em USD
    preco_reais DECIMAL(18, 8) NULL,      -- Alta precisão (18 dígitos no total, 8 após a vírgula) -- aqui consultei na binance como está vindo o dado :{"symbol":"BTCBRL","price":"420650.00000000"}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- Data/hora de criação: Define automaticamente o momento do cadastro do registro

    CONSTRAINT fk_historico_gatilhos_config_alerta 
        FOREIGN KEY (config_alerta_id) 
        REFERENCES config_alerta(id) -- nome da minha tabela em que o usuario configura como quer ser alertado.
        ON DELETE CASCADE 
);

ALTER TABLE projeto_bitntime.historico_alertas 
ADD COLUMN direcao ENUM('ALTA', 'QUEDA') NOT NULL AFTER preco_dolar;
-- -- -- -- -- -- -- -- -- -- -- -- SPRINT 4 -- -- -- -- -- -- -- -- -- -- -- --

CREATE TABLE preco_btc (
    id INT AUTO_INCREMENT PRIMARY KEY,     -- Identificador da do preço. foi pensado já em auto_increment para a  sprint 4 será inserido e não mais 'upado',
    preco_dolar DECIMAL(18, 8) NULL,      -- Aceita NULL caso não seja consultado o par em USD
    preco_reais DECIMAL(18, 8) NULL,      -- Alta precisão (18 dígitos no total, 8 após a vírgula) -- aqui consultei na binance como está vindo o dado :{"symbol":"BTCBRL","price":"420650.00000000"}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- Data/hora de criação: Define automaticamente o momento do cadastro do registro
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP    -- Data/hora de atualização: Atualiza automaticamente a cada alteração no registro
    
);

