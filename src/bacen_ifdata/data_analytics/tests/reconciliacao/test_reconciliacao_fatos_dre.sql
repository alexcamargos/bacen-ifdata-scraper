{{ config(severity = 'error') }}

WITH silver_dre AS (
    -- Conglomerados Prudenciais
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(receitas_intermediacao_financeira, 0) as receitas_intermediacao_financeira,
        COALESCE(rendas_operacoes_de_credito, 0) as rendas_operacoes_de_credito,
        COALESCE(rendas_operacoes_de_arrendamento_mercantil, 0) as rendas_operacoes_de_arrendamento_mercantil,
        COALESCE(rendas_operacoes_tvm, 0) as rendas_operacoes_tvm,
        COALESCE(rendas_operacoes_instrumentos_financeiros_derivativos, 0) as rendas_operacoes_instrumentos_financeiros_derivativos,
        COALESCE(rendas_operacoes_cambio, 0) as resultado_operacoes_cambio,
        COALESCE(rendas_aplicacoes_compulsorias, 0) as rendas_aplicacoes_compulsorias,
        COALESCE(despesas_intermediacao_financeira, 0) as despesas_intermediacao_financeira,
        COALESCE(despesas_captacao, 0) as despesas_captacao,
        COALESCE(despesas_obrigacoes_emprestimos_repasses, 0) as despesas_obrigacoes_emprestimos_repasses,
        COALESCE(despesas_operacoes_arrendamento_mercantil, 0) as despesas_operacoes_arrendamento_mercantil,
        COALESCE(despesas_operacoes_cambio, 0) as despesas_operacoes_cambio,
        COALESCE(resultado_provisao_creditos_dificil_liquidacao, 0) as resultado_provisao_creditos_dificil_liquidacao,
        COALESCE(resultado_intermediacao_financeira, 0) as resultado_intermediacao_financeira,
        COALESCE(rendas_prestacao_servicos, 0) as rendas_prestacao_servicos,
        COALESCE(rendas_tarifas_bancarias, 0) as rendas_tarifas_bancarias,
        COALESCE(despesas_pessoal, 0) as despesas_pessoal,
        COALESCE(despesas_administrativas, 0) as despesas_administrativas,
        COALESCE(despesas_tributarias, 0) as despesas_tributarias,
        COALESCE(resultado_participacoes, 0) as resultado_participacoes,
        COALESCE(outras_receitas_operacionais, 0) as outras_receitas_operacionais,
        COALESCE(outras_despesas_operacionais, 0) as outras_despesas_operacionais,
        COALESCE(outras_receitas_despesas_operacionais, 0) as outras_receitas_despesas_operacionais,
        COALESCE(resultado_operacional, 0) as resultado_operacional,
        COALESCE(resultado_nao_operacional, 0) as resultado_nao_operacional,
        COALESCE(resultado_antes_tributacao_participacao, 0) as resultado_antes_tributacao,
        COALESCE(imposto_renda_contribuicao_social, 0) as imposto_renda_contribuicao_social,
        COALESCE(participacao_lucros, 0) as participacao_lucros,
        COALESCE(lucro_liquido, 0) as lucro_liquido,
        COALESCE(juros_sobre_capital_proprio, 0) as juros_sobre_capital
    FROM {{ source('silver', 'prudential_conglomerates_income_statement') }}
    
    UNION ALL
    
    -- Conglomerados Financeiros
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(receitas_intermediacao_financeira, 0) as receitas_intermediacao_financeira,
        COALESCE(rendas_operacoes_de_credito, 0) as rendas_operacoes_de_credito,
        COALESCE(rendas_operacoes_de_arrendamento_mercantil, 0) as rendas_operacoes_de_arrendamento_mercantil,
        COALESCE(rendas_operacoes_tvm, 0) as rendas_operacoes_tvm,
        COALESCE(rendas_operacoes_instrumentos_financeiros_derivativos, 0) as rendas_operacoes_instrumentos_financeiros_derivativos,
        COALESCE(resultado_operacoes_cambio, 0) as resultado_operacoes_cambio,
        COALESCE(rendas_aplicacoes_compulsorias, 0) as rendas_aplicacoes_compulsorias,
        COALESCE(despesas_intermediacao_financeira, 0) as despesas_intermediacao_financeira,
        COALESCE(despesas_captacao, 0) as despesas_captacao,
        COALESCE(despesas_obrigacoes_emprestimos_repasses, 0) as despesas_obrigacoes_emprestimos_repasses,
        COALESCE(despesas_operacoes_arrendamento_mercantil, 0) as despesas_operacoes_arrendamento_mercantil,
        COALESCE(despesas_operacoes_cambio, 0) as despesas_operacoes_cambio,
        COALESCE(resultado_provisao_creditos_dificil_liquidacao, 0) as resultado_provisao_creditos_dificil_liquidacao,
        COALESCE(resultado_intermediacao_financeira, 0) as resultado_intermediacao_financeira,
        COALESCE(rendas_prestacao_servicos, 0) as rendas_prestacao_servicos,
        COALESCE(rendas_tarifas_bancarias, 0) as rendas_tarifas_bancarias,
        COALESCE(despesas_pessoal, 0) as despesas_pessoal,
        COALESCE(despesas_administrativas, 0) as despesas_administrativas,
        COALESCE(despesas_tributarias, 0) as despesas_tributarias,
        COALESCE(resultado_participacoes, 0) as resultado_participacoes,
        COALESCE(outras_receitas_operacionais, 0) as outras_receitas_operacionais,
        COALESCE(outras_despesas_operacionais, 0) as outras_despesas_operacionais,
        COALESCE(outras_receitas_despesas_operacionais, 0) as outras_receitas_despesas_operacionais,
        COALESCE(resultado_operacional, 0) as resultado_operacional,
        COALESCE(resultado_nao_operacional, 0) as resultado_nao_operacional,
        COALESCE(resultado_antes_tributacao_lucro_participacao, 0) as resultado_antes_tributacao,
        COALESCE(imposto_renda_contribuicao_social, 0) as imposto_renda_contribuicao_social,
        COALESCE(participacao_lucros, 0) as participacao_lucros,
        COALESCE(lucro_liquido, 0) as lucro_liquido,
        COALESCE(juros_sobre_capital_social_cooperativas, 0) as juros_sobre_capital
    FROM {{ source('silver', 'financial_conglomerates_income_statement') }}
    
    UNION ALL
    
    -- Instituicoes Independentes
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(receitas_intermediacao_financeira, 0) as receitas_intermediacao_financeira,
        COALESCE(rendas_operacoes_de_credito, 0) as rendas_operacoes_de_credito,
        COALESCE(rendas_operacoes_de_arrendamento_mercantil, 0) as rendas_operacoes_de_arrendamento_mercantil,
        COALESCE(rendas_operacoes_tvm, 0) as rendas_operacoes_tvm,
        COALESCE(rendas_operacoes_instrumentos_financeiros_derivativos, 0) as rendas_operacoes_instrumentos_financeiros_derivativos,
        COALESCE(resultado_operacoes_cambio, 0) as resultado_operacoes_cambio,
        COALESCE(rendas_aplicacoes_compulsorias, 0) as rendas_aplicacoes_compulsorias,
        COALESCE(despesas_intermediacao_financeira, 0) as despesas_intermediacao_financeira,
        COALESCE(despesas_captacao, 0) as despesas_captacao,
        COALESCE(despesas_obrigacoes_emprestimos_repasses, 0) as despesas_obrigacoes_emprestimos_repasses,
        COALESCE(despesas_operacoes_arrendamento_mercantil, 0) as despesas_operacoes_arrendamento_mercantil,
        COALESCE(despesas_operacoes_cambio, 0) as despesas_operacoes_cambio,
        COALESCE(resultado_provisao_creditos_dificil_liquidacao, 0) as resultado_provisao_creditos_dificil_liquidacao,
        COALESCE(resultado_intermediacao_financeira, 0) as resultado_intermediacao_financeira,
        COALESCE(rendas_prestacao_servicos, 0) as rendas_prestacao_servicos,
        COALESCE(rendas_tarifas_bancarias, 0) as rendas_tarifas_bancarias,
        COALESCE(despesas_pessoal, 0) as despesas_pessoal,
        COALESCE(despesas_administrativas, 0) as despesas_administrativas,
        COALESCE(despesas_tributarias, 0) as despesas_tributarias,
        COALESCE(resultado_participacoes, 0) as resultado_participacoes,
        COALESCE(outras_receitas_operacionais, 0) as outras_receitas_operacionais,
        COALESCE(outras_despesas_operacionais, 0) as outras_despesas_operacionais,
        COALESCE(outras_receitas_despesas_operacionais, 0) as outras_receitas_despesas_operacionais,
        COALESCE(resultado_operacional, 0) as resultado_operacional,
        COALESCE(resultado_nao_operacional, 0) as resultado_nao_operacional,
        COALESCE(resultado_antes_tributacao_lucro_participacao, 0) as resultado_antes_tributacao,
        COALESCE(imposto_renda_contribuicao_social, 0) as imposto_renda_contribuicao_social,
        COALESCE(participacao_lucros, 0) as participacao_lucros,
        COALESCE(lucro_liquido, 0) as lucro_liquido,
        COALESCE(juros_sobre_capital_social_cooperativas, 0) as juros_sobre_capital
    FROM {{ source('silver', 'individual_institutions_income_statement') }}
),

