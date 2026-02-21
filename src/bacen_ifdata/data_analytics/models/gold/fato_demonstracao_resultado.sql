{{ config(materialized='table') }}

WITH summary_prudential AS (
    SELECT 
        codigo, 
        data_base, 
        ativo_total,
        patrimonio_liquido,
        lucro_liquido 
    FROM {{ source('silver', 'prudential_conglomerates_summary') }}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY ativo_total DESC) = 1
),

summary_financial AS (
    SELECT 
        codigo, 
        data_base, 
        ativo_total,
        patrimonio_liquido,
        lucro_liquido 
    FROM {{ source('silver', 'financial_conglomerates_summary') }}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY ativo_total DESC) = 1
),

summary_individual AS (
    SELECT 
        codigo, 
        data_base, 
        ativo_total,
        patrimonio_liquido,
        lucro_liquido 
    FROM {{ source('silver', 'individual_institutions_summary') }}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY ativo_total DESC) = 1
),

dre AS (
    -- Conglomerados Prudenciais
    SELECT
        dre.codigo,
        dre.data_base,
        'Conglomerado Prudencial' as tipo_instituicao,
        -- Receitas
        dre.receitas_intermediacao_financeira,
        dre.rendas_operacoes_de_credito,
        dre.rendas_operacoes_de_arrendamento_mercantil,
        dre.rendas_operacoes_tvm,
        dre.rendas_operacoes_instrumentos_financeiros_derivativos,
        dre.rendas_operacoes_cambio,
        dre.rendas_aplicacoes_compulsorias,
        -- Despesas
        dre.despesas_intermediacao_financeira,
        dre.despesas_captacao,
        dre.despesas_obrigacoes_emprestimos_repasses,
        dre.despesas_operacoes_arrendamento_mercantil,
        dre.despesas_operacoes_cambio,
        dre.resultado_provisao_creditos_dificil_liquidacao,
        -- Resultados Intermediacao
        dre.resultado_intermediacao_financeira,
        -- Outras Receitas/Despesas
        dre.rendas_prestacao_servicos,
        dre.rendas_tarifas_bancarias,
        dre.despesas_pessoal,
        dre.despesas_administrativas,
        dre.despesas_tributarias,
        dre.resultado_participacoes,
        dre.outras_receitas_operacionais,
        dre.outras_despesas_operacionais,
        dre.outras_receitas_despesas_operacionais,
        -- Resultado Operacional
        dre.resultado_operacional,
        -- Resultado Nao Operacional
        dre.resultado_nao_operacional,
        -- Apuracao Final
        dre.resultado_antes_tributacao_participacao as resultado_antes_tributacao,
        dre.imposto_renda_contribuicao_social,
        dre.participacao_lucros,
        dre.lucro_liquido,
        NULL as juros_sobre_capital_social_cooperativas,
        dre.juros_sobre_capital_proprio,
        (r.lucro_liquido / NULLIF(r.patrimonio_liquido, 0)) as roe,
        (r.lucro_liquido / NULLIF(r.ativo_total, 0)) as roa
    FROM {{ source('silver', 'prudential_conglomerates_income_statement') }} dre
    LEFT JOIN summary_prudential r
      ON dre.codigo = r.codigo AND dre.data_base = r.data_base

    UNION ALL

    -- Conglomerados Financeiros
    SELECT
        dre.codigo,
        dre.data_base,
        'Conglomerado Financeiro' as tipo_instituicao,
        -- Receitas
        dre.receitas_intermediacao_financeira,
        dre.rendas_operacoes_de_credito,
        dre.rendas_operacoes_de_arrendamento_mercantil,
        dre.rendas_operacoes_tvm,
        dre.rendas_operacoes_instrumentos_financeiros_derivativos,
        dre.resultado_operacoes_cambio as rendas_operacoes_cambio,
        dre.rendas_aplicacoes_compulsorias,
        -- Despesas
        dre.despesas_intermediacao_financeira,
        dre.despesas_captacao,
        dre.despesas_obrigacoes_emprestimos_repasses,
        dre.despesas_operacoes_arrendamento_mercantil,
        dre.despesas_operacoes_cambio,
        dre.resultado_provisao_creditos_dificil_liquidacao,
        -- Resultados Intermediacao
        dre.resultado_intermediacao_financeira,
        -- Outras Receitas/Despesas
        dre.rendas_prestacao_servicos,
        dre.rendas_tarifas_bancarias,
        dre.despesas_pessoal,
        dre.despesas_administrativas,
        dre.despesas_tributarias,
        dre.resultado_participacoes,
        dre.outras_receitas_operacionais,
        dre.outras_despesas_operacionais,
        dre.outras_receitas_despesas_operacionais,
        -- Resultado Operacional
        dre.resultado_operacional,
        -- Resultado Nao Operacional
        dre.resultado_nao_operacional,
        -- Apuracao Final
        dre.resultado_antes_tributacao_lucro_participacao as resultado_antes_tributacao,
        dre.imposto_renda_contribuicao_social,
        dre.participacao_lucros,
        dre.lucro_liquido,
        dre.juros_sobre_capital_social_cooperativas,
        NULL as juros_sobre_capital_proprio,
        (r.lucro_liquido / NULLIF(r.patrimonio_liquido, 0)) as roe,
        (r.lucro_liquido / NULLIF(r.ativo_total, 0)) as roa
    FROM {{ source('silver', 'financial_conglomerates_income_statement') }} dre
    LEFT JOIN summary_financial r
      ON dre.codigo = r.codigo AND dre.data_base = r.data_base

    UNION ALL

    -- Instituições Individuais
    SELECT
        dre.codigo,
        dre.data_base,
        'Instituicao Individual' as tipo_instituicao,
        -- Receitas
        dre.receitas_intermediacao_financeira,
        dre.rendas_operacoes_de_credito,
        dre.rendas_operacoes_de_arrendamento_mercantil,
        dre.rendas_operacoes_tvm,
        dre.rendas_operacoes_instrumentos_financeiros_derivativos,
        dre.resultado_operacoes_cambio as rendas_operacoes_cambio,
        dre.rendas_aplicacoes_compulsorias,
        -- Despesas
        dre.despesas_intermediacao_financeira,
        dre.despesas_captacao,
        dre.despesas_obrigacoes_emprestimos_repasses,
        dre.despesas_operacoes_arrendamento_mercantil,
        dre.despesas_operacoes_cambio,
        dre.resultado_provisao_creditos_dificil_liquidacao,
        -- Resultados Intermediacao
        dre.resultado_intermediacao_financeira,
        -- Outras Receitas/Despesas
        dre.rendas_prestacao_servicos,
        dre.rendas_tarifas_bancarias,
        dre.despesas_pessoal,
        dre.despesas_administrativas,
        dre.despesas_tributarias,
        dre.resultado_participacoes,
        dre.outras_receitas_operacionais,
        dre.outras_despesas_operacionais,
        dre.outras_receitas_despesas_operacionais,
        -- Resultado Operacional
        dre.resultado_operacional,
        -- Resultado Nao Operacional
        dre.resultado_nao_operacional,
        -- Apuracao Final
        dre.resultado_antes_tributacao_lucro_participacao as resultado_antes_tributacao,
        dre.imposto_renda_contribuicao_social,
        dre.participacao_lucros,
        dre.lucro_liquido,
        dre.juros_sobre_capital_social_cooperativas,
        NULL as juros_sobre_capital_proprio,
        (r.lucro_liquido / NULLIF(r.patrimonio_liquido, 0)) as roe,
        (r.lucro_liquido / NULLIF(r.ativo_total, 0)) as roa
    FROM {{ source('silver', 'individual_institutions_income_statement') }} dre
    LEFT JOIN summary_individual r
      ON dre.codigo = r.codigo AND dre.data_base = r.data_base
)

