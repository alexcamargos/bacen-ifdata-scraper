{{ config(materialized='view') }}

WITH fatos AS (
    SELECT
        id_instituicao,
        id_data,
        nome_instituicao_historico,
        disponibilidades,
        aplicacoes_interfinanceiras_liquidez,
        tvm_derivativos,
        operacoes_de_credito,
        provisao_operacoes_de_credito,
        operacoes_de_credito_liquidas_provisao,
        arrendamento_mercantil_a_receber,
        imobilizado_de_arrendamento,
        credores_antecipacao_valor_residual,
        provisao_arrendamento_mercantil,
        arrendamento_mercantil_liquido_de_provisao,
        outros_creditos_liquido_de_provisao,
        outros_ativos_realizaveis,
        permanente_ajustado,
        ativo_total_ajustado,
        ativo_total,
        depositos_vista,
        depositos_poupanca,
        depositos_interfinanceiros,
        depositos_a_prazo,
        conta_de_pagamento_pre_paga,
        depositos_outros,
        depositos,
        captacoes_mercado_aberto,
        letras_de_credito_imobiliario,
        letras_de_credito_agronegocio,
        letras_financeiras,
        obrigacoes_titulos_e_valores_mobiliarios_exterior,
        outros_recursos_de_aceites_e_emissao_de_titulos,
        recursos_aceites_cambiais,
        obrigacoes_emprestimos_repasses,
        captacoes,
        obrigacoes_por_instr_financeiros_derivativos,
        outras_obrigacoes,
        passivo_circulante_exigivel_longo_prazo,
        patrimonio_liquido,
        passivo_total
    FROM {{ ref('fato_balanco_patrimonial') }}
),
dim_inst AS (
    SELECT
        id_instituicao,
        codigo_origem,
        nome_instituicao,
        tipo_instituicao,
        nome_conglomerado,
        tipo_relatorio_bcb,
        segmento,
        segmento_descricao,
        cidade,
        uf,
        regiao,
        tipo_de_controle,
        tcb,
        consolidado_bancario,
        classe_instituicao
    FROM {{ ref('int_instituicao_enriquecida') }}
),
dim_tempo AS (
    SELECT
        id_data,
        data
    FROM {{ ref('dim_tempo') }}
)

SELECT
    f.id_instituicao,
    f.id_data,
    
    -- Instituição
    i.codigo_origem,
    i.nome_instituicao,
    f.nome_instituicao_historico,
    i.tipo_instituicao,
    i.nome_conglomerado,
    
    -- Tipo do Relatório Filtrado
    i.tipo_relatorio_bcb,
    
    -- Atributos Dimensionais
    i.segmento,
    i.segmento_descricao,
    i.cidade,
    i.uf,
    i.regiao,
    i.tipo_de_controle,
    i.tcb,
    i.consolidado_bancario,
    i.classe_instituicao,
    
    -- Data
    t.data as data_base,
    
    -- Fatos Ativo
    f.disponibilidades,
    f.aplicacoes_interfinanceiras_liquidez,
    f.tvm_derivativos,
    f.operacoes_de_credito,
    f.provisao_operacoes_de_credito,
    f.operacoes_de_credito_liquidas_provisao,
    f.arrendamento_mercantil_a_receber,
    f.imobilizado_de_arrendamento,
    f.credores_antecipacao_valor_residual,
    f.provisao_arrendamento_mercantil,
    f.arrendamento_mercantil_liquido_de_provisao,
    f.outros_creditos_liquido_de_provisao,
    f.outros_ativos_realizaveis,
    f.permanente_ajustado,
    f.ativo_total_ajustado,
    f.ativo_total,
    
    -- Fatos Passivo
    f.depositos_vista,
    f.depositos_poupanca,
    f.depositos_interfinanceiros,
    f.depositos_a_prazo,
    f.conta_de_pagamento_pre_paga,
    f.depositos_outros,
    f.depositos,
    f.captacoes_mercado_aberto,
    f.letras_de_credito_imobiliario,
    f.letras_de_credito_agronegocio,
    f.letras_financeiras,
    f.obrigacoes_titulos_e_valores_mobiliarios_exterior,
    f.outros_recursos_de_aceites_e_emissao_de_titulos,
    f.recursos_aceites_cambiais,
    f.obrigacoes_emprestimos_repasses,
    f.captacoes,
    f.obrigacoes_por_instr_financeiros_derivativos,
    f.outras_obrigacoes,
    f.passivo_circulante_exigivel_longo_prazo,
    f.patrimonio_liquido,
    f.passivo_total

FROM fatos f
LEFT JOIN dim_inst i ON f.id_instituicao = i.id_instituicao
LEFT JOIN dim_tempo t ON f.id_data = t.id_data
