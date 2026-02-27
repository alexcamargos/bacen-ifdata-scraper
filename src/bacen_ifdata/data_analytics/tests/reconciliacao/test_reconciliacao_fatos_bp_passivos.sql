{{ config(severity = 'error') }}

WITH silver_passivos AS (
    -- Conglomerados Prudenciais
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(depositos_vista, 0) as depositos_vista,
        COALESCE(depositos_poupanca, 0) as depositos_poupanca,
        COALESCE(depositos_interfinanceiros, 0) as depositos_interfinanceiros,
        COALESCE(depositos_a_prazo, 0) as depositos_a_prazo,
        COALESCE(conta_de_pagamento_pre_paga, 0) as conta_de_pagamento_pre_paga,
        COALESCE(depositos_outros, 0) as depositos_outros,
        COALESCE(deposito_total, 0) as depositos,
        COALESCE("obrigações_operações_compromissadas", 0) as captacoes_mercado_aberto,
        COALESCE(letras_de_credito_imobiliario, 0) as letras_de_credito_imobiliario,
        COALESCE(letras_de_credito_agronegocio, 0) as letras_de_credito_agronegocio,
        COALESCE(letras_financeiras, 0) as letras_financeiras,
        COALESCE(obrigacoes_titulos_e_valores_mobiliarios_exterior, 0) as obrigacoes_titulos_e_valores_mobiliarios_exterior,
        COALESCE(outros_recursos_de_aceites_e_emissao_de_titulos, 0) as outros_recursos_de_aceites_e_emissao_de_titulos,
        COALESCE(recursos_de_aceites_e_emissao_de_titulos, 0) as recursos_aceites_cambiais,
        COALESCE(obrigacoes_emprestimos_e_repasses, 0) as obrigacoes_emprestimos_repasses,
        COALESCE(captacoes, 0) as captacoes,
        COALESCE(instrumentos_derivativos, 0) as obrigacoes_por_instr_financeiros_derivativos,
        COALESCE("outras_obrigações", 0) as outras_obrigacoes,
        COALESCE("passivo_circulante_exigível_a_longo_prazo", 0) as passivo_circulante_exigivel_longo_prazo,
        COALESCE(patrimonio_liquido, 0) as patrimonio_liquido
    FROM (SELECT * FROM {{ source('silver', 'prudential_conglomerates_liabilities') }} QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY deposito_total DESC NULLS LAST, codigo) = 1)
    
    UNION ALL
    
    -- Conglomerados Financeiros
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(depositos_vista, 0) as depositos_vista,
        COALESCE(depositos_poupanca, 0) as depositos_poupanca,
        COALESCE(depositos_interfinanceiros, 0) as depositos_interfinanceiros,
        COALESCE(depositos_a_prazo, 0) as depositos_a_prazo,
        COALESCE(conta_de_pagamento_pre_paga, 0) as conta_de_pagamento_pre_paga,
        COALESCE(depositos_outros, 0) as depositos_outros,
        COALESCE(deposito_total, 0) as depositos,
        COALESCE(obrigacoes_operacoes_compromissadas, 0) as captacoes_mercado_aberto,
        COALESCE(letras_de_credito_imobiliario, 0) as letras_de_credito_imobiliario,
        COALESCE(letras_de_credito_agronegocio, 0) as letras_de_credito_agronegocio,
        COALESCE(letras_financeiras, 0) as letras_financeiras,
        COALESCE(obrigacoes_titulos_e_valores_mobiliarios_exterior, 0) as obrigacoes_titulos_e_valores_mobiliarios_exterior,
        COALESCE(outros_recursos_de_aceites_e_emissao_de_titulos, 0) as outros_recursos_de_aceites_e_emissao_de_titulos,
        COALESCE(recursos_de_aceites_e_emissao_de_titulos, 0) as recursos_aceites_cambiais,
        COALESCE(obrigacoes_emprestimos_e_repasses, 0) as obrigacoes_emprestimos_repasses,
        COALESCE(captacoes, 0) as captacoes,
        COALESCE(instrumentos_derivativos, 0) as obrigacoes_por_instr_financeiros_derivativos,
        COALESCE(outras_obrigacoes, 0) as outras_obrigacoes,
        COALESCE(passivo_circulante_exigivel_a_longo_prazo, 0) as passivo_circulante_exigivel_longo_prazo,
        COALESCE(patrimonio_liquido, 0) as patrimonio_liquido
    FROM (SELECT * FROM {{ source('silver', 'financial_conglomerates_liabilities') }} QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY deposito_total DESC NULLS LAST, codigo) = 1)
    
    UNION ALL
    
    -- Instituicoes Independentes
    SELECT
        {{ format_date_id('data_base') }} as id_data,
        COALESCE(depositos_vista, 0) as depositos_vista,
        COALESCE(depositos_poupanca, 0) as depositos_poupanca,
        COALESCE(depositos_interfinanceiros, 0) as depositos_interfinanceiros,
        COALESCE(depositos_a_prazo, 0) as depositos_a_prazo,
        COALESCE(conta_de_pagamento_pre_paga, 0) as conta_de_pagamento_pre_paga,
        COALESCE(depositos_outros, 0) as depositos_outros,
        COALESCE(deposito_total, 0) as depositos,
        COALESCE(obrigacoes_operacoes_compromissadas, 0) as captacoes_mercado_aberto,
        COALESCE(letras_de_credito_imobiliario, 0) as letras_de_credito_imobiliario,
        COALESCE(letras_de_credito_agronegocio, 0) as letras_de_credito_agronegocio,
        COALESCE(letras_financeiras, 0) as letras_financeiras,
        COALESCE(obrigacoes_titulos_e_valores_mobiliarios_exterior, 0) as obrigacoes_titulos_e_valores_mobiliarios_exterior,
        COALESCE(outros_recursos_de_aceites_e_emissao_de_titulos, 0) as outros_recursos_de_aceites_e_emissao_de_titulos,
        COALESCE(recursos_de_aceites_e_emissao_de_titulos, 0) as recursos_aceites_cambiais,
        COALESCE(obrigacoes_emprestimos_e_repasses, 0) as obrigacoes_emprestimos_repasses,
        COALESCE(captacoes, 0) as captacoes,
        COALESCE(instrumentos_derivativos, 0) as obrigacoes_por_instr_financeiros_derivativos,
        COALESCE(outras_obrigacoes, 0) as outras_obrigacoes,
        COALESCE(passivo_circulante_exigivel_a_longo_prazo, 0) as passivo_circulante_exigivel_longo_prazo,
        COALESCE(patrimonio_liquido, 0) as patrimonio_liquido
    FROM (SELECT * FROM {{ source('silver', 'individual_institutions_liabilities') }} QUALIFY ROW_NUMBER() OVER (PARTITION BY codigo, data_base ORDER BY deposito_total DESC NULLS LAST, codigo) = 1)
),