silver_agg AS (
    SELECT
        id_data,
        SUM(receitas_intermediacao_financeira) as t_receitas_intermediacao_financeira,
        SUM(rendas_operacoes_de_credito) as t_rendas_operacoes_de_credito,
        SUM(rendas_operacoes_de_arrendamento_mercantil) as t_rendas_operacoes_de_arrendamento_mercantil,
        SUM(rendas_operacoes_tvm) as t_rendas_operacoes_tvm,
        SUM(rendas_operacoes_instrumentos_financeiros_derivativos) as t_rendas_operacoes_instrumentos_financeiros_derivativos,
        SUM(resultado_operacoes_cambio) as t_resultado_operacoes_cambio,
        SUM(rendas_aplicacoes_compulsorias) as t_rendas_aplicacoes_compulsorias,
        SUM(despesas_intermediacao_financeira) as t_despesas_intermediacao_financeira,
        SUM(despesas_captacao) as t_despesas_captacao,
        SUM(despesas_obrigacoes_emprestimos_repasses) as t_despesas_obrigacoes_emprestimos_repasses,
        SUM(despesas_operacoes_arrendamento_mercantil) as t_despesas_operacoes_arrendamento_mercantil,
        SUM(despesas_operacoes_cambio) as t_despesas_operacoes_cambio,
        SUM(resultado_provisao_creditos_dificil_liquidacao) as t_resultado_provisao_creditos_dificil_liquidacao,
        SUM(resultado_intermediacao_financeira) as t_resultado_intermediacao_financeira,
        SUM(rendas_prestacao_servicos) as t_rendas_prestacao_servicos,
        SUM(rendas_tarifas_bancarias) as t_rendas_tarifas_bancarias,
        SUM(despesas_pessoal) as t_despesas_pessoal,
        SUM(despesas_administrativas) as t_despesas_administrativas,
        SUM(despesas_tributarias) as t_despesas_tributarias,
        SUM(resultado_participacoes) as t_resultado_participacoes,
        SUM(outras_receitas_operacionais) as t_outras_receitas_operacionais,
        SUM(outras_despesas_operacionais) as t_outras_despesas_operacionais,
        SUM(outras_receitas_despesas_operacionais) as t_outras_receitas_despesas_operacionais,
        SUM(resultado_operacional) as t_resultado_operacional,
        SUM(resultado_nao_operacional) as t_resultado_nao_operacional,
        SUM(resultado_antes_tributacao) as t_resultado_antes_tributacao,
        SUM(imposto_renda_contribuicao_social) as t_imposto_renda_contribuicao_social,
        SUM(participacao_lucros) as t_participacao_lucros,
        SUM(lucro_liquido) as t_lucro_liquido,
        SUM(juros_sobre_capital) as t_juros_sobre_capital
    FROM silver_dre
    GROUP BY id_data
),

