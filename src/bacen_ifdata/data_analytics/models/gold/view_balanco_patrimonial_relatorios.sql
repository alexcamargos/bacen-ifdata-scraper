{{ config(materialized='view') }}

WITH fatos AS (
    SELECT * FROM {{ ref('fato_balanco_patrimonial') }}
),
dim_inst AS (
    SELECT * FROM {{ ref('dim_instituicao') }}
),
dim_tempo AS (
    SELECT * FROM {{ ref('dim_tempo') }}
),
dim_seg AS (
    SELECT * FROM {{ ref('dim_segmento') }}
),
dim_loc AS (
    SELECT * FROM {{ ref('dim_localizacao') }}
),
dim_cont AS (
    SELECT * FROM {{ ref('dim_controle') }}
),
dim_cons AS (
    SELECT * FROM {{ ref('dim_consolidado') }}
),
dim_classe AS (
    SELECT * FROM {{ ref('dim_classe_instituicao') }}
)

SELECT
    f.id_instituicao,
    f.id_data,
    
    -- Instituição
    i.codigo_origem,
    i.nome as nome_instituicao,
    i.tipo_instituicao,
    i.nome_conglomerado,
    
    -- Tipo do Relatório Filtrado
    i.tipo_relatorio_bcb,
    
    -- Atributos Dimensionais
    s.descricao as segmento,
    l.cidade,
    l.uf,
    l.regiao,
    c.descricao as tipo_de_controle,
    cb.codigo as tcb,
    cb.descricao as consolidado_bancario,
    cl.descricao as classe_instituicao,
    
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
LEFT JOIN dim_seg s ON i.id_segmento = s.id_segmento
LEFT JOIN dim_loc l ON i.id_localizacao = l.id_localizacao
LEFT JOIN dim_cont c ON i.id_controle = c.id_controle
LEFT JOIN dim_cons cb ON i.id_consolidado = cb.id_consolidado
LEFT JOIN dim_classe cl ON i.id_classe = cl.id_classe
