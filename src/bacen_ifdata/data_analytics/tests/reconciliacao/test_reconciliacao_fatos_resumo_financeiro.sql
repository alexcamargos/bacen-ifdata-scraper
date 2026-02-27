{{ config(severity = 'error') }}

WITH silver_data AS (
    -- Conglomerados Prudenciais
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(ativo_total, 0) as ativo_total,
        COALESCE(carteira_de_credito_classificada, 0) as carteira_credito,
        COALESCE(passivo_circulante_e_exigivel_a_longo_prazo, 0) as passivo_exigivel,
        COALESCE(captacoes, 0) as captacoes,
        COALESCE(patrimonio_liquido, 0) as patrimonio_liquido,
        COALESCE(lucro_liquido, 0) as lucro_liquido,
        COALESCE(numero_de_agencias, 0) as quantidade_agencias,
        COALESCE(numero_de_postos_de_atendimento, 0) as quantidade_postos_atendimento
    FROM {{ source('silver', 'prudential_conglomerates_summary') }}
    
    UNION ALL
    
    -- Conglomerados Financeiros
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(ativo_total, 0) as ativo_total,
        COALESCE(carteira_de_credito_classificada, 0) as carteira_credito,
        COALESCE(passivo_circulante_e_exigivel_a_longo_prazo, 0) as passivo_exigivel,
        COALESCE(captacoes, 0) as captacoes,
        COALESCE(patrimonio_liquido, 0) as patrimonio_liquido,
        COALESCE(lucro_liquido, 0) as lucro_liquido,
        COALESCE(numero_de_agencias, 0) as quantidade_agencias,
        COALESCE(numero_de_postos_de_atendimento, 0) as quantidade_postos_atendimento
    FROM {{ source('silver', 'financial_conglomerates_summary') }}
    
    UNION ALL
    
    -- Instituicoes Independentes
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(ativo_total, 0) as ativo_total,
        COALESCE(carteira_de_credito_classificada, 0) as carteira_credito,
        COALESCE(passivo_circulante_e_exigivel_a_longo_prazo, 0) as passivo_exigivel,
        COALESCE(captacoes, 0) as captacoes,
        COALESCE(patrimonio_liquido, 0) as patrimonio_liquido,
        COALESCE(lucro_liquido, 0) as lucro_liquido,
        COALESCE(numero_de_agencias, 0) as quantidade_agencias,
        COALESCE(numero_de_postos_de_atendimento, 0) as quantidade_postos_atendimento
    FROM {{ source('silver', 'individual_institutions_summary') }}
),

silver_agg AS (
    SELECT
        id_data,
        SUM(ativo_total) as total_ativo,
        SUM(carteira_credito) as total_carteira_credito,
        SUM(passivo_exigivel) as total_passivo_exigivel,
        SUM(captacoes) as total_captacoes,
        SUM(patrimonio_liquido) as total_patrimonio_liquido,
        SUM(lucro_liquido) as total_lucro_liquido,
        SUM(quantidade_agencias) as total_agencias,
        SUM(quantidade_postos_atendimento) as total_postos
    FROM silver_data
    GROUP BY id_data
),

gold_agg AS (
    SELECT
        id_data,
        SUM(COALESCE(ativo_total, 0)) as total_ativo,
        SUM(COALESCE(carteira_credito, 0)) as total_carteira_credito,
        SUM(COALESCE(passivo_exigivel, 0)) as total_passivo_exigivel,
        SUM(COALESCE(captacoes, 0)) as total_captacoes,
        SUM(COALESCE(patrimonio_liquido, 0)) as total_patrimonio_liquido,
        SUM(COALESCE(lucro_liquido, 0)) as total_lucro_liquido,
        SUM(COALESCE(quantidade_agencias, 0)) as total_agencias,
        SUM(COALESCE(quantidade_postos_atendimento, 0)) as total_postos
    FROM {{ ref('fato_resumo_financeiro') }}
    GROUP BY id_data
)

SELECT
    COALESCE(s.id_data, g.id_data) as id_data,
    s.total_ativo as silver_ativo,
    g.total_ativo as gold_ativo,
    ROUND(COALESCE(s.total_ativo, 0) - COALESCE(g.total_ativo, 0), 2) as diff_ativo,
    
    s.total_carteira_credito as silver_carteira,
    g.total_carteira_credito as gold_carteira,
    ROUND(COALESCE(s.total_carteira_credito, 0) - COALESCE(g.total_carteira_credito, 0), 2) as diff_carteira,
    
    s.total_passivo_exigivel as silver_passivo,
    g.total_passivo_exigivel as gold_passivo,
    ROUND(COALESCE(s.total_passivo_exigivel, 0) - COALESCE(g.total_passivo_exigivel, 0), 2) as diff_passivo,
    
    s.total_captacoes as silver_captacoes,
    g.total_captacoes as gold_captacoes,
    ROUND(COALESCE(s.total_captacoes, 0) - COALESCE(g.total_captacoes, 0), 2) as diff_captacoes,
    
    s.total_patrimonio_liquido as silver_patrimonio,
    g.total_patrimonio_liquido as gold_patrimonio,
    ROUND(COALESCE(s.total_patrimonio_liquido, 0) - COALESCE(g.total_patrimonio_liquido, 0), 2) as diff_patrimonio,
    
    s.total_lucro_liquido as silver_lucro,
    g.total_lucro_liquido as gold_lucro,
    ROUND(COALESCE(s.total_lucro_liquido, 0) - COALESCE(g.total_lucro_liquido, 0), 2) as diff_lucro,
    
    s.total_agencias as silver_agencias,
    g.total_agencias as gold_agencias,
    ROUND(COALESCE(s.total_agencias, 0) - COALESCE(g.total_agencias, 0), 2) as diff_agencias,
    
    s.total_postos as silver_postos,
    g.total_postos as gold_postos,
    ROUND(COALESCE(s.total_postos, 0) - COALESCE(g.total_postos, 0), 2) as diff_postos

FROM silver_agg s
FULL OUTER JOIN gold_agg g ON s.id_data = g.id_data
WHERE 
    ROUND(COALESCE(s.total_ativo, 0) - COALESCE(g.total_ativo, 0), 2) != 0 OR
    ROUND(COALESCE(s.total_carteira_credito, 0) - COALESCE(g.total_carteira_credito, 0), 2) != 0 OR
    ROUND(COALESCE(s.total_passivo_exigivel, 0) - COALESCE(g.total_passivo_exigivel, 0), 2) != 0 OR
    ROUND(COALESCE(s.total_captacoes, 0) - COALESCE(g.total_captacoes, 0), 2) != 0 OR
    ROUND(COALESCE(s.total_patrimonio_liquido, 0) - COALESCE(g.total_patrimonio_liquido, 0), 2) != 0 OR
    ROUND(COALESCE(s.total_lucro_liquido, 0) - COALESCE(g.total_lucro_liquido, 0), 2) != 0 OR
    ROUND(COALESCE(s.total_agencias, 0) - COALESCE(g.total_agencias, 0), 2) != 0 OR
    ROUND(COALESCE(s.total_postos, 0) - COALESCE(g.total_postos, 0), 2) != 0
