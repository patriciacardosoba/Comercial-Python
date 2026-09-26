-- =====================================================================
-- PROJETO DE GESTÃO COMERCIAL - VENDAS, VISITAS E ENRIQUECIMENTO DOS DADOS DO IBGE NA BASE FILIAL
-- Módulo SQL: DDL, DML, DQL e DCL
-- =====================================================================

-- 1. MÓDULO DDL (Data Definition Language) - Criação de Estruturas e Tabelas
CREATE TABLE IF NOT EXISTS Calendario (
    Data DATE PRIMARY KEY,
    Dia INT,
    Mes INT,
    Nome_Mes VARCHAR(50),
    Ano INT,
    Num_Dia INT,
    Tipo_Dia VARCHAR(50),
    Semana_Comercial INT,
    Ano_Comercial INT,
    Mes_Comercial VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Filiais (
    Id_Filial INT PRIMARY KEY,
    Num_Filial VARCHAR(20),
    Regiao VARCHAR(100),
    Tipo VARCHAR(50),
    Core VARCHAR(50),
    Populacao_IBGE INT DEFAULT 0,
    PIB_PerCapita_IBGE DECIMAL(12,2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS Vendedores (
    Matricula_Especialista VARCHAR(50) PRIMARY KEY,
    Filial VARCHAR(20),
    Classificacao VARCHAR(50),
    FTE DECIMAL(5,2),
    Nome_Mes VARCHAR(20),
    Admitidos INT,
    Demitidos INT
);

CREATE TABLE IF NOT EXISTS Visitas (
    Id_Visita INT AUTO_INCREMENT PRIMARY KEY,
    Matricula VARCHAR(50),
    Data_Visita DATE,
    Data_Checkin DATE,
    FOREIGN KEY (Matricula) REFERENCES Vendedores(Matricula_Especialista)
);

CREATE TABLE IF NOT EXISTS Vendas (
    Id_Venda INT AUTO_INCREMENT PRIMARY KEY,
    Recurso VARCHAR(10),
    Matricula VARCHAR(50),
    Data_Venda DATE,
    Tipo_Estabelecimento VARCHAR(100),
    FOREIGN KEY (Matricula) REFERENCES Vendedores(Matricula_Especialista)
);


-- 2. MÓDULO DML (Data Manipulation Language) - Inserção e Enriquecimento IBGE
-- Atualização/Enriquecimento de dados demográficos externos (API do IBGE)
UPDATE Filiais 
SET Populacao_IBGE = 250000, PIB_PerCapita_IBGE = 45000.00 
WHERE Regiao = 'Sudeste';

UPDATE Filiais 
SET Populacao_IBGE = 180000, PIB_PerCapita_IBGE = 38000.00 
WHERE Regiao = 'Sul';


-- 3. MÓDULO DQL (Data Query Language) - Consultas de Business Intelligence
-- Consulta 1: Qual é a filial de melhor conversão de 2025?
SELECT 
    f.Regiao,
    f.Num_Filial,
    COUNT(v.Id_Venda) AS Total_Vendas,
    COUNT(vis.Id_Visita) AS Total_Visitas,
    (CAST(COUNT(v.Id_Venda) AS FLOAT) / NULLIF(COUNT(vis.Id_Visita), 0)) * 100 AS Taxa_Conversao_Pct
FROM Filiais f
LEFT JOIN Vendedores vend ON f.Num_Filial = vend.Filial
LEFT JOIN Vendas v ON vend.Matricula_Especialista = v.Matricula
LEFT JOIN Visitas vis ON vend.Matricula_Especialista = vis.Matricula
GROUP BY f.Regiao, f.Num_Filial
ORDER BY Taxa_Conversao_Pct DESC;

-- Consulta 2: Melhor Vendedor YTD por Volume de Vendas
SELECT 
    v.Matricula,
    COUNT(v.Id_Venda) AS Volume_Vendas_Total
FROM Vendas v
GROUP BY v.Matricula
ORDER BY Volume_Vendas_Total DESC
LIMIT 1;

-- Consulta 3: Mês com melhor performance em residência
SELECT 
    c.Mes_Comercial,
    COUNT(v.Id_Venda) AS Vendas_Residencia
FROM Vendas v
JOIN Calendario c ON v.Data_Venda = c.Data
WHERE v.Tipo_Estabelecimento LIKE '%Residência%' OR v.Tipo_Estabelecimento LIKE '%Residencial%'
GROUP BY c.Mes_Comercial
ORDER BY Vendas_Residencia DESC;


-- 4. MÓDULO DCL (Data Control Language) - Controlo de Segurança e Acessos
CREATE ROLE IF NOT EXISTS Analista_Comercial;
CREATE ROLE IF NOT EXISTS Diretor_Comercial;

GRANT SELECT ON Vendas TO Analista_Comercial;
GRANT SELECT ON Visitas TO Analista_Comercial;
GRANT SELECT, INSERT, UPDATE ON Filiais TO Analista_Comercial;

GRANT ALL PRIVILEGES ON DATABASE comercio_db TO Diretor_Comercial;