gold_agg AS (
    SELECT
        id_data,
        SUM(COALESCE(receitas_intermediacao_financeira, 0)) as t_receitas_intermediacao_financeira,
        SUM(COALESCE(rendas_operacoes_de_credito, 0)) as t_rendas_operacoes_de_credito,
        SUM(COALESCE(rendas_operacoes_de_arrendamento_mercantil, 0)) as t_rendas_operacoes_de_arrendamento_mercantil,
        SUM(COALESCE(rendas_operacoes_tvm, 0)) as t_rendas_operacoes_tvm,
        SUM(COALESCE(rendas_operacoes_instrumentos_financeiros_derivativos, 0)) as t_rendas_operacoes_instrumentos_financeiros_derivativos,
        SUM(COALESCE(resultado_operacoes_cambio, 0)) as t_resultado_operacoes_cambio,
        SUM(COALESCE(rendas_aplicacoes_compulsorias, 0)) as t_rendas_aplicacoes_compulsorias,
        SUM(COALESCE(despesas_intermediacao_financeira, 0)) as t_despesas_intermediacao_financeira,
        SUM(COALESCE(despesas_captacao, 0)) as t_despesas_captacao,
        SUM(COALESCE(despesas_obrigacoes_emprestimos_repasses, 0)) as t_despesas_obrigacoes_emprestimos_repasses,
        SUM(COALESCE(despesas_operacoes_arrendamento_mercantil, 0)) as t_despesas_operacoes_arrendamento_mercantil,
        SUM(COALESCE(despesas_operacoes_cambio, 0)) as t_despesas_operacoes_cambio,
        SUM(COALESCE(resultado_provisao_creditos_dificil_liquidacao, 0)) as t_resultado_provisao_creditos_dificil_liquidacao,
        SUM(COALESCE(resultado_intermediacao_financeira, 0)) as t_resultado_intermediacao_financeira,
        SUM(COALESCE(rendas_prestacao_servicos, 0)) as t_rendas_prestacao_servicos,
        SUM(COALESCE(rendas_tarifas_bancarias, 0)) as t_rendas_tarifas_bancarias,
        SUM(COALESCE(despesas_pessoal, 0)) as t_despesas_pessoal,
        SUM(COALESCE(despesas_administrativas, 0)) as t_despesas_administrativas,
        SUM(COALESCE(despesas_tributarias, 0)) as t_despesas_tributarias,
        SUM(COALESCE(resultado_participacoes, 0)) as t_resultado_participacoes,
        SUM(COALESCE(outras_receitas_operacionais, 0)) as t_outras_receitas_operacionais,
        SUM(COALESCE(outras_despesas_operacionais, 0)) as t_outras_despesas_operacionais,
        SUM(COALESCE(outras_receitas_despesas_operacionais, 0)) as t_outras_receitas_despesas_operacionais,
        SUM(COALESCE(resultado_operacional, 0)) as t_resultado_operacional,
        SUM(COALESCE(resultado_nao_operacional, 0)) as t_resultado_nao_operacional,
        SUM(COALESCE(resultado_antes_tributacao, 0)) as t_resultado_antes_tributacao,
        SUM(COALESCE(imposto_renda_contribuicao_social, 0)) as t_imposto_renda_contribuicao_social,
        SUM(COALESCE(participacao_lucros, 0)) as t_participacao_lucros,
        SUM(COALESCE(lucro_liquido, 0)) as t_lucro_liquido,
        SUM(COALESCE(juros_sobre_capital, 0)) as t_juros_sobre_capital
    FROM {{ ref('fato_demonstracao_resultado') }}
    GROUP BY id_data
)

