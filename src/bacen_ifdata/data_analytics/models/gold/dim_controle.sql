{{ config(materialized='table') }}

SELECT 
    md5(cast(codigo as varchar)) as id_controle,
    codigo,
    descricao
FROM {{ ref('seed_dim_controle') }}
