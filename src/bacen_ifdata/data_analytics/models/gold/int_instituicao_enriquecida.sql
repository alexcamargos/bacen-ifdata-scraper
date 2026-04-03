{{ config(materialized='table') }}

WITH dim_inst AS (
    SELECT
        id_instituicao,
        codigo_origem,
        nome AS nome_instituicao,
        tipo_instituicao,
        tipo_relatorio_bcb,
        id_segmento,
        id_localizacao,
        id_controle,
        id_consolidado,
        id_classe,
        nome_conglomerado
    FROM {{ ref('dim_instituicao') }}
),
dim_seg AS (
    SELECT
        id_segmento,
        upper(codigo) AS segmento,
        descricao AS segmento_descricao
    FROM {{ ref('dim_segmento') }}
),
dim_loc AS (
    SELECT
        id_localizacao,
        cidade,
        uf,
        regiao
    FROM {{ ref('dim_localizacao') }}
),
dim_cont AS (
    SELECT
        id_controle,
        descricao AS tipo_de_controle
    FROM {{ ref('dim_controle') }}
),
dim_cons AS (
    SELECT
        id_consolidado,
        codigo AS tcb,
        descricao AS consolidado_bancario
    FROM {{ ref('dim_consolidado') }}
),
dim_classe AS (
    SELECT
        id_classe,
        descricao AS classe_instituicao
    FROM {{ ref('dim_classe_instituicao') }}
)

SELECT
    i.id_instituicao,
    i.codigo_origem,
    i.nome_instituicao,
    i.tipo_instituicao,
    i.nome_conglomerado,
    i.tipo_relatorio_bcb,
    s.segmento,
    s.segmento_descricao,
    l.cidade,
    l.uf,
    l.regiao,
    c.tipo_de_controle,
    cb.tcb,
    cb.consolidado_bancario,
    cl.classe_instituicao
FROM dim_inst i
LEFT JOIN dim_seg s ON i.id_segmento = s.id_segmento
LEFT JOIN dim_loc l ON i.id_localizacao = l.id_localizacao
LEFT JOIN dim_cont c ON i.id_controle = c.id_controle
LEFT JOIN dim_cons cb ON i.id_consolidado = cb.id_consolidado
LEFT JOIN dim_classe cl ON i.id_classe = cl.id_classe
