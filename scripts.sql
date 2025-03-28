CREATE TABLE IF NOT EXISTS operadoras (
    Registro_ANS VARCHAR(20) PRIMARY KEY,
    CNPJ VARCHAR(20),
    Razao_Social VARCHAR(255),
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(100),
    Logradouro VARCHAR(255),
    Numero VARCHAR(20),
    Complemento VARCHAR(255),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    UF CHAR(2),
    CEP VARCHAR(20),
    DDD VARCHAR(5),
    Telefone VARCHAR(20),
    Fax VARCHAR(20),
    Endereco_eletronico VARCHAR(255),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(255),
    Regiao_de_Comercializacao TEXT,
    Data_Registro_ANS DATE
);

CREATE TABLE IF NOT EXISTS despesas_medicas (
    id SERIAL PRIMARY KEY, 
    DATA DATE NOT NULL,
    REG_ANS VARCHAR(20),
    CD_CONTA_CONTABIL VARCHAR(50),
    DESCRICAO TEXT,
    VL_SALDO_INICIAL DECIMAL(15,2),
    VL_SALDO_FINAL DECIMAL(15,2),
    Ano INT,
    Trimestre INT,
    FOREIGN KEY (REG_ANS) REFERENCES operadoras(Registro_ANS)
);

LOAD DATA INFILE '/dados_operadoras/Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'dados_tratados.csv'
INTO TABLE despesas_medicas
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Top 10 operadoras com maiores despesas no último trimestre
WITH ultimo_trimestre AS (
    SELECT MAX(Ano) AS Ano, MAX(Trimestre) AS Trimestre
    FROM despesas_medicas
)
SELECT d.REG_ANS, o.Nome_Fantasia, SUM(d.VL_SALDO_FINAL) AS Total_Despesas
FROM despesas_medicas d
JOIN operadoras o ON d.REG_ANS = o.Registro_ANS
JOIN ultimo_trimestre ut ON d.Ano = ut.Ano AND d.Trimestre = ut.Trimestre
WHERE d.DESCRICAO LIKE '%EVENTOS/SINISTROS CONHECIDOS%'
GROUP BY d.REG_ANS, o.Nome_Fantasia
ORDER BY Total_Despesas DESC
LIMIT 10;

-- Top 10 operadoras com maiores despesas no último ano
WITH ultimo_ano AS (
    SELECT MAX(Ano) AS Ano FROM despesas_medicas
)
SELECT d.REG_ANS, o.Nome_Fantasia, SUM(d.VL_SALDO_FINAL) AS Total_Despesas
FROM despesas_medicas d
JOIN operadoras o ON d.REG_ANS = o.Registro_ANS
JOIN ultimo_ano ua ON d.Ano = ua.Ano
WHERE d.DESCRICAO LIKE '%EVENTOS/SINISTROS CONHECIDOS%'
GROUP BY d.REG_ANS, o.Nome_Fantasia
ORDER BY Total_Despesas DESC
LIMIT 10;

