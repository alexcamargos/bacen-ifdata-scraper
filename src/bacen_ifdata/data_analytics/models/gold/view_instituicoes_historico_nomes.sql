{{ config(materialized='view') }}

WITH fatos AS (
    SELECT id_instituicao, id_data, nome_instituicao_historico FROM {{ ref('fato_resumo_financeiro') }}
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
),

base_historico AS (
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
        i.cidade,
        i.uf,
        i.regiao,
        i.tipo_de_controle,
        i.tcb,
        i.consolidado_bancario,
        i.classe_instituicao,
        
        -- Data
        t.data as data_base,
        
        -- Identificação da Mudança (De - Para)
        LAG(f.nome_instituicao_historico) OVER (
            PARTITION BY i.codigo_origem, i.tipo_instituicao 
            ORDER BY t.data ASC
        ) as nome_instituicao_anterior
        
    FROM fatos f
    LEFT JOIN dim_inst i ON f.id_instituicao = i.id_instituicao
    LEFT JOIN dim_tempo t ON f.id_data = t.id_data
)

SELECT
    id_instituicao,
    id_data,
    codigo_origem,
    nome_instituicao,
    nome_instituicao_anterior,
    nome_instituicao_historico,
    
    -- Flag útil para filtrar apenas os momentos exatos em que houve mudança nos nomes das insituições
    CASE 
        WHEN nome_instituicao_anterior IS NOT NULL AND nome_instituicao_anterior != nome_instituicao_historico THEN true
        ELSE false
    END as houve_mudanca_nome,
    
    tipo_instituicao,
    nome_conglomerado,
    tipo_relatorio_bcb,
    segmento,
    cidade,
    uf,
    regiao,
    tipo_de_controle,
    tcb,
    consolidado_bancario,
    classe_instituicao,
    data_base
FROM base_historico
