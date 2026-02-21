{{ config(materialized='table') }}

WITH location_sources AS (
    SELECT DISTINCT
        cidade,
        uf,
        regiao
    FROM {{ source('silver', 'prudential_conglomerates_summary') }}
    WHERE cidade IS NOT NULL
    
    UNION
    
    SELECT DISTINCT
        cidade,
        uf,
        regiao
    FROM {{ source('silver', 'financial_conglomerates_summary') }}
    WHERE cidade IS NOT NULL
    
    UNION
    
    SELECT DISTINCT
        cidade,
        uf,
        regiao
    FROM {{ source('silver', 'individual_institutions_summary') }}
    WHERE cidade IS NOT NULL

    UNION

    SELECT DISTINCT
        cidade,
        uf,
        regiao
    FROM {{ source('silver', 'foreign_exchange_quarterly_foreign_currency_flow') }}
    WHERE cidade IS NOT NULL

    UNION

    -- Fallback: localizações de instituições presentes apenas nas tabelas SCR
    SELECT DISTINCT
        cidade,
        uf,
        regiao
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_indexer') }}
    WHERE cidade IS NOT NULL
)

SELECT
    -- Create a surrogate key based on the unique combination of location fields
    md5(cast(coalesce(cidade, '') || coalesce(uf, '') || coalesce(regiao, '') as varchar)) as id_localizacao,
    cidade,
    uf,
    regiao
FROM location_sources

UNION

-- Sentinel para instituições sem dados de localização (cidade, uf, regiao = NULL)
SELECT
    md5(cast('' as varchar)) as id_localizacao,
    NULL as cidade,
    NULL as uf,
    NULL as regiao

