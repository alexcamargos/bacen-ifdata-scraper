{{ config(materialized='view') }}

WITH fatos AS (
    SELECT id_instituicao, id_data, nome_instituicao_historico FROM {{ ref('fato_resumo_financeiro') }}
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
),

base_historico AS (
    SELECT
        f.id_instituicao,
        f.id_data,
        
        -- Instituição
        i.codigo_origem,
        i.nome as nome_instituicao,
        f.nome_instituicao_historico,
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
        
        -- Identificação da Mudança (De - Para)
        LAG(f.nome_instituicao_historico) OVER (
            PARTITION BY i.codigo_origem, i.tipo_instituicao 
            ORDER BY t.data ASC
        ) as nome_instituicao_anterior
        
    FROM fatos f
    LEFT JOIN dim_inst i ON f.id_instituicao = i.id_instituicao
    LEFT JOIN dim_tempo t ON f.id_data = t.id_data
    LEFT JOIN dim_seg s ON i.id_segmento = s.id_segmento
    LEFT JOIN dim_loc l ON i.id_localizacao = l.id_localizacao
    LEFT JOIN dim_cont c ON i.id_controle = c.id_controle
    LEFT JOIN dim_cons cb ON i.id_consolidado = cb.id_consolidado
    LEFT JOIN dim_classe cl ON i.id_classe = cl.id_classe
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