SELECT
    {{ generate_instituicao_id('codigo', 'tipo_instituicao') }} as id_instituicao,
    strftime(try_cast(data_base as date), '%Y%m%d')::int as id_data,
    -- Receitas
    receitas_intermediacao_financeira,
    rendas_operacoes_de_credito,
    rendas_operacoes_de_arrendamento_mercantil,
    rendas_operacoes_tvm,
    rendas_operacoes_instrumentos_financeiros_derivativos,
    rendas_operacoes_cambio,
    rendas_aplicacoes_compulsorias,
    -- Despesas
    despesas_intermediacao_financeira,
    despesas_captacao,
    despesas_obrigacoes_emprestimos_repasses,
    despesas_operacoes_arrendamento_mercantil,
    despesas_operacoes_cambio,
    resultado_provisao_creditos_dificil_liquidacao,
    -- Intermediacao
    resultado_intermediacao_financeira,
    -- Outras
    rendas_prestacao_servicos,
    rendas_tarifas_bancarias,
    despesas_pessoal,
    despesas_administrativas,
    despesas_tributarias,
    resultado_participacoes,
    outras_receitas_operacionais,
    outras_despesas_operacionais,
    outras_receitas_despesas_operacionais,
    -- Resultados
    resultado_operacional,
    resultado_nao_operacional,
    resultado_antes_tributacao,
    imposto_renda_contribuicao_social,
    participacao_lucros,
    lucro_liquido,
    juros_sobre_capital_social_cooperativas,
    juros_sobre_capital_proprio
FROM dre
