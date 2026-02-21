{{ config(materialized='table') }}

WITH datas_unicas AS (
    -- Conglomerados Prudenciais - Resumo
    SELECT DISTINCT data_base as data
    FROM {{ source('silver', 'prudential_conglomerates_summary') }}
    UNION
    -- Conglomerados Prudenciais - Ativo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'prudential_conglomerates_assets') }}
    UNION
    -- Conglomerados Prudenciais - Passivo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'prudential_conglomerates_liabilities') }}
    UNION
    -- Conglomerados Prudenciais - Demonstração de Resultado
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'prudential_conglomerates_income_statement') }}
    UNION
    -- Conglomerados Prudenciais - Informações de Capital
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'prudential_conglomerates_capital_information') }}
    UNION
    -- Conglomerados Prudenciais - Segmentação
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'prudential_conglomerates_segmentation') }}
    UNION
    -- Conglomerados Financeiros - Resumo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_summary') }}
    UNION
    -- Conglomerados Financeiros - Ativo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_assets') }}
    UNION
    -- Conglomerados Financeiros - Passivo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_liabilities') }}
    UNION
    -- Conglomerados Financeiros - Demonstração de Resultado
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_income_statement') }}
    UNION
    -- Conglomerados Financeiros - Informações de Capital
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_capital_information') }}
    UNION
    -- Instituições Individuais - Resumo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'individual_institutions_summary') }}
    UNION
    -- Instituições Individuais - Ativo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'individual_institutions_assets') }}
    UNION
    -- Instituições Individuais - Passivo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'individual_institutions_liabilities') }}
    UNION
    -- Instituições Individuais - Demonstração de Resultado
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'individual_institutions_income_statement') }}
    UNION
    -- Conglomerados Financeiros - Carteira PF Modalidade e Prazo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_portfolio_individuals_type_maturity') }}
    UNION
    -- Conglomerados Financeiros - Carteira PJ Modalidade e Prazo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_type_maturity') }}
    UNION
    -- Conglomerados Financeiros - Carteira PJ Atividade Econômica
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_economic_activity') }}
    UNION
    -- Conglomerados Financeiros - Carteira PJ Porte
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_business_size') }}
    UNION
    -- Conglomerados Financeiros - Nível de Risco
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_portfolio_risk_level') }}
    UNION
    -- Conglomerados Financeiros - Região Geográfica
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_portfolio_geographic_region') }}
    UNION
    -- Conglomerados Financeiros - Indexador
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_portfolio_indexer') }}
    UNION
    -- Conglomerados Financeiros - Quantidade de Clientes
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_portfolio_number_clients_operations') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Carteira PF Modalidade e Prazo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_individuals_type_maturity') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Carteira PJ Modalidade e Prazo
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_type_maturity') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Carteira PJ Atividade Econômica
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_economic_activity') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Carteira PJ Porte
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_business_size') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Nível de Risco
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_risk_level') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Região Geográfica
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_geographic_region') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Indexador
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_indexer') }}
    UNION
    -- SCR Portfolios (Financial Conglomerates) - Quantidade de Clientes
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_number_clients_operations') }}
    UNION
    -- Câmbio
    SELECT DISTINCT data_base
    FROM {{ source('silver', 'foreign_exchange_quarterly_foreign_currency_flow') }}
)

SELECT
    strftime(data, '%Y%m%d')::int as id_data,
    data,
    extract(year from data)::int as ano,
    extract(quarter from data)::int as trimestre,
    extract(month from data)::int as mes
FROM datas_unicas
