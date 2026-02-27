{{ config(severity = 'error') }}

WITH silver_ativos AS (
    -- Conglomerados Prudenciais
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(disponibilidades, 0) as disponibilidades,
        COALESCE(aplicacoes_interfinanceiras_liquidez, 0) as aplicacoes_interfinanceiras_liquidez,
        COALESCE(tvm_e_instrumentos_financeiros_derivativos, 0) as tvm_derivativos,
        COALESCE(operacoes_de_credito, 0) as operacoes_de_credito,
        COALESCE(provisao_operacoes_de_credito, 0) as provisao_operacoes_de_credito,
        COALESCE(operacoes_de_credito_liquidas_provisao, 0) as operacoes_de_credito_liquidas_provisao,
        COALESCE(arrendamento_mercantil_a_receber, 0) as arrendamento_mercantil_a_receber,
        COALESCE(imobilizado_de_arrendamento, 0) as imobilizado_de_arrendamento,
        COALESCE(credores_antecipacao_valor_residual, 0) as credores_antecipacao_valor_residual,
        COALESCE(provisao_arrendamento_mercantil, 0) as provisao_arrendamento_mercantil,
        COALESCE(arrendamento_mercantil_liquido_de_provisao, 0) as arrendamento_mercantil_liquido_de_provisao,
        COALESCE(outros_creditos_liquido_de_provisao, 0) as outros_creditos_liquido_de_provisao,
        COALESCE(outros_ativos_realizaveis, 0) as outros_ativos_realizaveis,
        COALESCE(permanente_ajustado, 0) as permanente_ajustado,
        COALESCE(ativo_total_ajustado, 0) as ativo_total_ajustado,
        COALESCE(ativo_total, 0) as ativo_total
    FROM (SELECT * FROM {{ source('silver', 'prudential_conglomerates_assets') }} QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY ativo_total DESC NULLS LAST, codigo) = 1)
    
    UNION ALL
    
    -- Conglomerados Financeiros
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(disponibilidades, 0) as disponibilidades,
        COALESCE(aplicacoes_interfinanceiras_liquidez, 0) as aplicacoes_interfinanceiras_liquidez,
        COALESCE(tvm_e_instrumentos_financeiros_derivativos, 0) as tvm_derivativos,
        COALESCE(operacoes_de_credito, 0) as operacoes_de_credito,
        COALESCE(provisao_operacoes_de_credito, 0) as provisao_operacoes_de_credito,
        COALESCE(operacoes_de_credito_liquidas_provisao, 0) as operacoes_de_credito_liquidas_provisao,
        COALESCE(arrendamento_mercantil_a_receber, 0) as arrendamento_mercantil_a_receber,
        COALESCE(imobilizado_de_arrendamento, 0) as imobilizado_de_arrendamento,
        COALESCE(credores_antecipacao_valor_residual, 0) as credores_antecipacao_valor_residual,
        COALESCE(provisao_arrendamento_mercantil, 0) as provisao_arrendamento_mercantil,
        COALESCE(arrendamento_mercantil_liquido_de_provisao, 0) as arrendamento_mercantil_liquido_de_provisao,
        COALESCE(outros_creditos_liquido_de_provisao, 0) as outros_creditos_liquido_de_provisao,
        COALESCE(outros_ativos_realizaveis, 0) as outros_ativos_realizaveis,
        COALESCE(permanente_ajustado, 0) as permanente_ajustado,
        COALESCE(ativo_total_ajustado, 0) as ativo_total_ajustado,
        COALESCE(ativo_total, 0) as ativo_total
    FROM (SELECT * FROM {{ source('silver', 'financial_conglomerates_assets') }} QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY ativo_total DESC NULLS LAST, codigo) = 1)
    
    UNION ALL
    
    -- Instituicoes Independentes
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(disponibilidades, 0) as disponibilidades,
        COALESCE(aplicacoes_interfinanceiras_liquidez, 0) as aplicacoes_interfinanceiras_liquidez,
        COALESCE(tvm_e_instrumentos_financeiros_derivativos, 0) as tvm_derivativos,
        COALESCE(operacoes_de_credito, 0) as operacoes_de_credito,
        COALESCE(provisao_operacoes_de_credito, 0) as provisao_operacoes_de_credito,
        COALESCE(operacoes_de_credito_liquidas_provisao, 0) as operacoes_de_credito_liquidas_provisao,
        COALESCE(arrendamento_mercantil_a_receber, 0) as arrendamento_mercantil_a_receber,
        COALESCE(imobilizado_de_arrendamento, 0) as imobilizado_de_arrendamento,
        COALESCE(credores_antecipacao_valor_residual, 0) as credores_antecipacao_valor_residual,
        COALESCE(provisao_arrendamento_mercantil, 0) as provisao_arrendamento_mercantil,
        COALESCE(arrendamento_mercantil_liquido_de_provisao, 0) as arrendamento_mercantil_liquido_de_provisao,
        COALESCE(outros_creditos_liquido_de_provisao, 0) as outros_creditos_liquido_de_provisao,
        COALESCE(outros_ativos_realizaveis, 0) as outros_ativos_realizaveis,
        COALESCE(permanente_ajustado, 0) as permanente_ajustado,
        COALESCE(ativo_total_ajustado, 0) as ativo_total_ajustado,
        COALESCE(ativo_total, 0) as ativo_total
    FROM (SELECT * FROM {{ source('silver', 'individual_institutions_assets') }} QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY ativo_total DESC NULLS LAST, codigo) = 1)
),

