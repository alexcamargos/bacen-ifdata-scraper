{{ config(materialized='view') }}

WITH fatos AS (
    SELECT * FROM {{ ref('fato_resumo_financeiro') }}
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
    
    -- Data
    t.data as data_base,
    
    -- Fatos (Métricas dbt)
    f.ativo_total,
    f.carteira_credito,
    f.passivo_exigivel,
    f.captacoes,
    f.patrimonio_liquido,
    f.lucro_liquido,
    f.quantidade_agencias,
    f.quantidade_postos_atendimento,
    f.roe,
    f.roa

FROM fatos f
LEFT JOIN dim_inst i ON f.id_instituicao = i.id_instituicao
LEFT JOIN dim_tempo t ON f.id_data = t.id_data
LEFT JOIN dim_seg s ON i.id_segmento = s.id_segmento
LEFT JOIN dim_loc l ON i.id_localizacao = l.id_localizacao
LEFT JOIN dim_cont c ON i.id_controle = c.id_controle
LEFT JOIN dim_cons cb ON i.id_consolidado = cb.id_consolidado
