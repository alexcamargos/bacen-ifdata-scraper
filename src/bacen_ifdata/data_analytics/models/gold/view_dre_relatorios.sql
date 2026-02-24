{{ config(materialized='view') }}

WITH fatos AS (
    SELECT * FROM {{ ref('fato_demonstracao_resultado') }}
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
    
    -- DRE - Receitas Intermediação
    f.rendas_operacoes_de_credito,
    f.rendas_operacoes_de_arrendamento_mercantil,
    f.rendas_operacoes_tvm,
    f.rendas_operacoes_instrumentos_financeiros_derivativos,
    f.resultado_operacoes_cambio,
    f.rendas_aplicacoes_compulsorias,
    f.receitas_intermediacao_financeira,
    
    -- DRE - Despesas Intermediação
    f.despesas_captacao,
    f.despesas_obrigacoes_emprestimos_repasses,
    f.despesas_operacoes_arrendamento_mercantil,
    f.despesas_operacoes_cambio,
    f.resultado_provisao_creditos_dificil_liquidacao,
    f.despesas_intermediacao_financeira,
    
    -- DRE - Resultado Intermediação
    f.resultado_intermediacao_financeira,
    
    -- DRE - Outras Receitas/Despesas Operacionais
    f.rendas_prestacao_servicos,
    f.rendas_tarifas_bancarias,
    f.despesas_pessoal,
    f.despesas_administrativas,
    f.despesas_tributarias,
    f.resultado_participacoes,
    f.outras_receitas_operacionais,
    f.outras_despesas_operacionais,
    f.outras_receitas_despesas_operacionais,
    
    -- DRE - Resultados
    f.resultado_operacional,
    f.resultado_nao_operacional,
    f.resultado_antes_tributacao,
    f.imposto_renda_contribuicao_social,
    f.participacao_lucros,
    f.lucro_liquido,
    f.juros_sobre_capital,
    
    -- KPIs
    f.roe,
    f.roa

FROM fatos f
LEFT JOIN dim_inst i ON f.id_instituicao = i.id_instituicao
LEFT JOIN dim_tempo t ON f.id_data = t.id_data
LEFT JOIN dim_seg s ON i.id_segmento = s.id_segmento
LEFT JOIN dim_loc l ON i.id_localizacao = l.id_localizacao
LEFT JOIN dim_cont c ON i.id_controle = c.id_controle
LEFT JOIN dim_cons cb ON i.id_consolidado = cb.id_consolidado
LEFT JOIN dim_classe cl ON i.id_classe = cl.id_classe