silver_agg AS (
    SELECT
        id_data,
        SUM(disponibilidades) as t_disponibilidades,
        SUM(aplicacoes_interfinanceiras_liquidez) as t_aplicacoes_interfinanceiras_liquidez,
        SUM(tvm_derivativos) as t_tvm_derivativos,
        SUM(operacoes_de_credito) as t_operacoes_de_credito,
        SUM(provisao_operacoes_de_credito) as t_provisao_operacoes_de_credito,
        SUM(operacoes_de_credito_liquidas_provisao) as t_operacoes_de_credito_liquidas_provisao,
        SUM(arrendamento_mercantil_a_receber) as t_arrendamento_mercantil_a_receber,
        SUM(imobilizado_de_arrendamento) as t_imobilizado_de_arrendamento,
        SUM(credores_antecipacao_valor_residual) as t_credores_antecipacao_valor_residual,
        SUM(provisao_arrendamento_mercantil) as t_provisao_arrendamento_mercantil,
        SUM(arrendamento_mercantil_liquido_de_provisao) as t_arrendamento_mercantil_liquido_de_provisao,
        SUM(outros_creditos_liquido_de_provisao) as t_outros_creditos_liquido_de_provisao,
        SUM(outros_ativos_realizaveis) as t_outros_ativos_realizaveis,
        SUM(permanente_ajustado) as t_permanente_ajustado,
        SUM(ativo_total_ajustado) as t_ativo_total_ajustado,
        SUM(ativo_total) as t_ativo_total
    FROM silver_ativos
    GROUP BY id_data
),

gold_agg AS (
    SELECT
        id_data,
        SUM(COALESCE(disponibilidades, 0)) as t_disponibilidades,
        SUM(COALESCE(aplicacoes_interfinanceiras_liquidez, 0)) as t_aplicacoes_interfinanceiras_liquidez,
        SUM(COALESCE(tvm_derivativos, 0)) as t_tvm_derivativos,
        SUM(COALESCE(operacoes_de_credito, 0)) as t_operacoes_de_credito,
        SUM(COALESCE(provisao_operacoes_de_credito, 0)) as t_provisao_operacoes_de_credito,
        SUM(COALESCE(operacoes_de_credito_liquidas_provisao, 0)) as t_operacoes_de_credito_liquidas_provisao,
        SUM(COALESCE(arrendamento_mercantil_a_receber, 0)) as t_arrendamento_mercantil_a_receber,
        SUM(COALESCE(imobilizado_de_arrendamento, 0)) as t_imobilizado_de_arrendamento,
        SUM(COALESCE(credores_antecipacao_valor_residual, 0)) as t_credores_antecipacao_valor_residual,
        SUM(COALESCE(provisao_arrendamento_mercantil, 0)) as t_provisao_arrendamento_mercantil,
        SUM(COALESCE(arrendamento_mercantil_liquido_de_provisao, 0)) as t_arrendamento_mercantil_liquido_de_provisao,
        SUM(COALESCE(outros_creditos_liquido_de_provisao, 0)) as t_outros_creditos_liquido_de_provisao,
        SUM(COALESCE(outros_ativos_realizaveis, 0)) as t_outros_ativos_realizaveis,
        SUM(COALESCE(permanente_ajustado, 0)) as t_permanente_ajustado,
        SUM(COALESCE(ativo_total_ajustado, 0)) as t_ativo_total_ajustado,
        SUM(COALESCE(ativo_total, 0)) as t_ativo_total
    FROM {{ ref('fato_balanco_patrimonial') }}
    GROUP BY id_data
)