silver_agg AS (
    SELECT
        id_data,
        SUM(depositos_vista) as t_depositos_vista,
        SUM(depositos_poupanca) as t_depositos_poupanca,
        SUM(depositos_interfinanceiros) as t_depositos_interfinanceiros,
        SUM(depositos_a_prazo) as t_depositos_a_prazo,
        SUM(conta_de_pagamento_pre_paga) as t_conta_de_pagamento_pre_paga,
        SUM(depositos_outros) as t_depositos_outros,
        SUM(depositos) as t_depositos,
        SUM(captacoes_mercado_aberto) as t_captacoes_mercado_aberto,
        SUM(letras_de_credito_imobiliario) as t_letras_de_credito_imobiliario,
        SUM(letras_de_credito_agronegocio) as t_letras_de_credito_agronegocio,
        SUM(letras_financeiras) as t_letras_financeiras,
        SUM(obrigacoes_titulos_e_valores_mobiliarios_exterior) as t_obrigacoes_titulos_e_valores_mobiliarios_exterior,
        SUM(outros_recursos_de_aceites_e_emissao_de_titulos) as t_outros_recursos_de_aceites_e_emissao_de_titulos,
        SUM(recursos_aceites_cambiais) as t_recursos_aceites_cambiais,
        SUM(obrigacoes_emprestimos_repasses) as t_obrigacoes_emprestimos_repasses,
        SUM(captacoes) as t_captacoes,
        SUM(obrigacoes_por_instr_financeiros_derivativos) as t_obrigacoes_por_instr_financeiros_derivativos,
        SUM(outras_obrigacoes) as t_outras_obrigacoes,
        SUM(passivo_circulante_exigivel_longo_prazo) as t_passivo_circulante_exigivel_longo_prazo,
        SUM(patrimonio_liquido) as t_patrimonio_liquido
    FROM silver_passivos
    GROUP BY id_data
),

