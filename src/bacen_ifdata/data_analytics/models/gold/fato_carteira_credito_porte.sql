{{ config(materialized='table') }}

WITH unpivoted AS (
    SELECT 
        codigo, 
        data_base, 
        nome_coluna, 
        valor,
        'Conglomerado Financeiro' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_business_size') }}
    UNPIVOT (
        valor FOR nome_coluna IN (
            COLUMNS(* EXCLUDE (
                instituicao, codigo, consolidado_bancario, tipo_de_consolidacao, tipo_de_controle,
                segmento_resolucao, segmento, cidade, uf, regiao, data_base,
                total_carteira_pessoa_juridica, total_nao_individualizado_pessoa_juridica, total_exterior_pessoa_juridica
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
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_business_size') }}
    UNPIVOT (
        valor FOR nome_coluna IN (
            COLUMNS(* EXCLUDE (
                instituicao, codigo, consolidado_bancario, tipo_de_consolidacao, tipo_de_controle,
                segmento_resolucao, segmento, cidade, uf, regiao, data_base,
                total_da_carteira_de_pessoa_juridica, total_nao_individualizado_pessoa_juridica, total_exterior_pessoa_juridica
            ))
        )
    )
),
mapped AS (
    SELECT
        u.codigo,
        u.data_base,
        u.tipo_instituicao,
        p.id_porte,
        u.valor
    FROM unpivoted u
    JOIN {{ ref('dim_porte') }} p ON u.nome_coluna = p.coluna
)

SELECT
    {{ generate_instituicao_id('codigo', 'tipo_instituicao') }} as id_instituicao,
    strftime(try_cast(data_base as date), '%Y%m%d')::int as id_data,
    id_porte,
    valor
FROM mapped
WHERE valor IS NOT NULL
