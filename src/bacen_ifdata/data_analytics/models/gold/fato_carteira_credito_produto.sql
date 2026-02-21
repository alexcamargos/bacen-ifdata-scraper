{{ config(materialized='table') }}

WITH unpivoted_pf AS (
    SELECT 
        codigo, 
        data_base, 
        nome_coluna, 
        valor,
        'Conglomerado Financeiro' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_portfolio_individuals_type_maturity') }}
    UNPIVOT (
        valor FOR nome_coluna IN (
            COLUMNS(* EXCLUDE (
                instituicao, codigo, consolidado_bancario, tipo_de_consolidacao, tipo_de_controle,
                segmento_resolucao, segmento, cidade, uf, regiao, data_base,
                total_carteira_pessoa_fisica, total_exterior_pessoa_fisica
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
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_individuals_type_maturity') }}
    UNPIVOT (
        valor FOR nome_coluna IN (
            COLUMNS(* EXCLUDE (
                instituicao, codigo, consolidado_bancario, tipo_de_consolidacao, tipo_de_controle,
                segmento_resolucao, segmento, cidade, uf, regiao, data_base,
                total_da_carteira_de_pessoa_fisica, total_exterior_pessoa_fisica
            ))
        )
    )
),
pf_mapped AS (
    SELECT
        u.codigo,
        u.data_base,
        u.tipo_instituicao,
        p.id_produto,
        f.id_faixa,
        u.valor
    FROM unpivoted_pf u
    JOIN {{ ref('dim_produto_credito') }} p ON u.nome_coluna LIKE p.prefixo_coluna || '%'
    JOIN {{ ref('dim_faixa_vencimento') }} f ON u.nome_coluna LIKE '%' || f.sufixo_coluna
    WHERE p.tipo_pessoa IN ('PF', 'Ambos')
),
unpivoted_pj AS (
    SELECT 
        codigo, 
        data_base, 
        nome_coluna, 
        valor,
        'Conglomerado Financeiro' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_type_maturity') }}
    UNPIVOT (
        valor FOR nome_coluna IN (
            COLUMNS(* EXCLUDE (
                instituicao, codigo, consolidado_bancario, tipo_de_consolidacao, tipo_de_controle,
                segmento_resolucao, segmento, cidade, uf, regiao, data_base,
                total_carteira_pessoa_juridica, total_exterior_pessoa_juridica
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
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_type_maturity') }}
    UNPIVOT (
        valor FOR nome_coluna IN (
            COLUMNS(* EXCLUDE (
                instituicao, codigo, consolidado_bancario, tipo_de_consolidacao, tipo_de_controle,
                segmento_resolucao, segmento, cidade, uf, regiao, data_base,
                total_da_carteira_de_pessoa_juridica, total_exterior_pessoa_juridica
            ))
        )
    )
),
pj_mapped AS (
    SELECT
        u.codigo,
        u.data_base,
        u.tipo_instituicao,
        p.id_produto,
        f.id_faixa,
        u.valor
    FROM unpivoted_pj u
    JOIN {{ ref('dim_produto_credito') }} p ON u.nome_coluna LIKE p.prefixo_coluna || '%'
    JOIN {{ ref('dim_faixa_vencimento') }} f ON u.nome_coluna LIKE '%' || f.sufixo_coluna
    WHERE p.tipo_pessoa IN ('PJ', 'Ambos')
),
combined AS (
    SELECT * FROM pf_mapped
    UNION ALL
    SELECT * FROM pj_mapped
)

SELECT
    {{ generate_instituicao_id('codigo', 'tipo_instituicao') }} as id_instituicao,
    strftime(try_cast(data_base as date), '%Y%m%d')::int as id_data,
    id_produto,
    id_faixa as id_faixa_vencimento,
    valor
FROM combined
WHERE valor IS NOT NULL