gold_agg AS (
    SELECT
        id_data,
        SUM(COALESCE(depositos_vista, 0)) as t_depositos_vista,
        SUM(COALESCE(depositos_poupanca, 0)) as t_depositos_poupanca,
        SUM(COALESCE(depositos_interfinanceiros, 0)) as t_depositos_interfinanceiros,
        SUM(COALESCE(depositos_a_prazo, 0)) as t_depositos_a_prazo,
        SUM(COALESCE(conta_de_pagamento_pre_paga, 0)) as t_conta_de_pagamento_pre_paga,
        SUM(COALESCE(depositos_outros, 0)) as t_depositos_outros,
        SUM(COALESCE(depositos, 0)) as t_depositos,
        SUM(COALESCE(captacoes_mercado_aberto, 0)) as t_captacoes_mercado_aberto,
        SUM(COALESCE(letras_de_credito_imobiliario, 0)) as t_letras_de_credito_imobiliario,
        SUM(COALESCE(letras_de_credito_agronegocio, 0)) as t_letras_de_credito_agronegocio,
        SUM(COALESCE(letras_financeiras, 0)) as t_letras_financeiras,
        SUM(COALESCE(obrigacoes_titulos_e_valores_mobiliarios_exterior, 0)) as t_obrigacoes_titulos_e_valores_mobiliarios_exterior,
        SUM(COALESCE(outros_recursos_de_aceites_e_emissao_de_titulos, 0)) as t_outros_recursos_de_aceites_e_emissao_de_titulos,
        SUM(COALESCE(recursos_aceites_cambiais, 0)) as t_recursos_aceites_cambiais,
        SUM(COALESCE(obrigacoes_emprestimos_repasses, 0)) as t_obrigacoes_emprestimos_repasses,
        SUM(COALESCE(captacoes, 0)) as t_captacoes,
        SUM(COALESCE(obrigacoes_por_instr_financeiros_derivativos, 0)) as t_obrigacoes_por_instr_financeiros_derivativos,
        SUM(COALESCE(outras_obrigacoes, 0)) as t_outras_obrigacoes,
        SUM(COALESCE(passivo_circulante_exigivel_longo_prazo, 0)) as t_passivo_circulante_exigivel_longo_prazo,
        SUM(COALESCE(patrimonio_liquido, 0)) as t_patrimonio_liquido
    FROM {{ ref('fato_balanco_patrimonial') }}
    GROUP BY id_data
)