SELECT
    COALESCE(s.id_data, g.id_data) as id_data,
    ROUND(s.t_disponibilidades - g.t_disponibilidades, 2) as diff_disponibilidades,
    ROUND(s.t_aplicacoes_interfinanceiras_liquidez - g.t_aplicacoes_interfinanceiras_liquidez, 2) as diff_aplicacoes_interfinanceiras_liquidez,
    ROUND(s.t_tvm_derivativos - g.t_tvm_derivativos, 2) as diff_tvm_derivativos,
    ROUND(s.t_operacoes_de_credito - g.t_operacoes_de_credito, 2) as diff_operacoes_de_credito,
    ROUND(s.t_provisao_operacoes_de_credito - g.t_provisao_operacoes_de_credito, 2) as diff_provisao_operacoes_de_credito,
    ROUND(s.t_operacoes_de_credito_liquidas_provisao - g.t_operacoes_de_credito_liquidas_provisao, 2) as diff_operacoes_de_credito_liquidas_provisao,
    ROUND(s.t_arrendamento_mercantil_a_receber - g.t_arrendamento_mercantil_a_receber, 2) as diff_arrendamento_mercantil_a_receber,
    ROUND(s.t_imobilizado_de_arrendamento - g.t_imobilizado_de_arrendamento, 2) as diff_imobilizado_de_arrendamento,
    ROUND(s.t_credores_antecipacao_valor_residual - g.t_credores_antecipacao_valor_residual, 2) as diff_credores_antecipacao_valor_residual,
    ROUND(s.t_provisao_arrendamento_mercantil - g.t_provisao_arrendamento_mercantil, 2) as diff_provisao_arrendamento_mercantil,
    ROUND(s.t_arrendamento_mercantil_liquido_de_provisao - g.t_arrendamento_mercantil_liquido_de_provisao, 2) as diff_arrendamento_mercantil_liquido_de_provisao,
    ROUND(s.t_outros_creditos_liquido_de_provisao - g.t_outros_creditos_liquido_de_provisao, 2) as diff_outros_creditos_liquido_de_provisao,
    ROUND(s.t_outros_ativos_realizaveis - g.t_outros_ativos_realizaveis, 2) as diff_outros_ativos_realizaveis,
    ROUND(s.t_permanente_ajustado - g.t_permanente_ajustado, 2) as diff_permanente_ajustado,
    ROUND(s.t_ativo_total_ajustado - g.t_ativo_total_ajustado, 2) as diff_ativo_total_ajustado,
    ROUND(s.t_ativo_total - g.t_ativo_total, 2) as diff_ativo_total

FROM silver_agg s
FULL OUTER JOIN gold_agg g ON s.id_data = g.id_data
WHERE 
    ROUND(COALESCE(s.t_disponibilidades, 0) - COALESCE(g.t_disponibilidades, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_aplicacoes_interfinanceiras_liquidez, 0) - COALESCE(g.t_aplicacoes_interfinanceiras_liquidez, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_tvm_derivativos, 0) - COALESCE(g.t_tvm_derivativos, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_operacoes_de_credito, 0) - COALESCE(g.t_operacoes_de_credito, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_provisao_operacoes_de_credito, 0) - COALESCE(g.t_provisao_operacoes_de_credito, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_operacoes_de_credito_liquidas_provisao, 0) - COALESCE(g.t_operacoes_de_credito_liquidas_provisao, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_arrendamento_mercantil_a_receber, 0) - COALESCE(g.t_arrendamento_mercantil_a_receber, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_imobilizado_de_arrendamento, 0) - COALESCE(g.t_imobilizado_de_arrendamento, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_credores_antecipacao_valor_residual, 0) - COALESCE(g.t_credores_antecipacao_valor_residual, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_provisao_arrendamento_mercantil, 0) - COALESCE(g.t_provisao_arrendamento_mercantil, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_arrendamento_mercantil_liquido_de_provisao, 0) - COALESCE(g.t_arrendamento_mercantil_liquido_de_provisao, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_outros_creditos_liquido_de_provisao, 0) - COALESCE(g.t_outros_creditos_liquido_de_provisao, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_outros_ativos_realizaveis, 0) - COALESCE(g.t_outros_ativos_realizaveis, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_permanente_ajustado, 0) - COALESCE(g.t_permanente_ajustado, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_ativo_total_ajustado, 0) - COALESCE(g.t_ativo_total_ajustado, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_ativo_total, 0) - COALESCE(g.t_ativo_total, 0), 2) != 0
