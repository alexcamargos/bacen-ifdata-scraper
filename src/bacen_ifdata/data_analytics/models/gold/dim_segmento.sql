{{ config(materialized='table') }}

SELECT 
    md5(cast(codigo as varchar)) as id_segmento,
    codigo,
    descricao
FROM {{ ref('seed_dim_segmento') }}
