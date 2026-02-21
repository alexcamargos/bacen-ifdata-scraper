{{ config(materialized='table') }}

WITH unpivoted AS (
    SELECT 
        codigo, 
        data_base, 
        nome_coluna, 
        valor,
        'Conglomerado Financeiro' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_portfolio_geographic_region') }}
    UNPIVOT (
        valor FOR nome_coluna IN (
            COLUMNS(* EXCLUDE (
                instituicao, codigo, consolidado_bancario, tipo_de_consolidacao, tipo_de_controle,
                segmento_resolucao, segmento, cidade, uf, regiao, data_base, total_geral
            ))
        )
    )

    UNION ALL

    SELECT 
        codigo, 
        data_base, 
        nome_coluna, 
        valor,
        'Conglomerado Financeiro (SCR)' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_geographic_region') }}
    UNPIVOT (
        valor FOR nome_coluna IN (
            COLUMNS(* EXCLUDE (
                instituicao, codigo, consolidado_bancario, tipo_de_consolidacao, tipo_de_controle,
                segmento_resolucao, segmento, cidade, uf, regiao, data_base, total_geral
            ))
        )
    )
),
mapped AS (
    SELECT
        u.codigo,
        u.data_base,
        u.tipo_instituicao,
        r.id_regiao,
        u.valor
    FROM unpivoted u
    JOIN {{ ref('dim_regiao') }} r ON u.nome_coluna = r.coluna
)

SELECT
    {{ generate_instituicao_id('codigo', 'tipo_instituicao') }} as id_instituicao,
    strftime(data_base, '%Y%m%d')::int as id_data,
    id_regiao,
    valor
FROM mapped
WHERE valor IS NOT NULL