SELECT
    COALESCE(s.id_data, g.id_data) as id_data,
    ROUND(s.t_receitas_intermediacao_financeira - g.t_receitas_intermediacao_financeira, 2) as diff_receitas_intermediacao_financeira,
    ROUND(s.t_rendas_operacoes_de_credito - g.t_rendas_operacoes_de_credito, 2) as diff_rendas_operacoes_de_credito,
    ROUND(s.t_rendas_operacoes_de_arrendamento_mercantil - g.t_rendas_operacoes_de_arrendamento_mercantil, 2) as diff_rendas_operacoes_de_arrendamento_mercantil,
    ROUND(s.t_rendas_operacoes_tvm - g.t_rendas_operacoes_tvm, 2) as diff_rendas_operacoes_tvm,
    ROUND(s.t_rendas_operacoes_instrumentos_financeiros_derivativos - g.t_rendas_operacoes_instrumentos_financeiros_derivativos, 2) as diff_rendas_operacoes_instrumentos_financeiros_derivativos,
    ROUND(s.t_resultado_operacoes_cambio - g.t_resultado_operacoes_cambio, 2) as diff_resultado_operacoes_cambio,
    ROUND(s.t_rendas_aplicacoes_compulsorias - g.t_rendas_aplicacoes_compulsorias, 2) as diff_rendas_aplicacoes_compulsorias,
    ROUND(s.t_despesas_intermediacao_financeira - g.t_despesas_intermediacao_financeira, 2) as diff_despesas_intermediacao_financeira,
    ROUND(s.t_despesas_captacao - g.t_despesas_captacao, 2) as diff_despesas_captacao,
    ROUND(s.t_despesas_obrigacoes_emprestimos_repasses - g.t_despesas_obrigacoes_emprestimos_repasses, 2) as diff_despesas_obrigacoes_emprestimos_repasses,
    ROUND(s.t_despesas_operacoes_arrendamento_mercantil - g.t_despesas_operacoes_arrendamento_mercantil, 2) as diff_despesas_operacoes_arrendamento_mercantil,
    ROUND(s.t_despesas_operacoes_cambio - g.t_despesas_operacoes_cambio, 2) as diff_despesas_operacoes_cambio,
    ROUND(s.t_resultado_provisao_creditos_dificil_liquidacao - g.t_resultado_provisao_creditos_dificil_liquidacao, 2) as diff_resultado_provisao_creditos_dificil_liquidacao,
    ROUND(s.t_resultado_intermediacao_financeira - g.t_resultado_intermediacao_financeira, 2) as diff_resultado_intermediacao_financeira,
    ROUND(s.t_rendas_prestacao_servicos - g.t_rendas_prestacao_servicos, 2) as diff_rendas_prestacao_servicos,
    ROUND(s.t_rendas_tarifas_bancarias - g.t_rendas_tarifas_bancarias, 2) as diff_rendas_tarifas_bancarias,
    ROUND(s.t_despesas_pessoal - g.t_despesas_pessoal, 2) as diff_despesas_pessoal,
    ROUND(s.t_despesas_administrativas - g.t_despesas_administrativas, 2) as diff_despesas_administrativas,
    ROUND(s.t_despesas_tributarias - g.t_despesas_tributarias, 2) as diff_despesas_tributarias,
    ROUND(s.t_resultado_participacoes - g.t_resultado_participacoes, 2) as diff_resultado_participacoes,
    ROUND(s.t_outras_receitas_operacionais - g.t_outras_receitas_operacionais, 2) as diff_outras_receitas_operacionais,
    ROUND(s.t_outras_despesas_operacionais - g.t_outras_despesas_operacionais, 2) as diff_outras_despesas_operacionais,
    ROUND(s.t_outras_receitas_despesas_operacionais - g.t_outras_receitas_despesas_operacionais, 2) as diff_outras_receitas_despesas_operacionais,
    ROUND(s.t_resultado_operacional - g.t_resultado_operacional, 2) as diff_resultado_operacional,
    ROUND(s.t_resultado_nao_operacional - g.t_resultado_nao_operacional, 2) as diff_resultado_nao_operacional,
    ROUND(s.t_resultado_antes_tributacao - g.t_resultado_antes_tributacao, 2) as diff_resultado_antes_tributacao,
    ROUND(s.t_imposto_renda_contribuicao_social - g.t_imposto_renda_contribuicao_social, 2) as diff_imposto_renda_contribuicao_social,
    ROUND(s.t_participacao_lucros - g.t_participacao_lucros, 2) as diff_participacao_lucros,
    ROUND(s.t_lucro_liquido - g.t_lucro_liquido, 2) as diff_lucro_liquido,
    ROUND(s.t_juros_sobre_capital - g.t_juros_sobre_capital, 2) as diff_juros_sobre_capital

