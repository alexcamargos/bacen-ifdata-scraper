{{ config(materialized='table') }}

WITH dados_brutos AS (
    -- Conglomerados Prudenciais
    SELECT
        codigo,
        data_base,
        'Conglomerado Prudencial' as tipo_instituicao,
        ativo_total,
        carteira_de_credito_classificada as carteira_credito,
        passivo_circulante_e_exigivel_a_longo_prazo as passivo_exigivel,
        captacoes,
        patrimonio_liquido,
        lucro_liquido,
        numero_de_agencias as quantidade_agencias,
        numero_de_postos_de_atendimento as quantidade_postos_atendimento,
        (lucro_liquido / NULLIF(patrimonio_liquido, 0)) as roe,
        (lucro_liquido / NULLIF(ativo_total, 0)) as roa
    FROM {{ source('silver', 'prudential_conglomerates_summary') }}

    UNION ALL

    -- Conglomerados Financeiros
    SELECT
        codigo,
        data_base,
        'Conglomerado Financeiro' as tipo_instituicao,
        ativo_total,
        carteira_de_credito_classificada as carteira_credito,
        passivo_circulante_e_exigivel_a_longo_prazo as passivo_exigivel,
        captacoes,
        patrimonio_liquido,
        lucro_liquido,
        numero_de_agencias as quantidade_agencias,
        numero_de_postos_de_atendimento as quantidade_postos_atendimento,
        (lucro_liquido / NULLIF(patrimonio_liquido, 0)) as roe,
        (lucro_liquido / NULLIF(ativo_total, 0)) as roa
    FROM {{ source('silver', 'financial_conglomerates_summary') }}

    UNION ALL

    -- Instituições Independentes
    SELECT
        codigo,
        data_base,
        'Instituicao Individual' as tipo_instituicao,
        ativo_total,
        carteira_de_credito_classificada as carteira_credito,
        passivo_circulante_e_exigivel_a_longo_prazo as passivo_exigivel,
        captacoes,
        patrimonio_liquido,
        lucro_liquido,
        numero_de_agencias as quantidade_agencias,
        numero_de_postos_de_atendimento as quantidade_postos_atendimento,
        (lucro_liquido / NULLIF(patrimonio_liquido, 0)) as roe,
        (lucro_liquido / NULLIF(ativo_total, 0)) as roa
    FROM {{ source('silver', 'individual_institutions_summary') }}
)

SELECT
    {{ generate_instituicao_id('d.codigo', 'd.tipo_instituicao') }} as id_instituicao, -- FK para dim_instituicao
    {{ format_date_id('d.data_base') }} as id_data,  -- FK para dim_tempo

    -- Métricas
    d.ativo_total,
    d.carteira_credito,
    d.passivo_exigivel,
    d.captacoes,
    d.patrimonio_liquido,
    d.lucro_liquido,
    d.quantidade_agencias,
    d.quantidade_postos_atendimento,
    d.roe,
    d.roa

FROM dados_brutos d