SELECT
    COALESCE(s.id_data, g.id_data) as id_data,
    ROUND(s.t_depositos_vista - g.t_depositos_vista, 2) as diff_depositos_vista,
    ROUND(s.t_depositos_poupanca - g.t_depositos_poupanca, 2) as diff_depositos_poupanca,
    ROUND(s.t_depositos_interfinanceiros - g.t_depositos_interfinanceiros, 2) as diff_depositos_interfinanceiros,
    ROUND(s.t_depositos_a_prazo - g.t_depositos_a_prazo, 2) as diff_depositos_a_prazo,
    ROUND(s.t_conta_de_pagamento_pre_paga - g.t_conta_de_pagamento_pre_paga, 2) as diff_conta_de_pagamento_pre_paga,
    ROUND(s.t_depositos_outros - g.t_depositos_outros, 2) as diff_depositos_outros,
    ROUND(s.t_depositos - g.t_depositos, 2) as diff_depositos,
    ROUND(s.t_captacoes_mercado_aberto - g.t_captacoes_mercado_aberto, 2) as diff_captacoes_mercado_aberto,
    ROUND(s.t_letras_de_credito_imobiliario - g.t_letras_de_credito_imobiliario, 2) as diff_letras_de_credito_imobiliario,
    ROUND(s.t_letras_de_credito_agronegocio - g.t_letras_de_credito_agronegocio, 2) as diff_letras_de_credito_agronegocio,
    ROUND(s.t_letras_financeiras - g.t_letras_financeiras, 2) as diff_letras_financeiras,
    ROUND(s.t_obrigacoes_titulos_e_valores_mobiliarios_exterior - g.t_obrigacoes_titulos_e_valores_mobiliarios_exterior, 2) as diff_obrigacoes_titulos_e_valores_mobiliarios_exterior,
    ROUND(s.t_outros_recursos_de_aceites_e_emissao_de_titulos - g.t_outros_recursos_de_aceites_e_emissao_de_titulos, 2) as diff_outros_recursos_de_aceites_e_emissao_de_titulos,
    ROUND(s.t_recursos_aceites_cambiais - g.t_recursos_aceites_cambiais, 2) as diff_recursos_aceites_cambiais,
    ROUND(s.t_obrigacoes_emprestimos_repasses - g.t_obrigacoes_emprestimos_repasses, 2) as diff_obrigacoes_emprestimos_repasses,
    ROUND(s.t_captacoes - g.t_captacoes, 2) as diff_captacoes,
    ROUND(s.t_obrigacoes_por_instr_financeiros_derivativos - g.t_obrigacoes_por_instr_financeiros_derivativos, 2) as diff_obrigacoes_por_instr_financeiros_derivativos,
    ROUND(s.t_outras_obrigacoes - g.t_outras_obrigacoes, 2) as diff_outras_obrigacoes,
    ROUND(s.t_passivo_circulante_exigivel_longo_prazo - g.t_passivo_circulante_exigivel_longo_prazo, 2) as diff_passivo_circulante_exigivel_longo_prazo,
    ROUND(s.t_patrimonio_liquido - g.t_patrimonio_liquido, 2) as diff_patrimonio_liquido

FROM silver_agg s
FULL OUTER JOIN gold_agg g ON s.id_data = g.id_data
WHERE 
    ROUND(COALESCE(s.t_depositos_vista, 0) - COALESCE(g.t_depositos_vista, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_depositos_poupanca, 0) - COALESCE(g.t_depositos_poupanca, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_depositos_interfinanceiros, 0) - COALESCE(g.t_depositos_interfinanceiros, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_depositos_a_prazo, 0) - COALESCE(g.t_depositos_a_prazo, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_conta_de_pagamento_pre_paga, 0) - COALESCE(g.t_conta_de_pagamento_pre_paga, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_depositos_outros, 0) - COALESCE(g.t_depositos_outros, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_depositos, 0) - COALESCE(g.t_depositos, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_captacoes_mercado_aberto, 0) - COALESCE(g.t_captacoes_mercado_aberto, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_letras_de_credito_imobiliario, 0) - COALESCE(g.t_letras_de_credito_imobiliario, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_letras_de_credito_agronegocio, 0) - COALESCE(g.t_letras_de_credito_agronegocio, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_letras_financeiras, 0) - COALESCE(g.t_letras_financeiras, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_obrigacoes_titulos_e_valores_mobiliarios_exterior, 0) - COALESCE(g.t_obrigacoes_titulos_e_valores_mobiliarios_exterior, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_outros_recursos_de_aceites_e_emissao_de_titulos, 0) - COALESCE(g.t_outros_recursos_de_aceites_e_emissao_de_titulos, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_recursos_aceites_cambiais, 0) - COALESCE(g.t_recursos_aceites_cambiais, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_obrigacoes_emprestimos_repasses, 0) - COALESCE(g.t_obrigacoes_emprestimos_repasses, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_captacoes, 0) - COALESCE(g.t_captacoes, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_obrigacoes_por_instr_financeiros_derivativos, 0) - COALESCE(g.t_obrigacoes_por_instr_financeiros_derivativos, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_outras_obrigacoes, 0) - COALESCE(g.t_outras_obrigacoes, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_passivo_circulante_exigivel_longo_prazo, 0) - COALESCE(g.t_passivo_circulante_exigivel_longo_prazo, 0), 2) != 0 OR
    ROUND(COALESCE(s.t_patrimonio_liquido, 0) - COALESCE(g.t_patrimonio_liquido, 0), 2) != 0