FROM silver_agg s
FULL OUTER JOIN gold_agg g ON s.id_data = g.id_data
WHERE 
    ROUND(COALESCE(s.t_receitas_intermediacao_financeira, 0) - COALESCE(g.t_receitas_intermediacao_financeira, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_rendas_operacoes_de_credito, 0) - COALESCE(g.t_rendas_operacoes_de_credito, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_rendas_operacoes_de_arrendamento_mercantil, 0) - COALESCE(g.t_rendas_operacoes_de_arrendamento_mercantil, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_rendas_operacoes_tvm, 0) - COALESCE(g.t_rendas_operacoes_tvm, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_rendas_operacoes_instrumentos_financeiros_derivativos, 0) - COALESCE(g.t_rendas_operacoes_instrumentos_financeiros_derivativos, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_resultado_operacoes_cambio, 0) - COALESCE(g.t_resultado_operacoes_cambio, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_rendas_aplicacoes_compulsorias, 0) - COALESCE(g.t_rendas_aplicacoes_compulsorias, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_despesas_intermediacao_financeira, 0) - COALESCE(g.t_despesas_intermediacao_financeira, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_despesas_captacao, 0) - COALESCE(g.t_despesas_captacao, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_despesas_obrigacoes_emprestimos_repasses, 0) - COALESCE(g.t_despesas_obrigacoes_emprestimos_repasses, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_despesas_operacoes_arrendamento_mercantil, 0) - COALESCE(g.t_despesas_operacoes_arrendamento_mercantil, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_despesas_operacoes_cambio, 0) - COALESCE(g.t_despesas_operacoes_cambio, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_resultado_provisao_creditos_dificil_liquidacao, 0) - COALESCE(g.t_resultado_provisao_creditos_dificil_liquidacao, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_resultado_intermediacao_financeira, 0) - COALESCE(g.t_resultado_intermediacao_financeira, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_rendas_prestacao_servicos, 0) - COALESCE(g.t_rendas_prestacao_servicos, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_rendas_tarifas_bancarias, 0) - COALESCE(g.t_rendas_tarifas_bancarias, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_despesas_pessoal, 0) - COALESCE(g.t_despesas_pessoal, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_despesas_administrativas, 0) - COALESCE(g.t_despesas_administrativas, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_despesas_tributarias, 0) - COALESCE(g.t_despesas_tributarias, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_resultado_participacoes, 0) - COALESCE(g.t_resultado_participacoes, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_outras_receitas_operacionais, 0) - COALESCE(g.t_outras_receitas_operacionais, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_outras_despesas_operacionais, 0) - COALESCE(g.t_outras_despesas_operacionais, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_outras_receitas_despesas_operacionais, 0) - COALESCE(g.t_outras_receitas_despesas_operacionais, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_resultado_operacional, 0) - COALESCE(g.t_resultado_operacional, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_resultado_nao_operacional, 0) - COALESCE(g.t_resultado_nao_operacional, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_resultado_antes_tributacao, 0) - COALESCE(g.t_resultado_antes_tributacao, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_imposto_renda_contribuicao_social, 0) - COALESCE(g.t_imposto_renda_contribuicao_social, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_participacao_lucros, 0) - COALESCE(g.t_participacao_lucros, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_lucro_liquido, 0) - COALESCE(g.t_lucro_liquido, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_juros_sobre_capital, 0) - COALESCE(g.t_juros_sobre_capital, 0), 2) != 0
