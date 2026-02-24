{{ config(materialized='table') }}

WITH prudential AS (
    SELECT 
        codigo as codigo_origem,
        instituicao as nome,
        segmento_resolucao as segmento,
        'Conglomerado Prudencial' as tipo_instituicao,
        cidade, uf, regiao,
        tipo_de_controle,
        consolidado_bancario,
        NULL as tipo_de_instituicao,
        NULL as nome_conglomerado
    FROM {{ source('silver', 'prudential_conglomerates_summary') }}
),

financial AS (
    SELECT 
        codigo as codigo_origem,
        instituicao as nome,
        segmento_resolucao as segmento,
        'Conglomerado Financeiro' as tipo_instituicao,
        cidade, uf, regiao,
        tipo_de_controle,
        consolidado_bancario,
        NULL as tipo_de_instituicao,
        NULL as nome_conglomerado
    FROM {{ source('silver', 'financial_conglomerates_summary') }}
),

individual AS (
    SELECT 
        codigo as codigo_origem,
        instituicao as nome,
        NULL as segmento,
        'Instituicao Individual' as tipo_instituicao,
        cidade, uf, regiao,
        tipo_de_controle,
        consolidado_bancario,
        tipo_de_instituicao,
        conglomerado as nome_conglomerado
    FROM {{ source('silver', 'individual_institutions_summary') }}
),

exchange AS (
    SELECT 
        codigo as codigo_origem,
        instituicao as nome,
        segmento_resolucao as segmento,
        'Instituição de Câmbio' as tipo_instituicao,
        cidade, uf, regiao,
        tipo_de_controle,
        consolidado_bancario,
        NULL as tipo_de_instituicao,
        NULL as nome_conglomerado
    FROM {{ source('silver', 'foreign_exchange_quarterly_foreign_currency_flow') }}
),

-- Fallback: instituições presentes nas tabelas de portfólio (SCR) mas ausentes dos resumos.
-- Isso garante integridade referencial completa para todas as tabelas fato.
portfolio_fallback AS (
    SELECT DISTINCT
        codigo as codigo_origem,
        instituicao as nome,
        segmento_resolucao as segmento,
        'Conglomerado Financeiro (SCR)' as tipo_instituicao,
        cidade, uf, regiao,
        tipo_de_controle,
        consolidado_bancario,
        NULL as tipo_de_instituicao,
        NULL as nome_conglomerado
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_indexer') }}
    WHERE codigo NOT IN (
        SELECT DISTINCT codigo FROM {{ source('silver', 'financial_conglomerates_summary') }}
    )
),

portfolio_fallback_standard AS (
    SELECT DISTINCT
        codigo as codigo_origem,
        instituicao as nome,
        segmento_resolucao as segmento,
        'Conglomerado Financeiro' as tipo_instituicao,
        cidade, uf, regiao,
        tipo_de_controle,
        consolidado_bancario,
        NULL as tipo_de_instituicao,
        NULL as nome_conglomerado
    FROM {{ source('silver', 'financial_conglomerates_portfolio_indexer') }}
    WHERE codigo NOT IN (
        SELECT DISTINCT codigo FROM {{ source('silver', 'financial_conglomerates_summary') }}
    )
),

