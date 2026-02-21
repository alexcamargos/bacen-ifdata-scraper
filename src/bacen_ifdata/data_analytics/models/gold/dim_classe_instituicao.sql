{{ config(materialized='table') }}

SELECT 
    md5(cast(codigo as varchar)) as id_classe,
    codigo,
    descricao
FROM {{ ref('seed_dim_classe_instituicao') }}
