{{ config(materialized='view') }}

WITH fatos AS (
    SELECT * FROM {{ ref('fato_resumo_financeiro') }}
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
        consolidado_bancario
    FROM {{ ref('int_instituicao_enriquecida') }}
),
dim_tempo AS (
    SELECT * FROM {{ ref('dim_tempo') }}
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