unificacao AS (
    -- Conglomerados Prudenciais - Resumo
    SELECT codigo_origem, nome, segmento, tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, tipo_de_instituicao, nome_conglomerado FROM prudential
    UNION
    -- Conglomerados Prudenciais - Ativo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Prudencial' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'prudential_conglomerates_assets') }}
    UNION
    -- Conglomerados Prudenciais - Passivo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Prudencial' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'prudential_conglomerates_liabilities') }}
    UNION
    -- Conglomerados Prudenciais - Demonstração de Resultado
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Prudencial' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'prudential_conglomerates_income_statement') }}
    UNION
    -- Conglomerados Prudenciais - Informações de Capital
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Prudencial' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'prudential_conglomerates_capital_information') }}
    UNION
    -- Conglomerados Prudenciais - Segmentação
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Prudencial' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'prudential_conglomerates_segmentation') }}

    UNION

    -- Conglomerados Financeiros - Resumo
    SELECT codigo_origem, nome, segmento, tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, tipo_de_instituicao, nome_conglomerado FROM financial
    UNION
    -- Conglomerados Financeiros - Ativo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_assets') }}
    UNION
    -- Conglomerados Financeiros - Passivo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_liabilities') }}
    UNION
    -- Conglomerados Financeiros - Demonstração de Resultado
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_income_statement') }}
    UNION
    -- Conglomerados Financeiros - Informações de Capital
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_capital_information') }}

    UNION

    -- SCR Portfolios (Financial Conglomerates) - Carteira PJ Modalidade e Prazo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_portfolio_individuals_type_maturity') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Carteira PJ Modalidade e Prazo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_type_maturity') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Carteira PJ Atividade Econômica
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_economic_activity') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Carteira PJ Porte
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_business_size') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Nível de Risco
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_portfolio_risk_level') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Região Geográfica
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_portfolio_geographic_region') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Indexador
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_portfolio_indexer') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Quantidade de Clientes
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_portfolio_number_clients_operations') }}

    UNION

    -- SCR Portfolios Independent (Financial Conglomerates SCR) - Carteira PF Modalidade e Prazo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_individuals_type_maturity') }}
    UNION
    -- SCR Portfolios Independent (Financial Conglomerates SCR) - Carteira PJ Modalidade e Prazo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_type_maturity') }}
    UNION
    -- SCR Portfolios Independent (Financial Conglomerates SCR) - Carteira PJ Atividade Econômica
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_economic_activity') }}
    UNION
    -- SCR Portfolios Independent (Financial Conglomerates SCR) - Carteira PJ Porte
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_business_size') }}
    UNION
    -- SCR Portfolios Independent (Financial Conglomerates SCR) - Nível de Risco
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_risk_level') }}
    UNION
    -- SCR Portfolios Independent (Financial Conglomerates SCR) - Região Geográfica
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_geographic_region') }}
    UNION
    -- SCR Portfolios Independent (Financial Conglomerates SCR) - Indexador
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_indexer') }}
    UNION
    -- SCR Portfolios Independent (Financial Conglomerates SCR) - Quantidade de Clientes
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro (SCR)' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, segmento as tipo_de_instituicao, NULL as nome_conglomerado FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_number_clients_operations') }}

    UNION

    -- Financial Conglomerates Portfolios (Standard) - Carteira PF Modalidade e Prazo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_portfolio_individuals_type_maturity') }}
    UNION
    -- Financial Conglomerates Portfolios (Standard) - Carteira PJ Modalidade e Prazo
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_type_maturity') }}
    UNION
    -- Financial Conglomerates Portfolios (Standard) - Carteira PJ Atividade Econômica
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_economic_activity') }}
    UNION
    -- Financial Conglomerates Portfolios (Standard) - Carteira PJ Porte
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_business_size') }}
    UNION
    -- Financial Conglomerates Portfolios (Standard) - Nível de Risco
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_portfolio_risk_level') }}
    UNION
    -- Financial Conglomerates Portfolios (Standard) - Região Geográfica
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_portfolio_geographic_region') }}
    UNION
    -- Financial Conglomerates Portfolios (Standard) - Indexador
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_portfolio_indexer') }}
    UNION
    -- Financial Conglomerates Portfolios (Standard) - Quantidade de Clientes
    SELECT codigo as codigo_origem, instituicao as nome, segmento_resolucao as segmento, 'Conglomerado Financeiro' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, NULL, NULL FROM {{ source('silver', 'financial_conglomerates_portfolio_number_clients_operations') }}

    UNION

    -- Instituições Individuais - Resumo
    SELECT codigo_origem, nome, segmento, tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, tipo_de_instituicao, nome_conglomerado FROM individual
    UNION
    -- Instituições Individuais - Ativo
    SELECT codigo as codigo_origem, instituicao as nome, NULL as segmento, 'Instituicao Individual' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, tipo_de_instituicao, conglomerado FROM {{ source('silver', 'individual_institutions_assets') }}
    UNION
    -- Instituições Individuais - Passivo
    SELECT codigo as codigo_origem, instituicao as nome, NULL as segmento, 'Instituicao Individual' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, tipo_de_instituicao, conglomerado FROM {{ source('silver', 'individual_institutions_liabilities') }}
    UNION
    -- Instituições Individuais - Demonstração de Resultado
    SELECT codigo as codigo_origem, instituicao as nome, NULL as segmento, 'Instituicao Individual' as tipo_instituicao, cidade, uf, regiao, tipo_de_controle, consolidado_bancario, tipo_de_instituicao, conglomerado FROM {{ source('silver', 'individual_institutions_income_statement') }}

    UNION

    -- Câmbio
    SELECT * FROM exchange
    UNION
    -- Fallback SCR
    SELECT * FROM portfolio_fallback
    UNION
    -- Fallback Standard
    SELECT * FROM portfolio_fallback_standard
)
,

final_with_id AS (
    SELECT
        {{ generate_instituicao_id('codigo_origem', 'tipo_instituicao') }} as id_instituicao,
        codigo_origem,
        nome,
        tipo_instituicao,
        CASE 
            WHEN tipo_instituicao = 'Instituicao Individual' THEN 'Instituições Individuais'
            WHEN tipo_instituicao IN ('Conglomerado Financeiro', 'Conglomerado Financeiro (SCR)') THEN 'Conglomerados Financeiros e Instituições Independentes'
            WHEN tipo_instituicao = 'Conglomerado Prudencial' THEN 'Conglomerados Prudenciais e Instituições Independentes'
            WHEN tipo_instituicao = 'Instituição de Câmbio' THEN 'Instituições com Operações de Câmbio'
        END AS tipo_relatorio_bcb,
        md5(cast(lower(nullif(segmento, '')) as varchar)) as id_segmento,
        md5(cast(coalesce(cidade, '') || coalesce(uf, '') || coalesce(regiao, '') as varchar)) as id_localizacao,
        md5(cast(nullif(tipo_de_controle, '') as varchar)) as id_controle,
        md5(cast(lower(nullif(consolidado_bancario, '')) as varchar)) as id_consolidado,
        md5(cast(nullif(tipo_de_instituicao, '') as varchar)) as id_classe,
        nome_conglomerado
    FROM unificacao
)

SELECT * FROM final_with_id
QUALIFY row_number() OVER (PARTITION BY id_instituicao ORDER BY nome DESC, codigo_origem DESC) = 1
