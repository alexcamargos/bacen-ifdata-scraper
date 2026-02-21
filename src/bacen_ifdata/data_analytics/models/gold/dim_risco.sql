{{ config(materialized='table') }}

SELECT 
    id_risco,
    nome_risco,
    coluna
FROM {{ ref('seed_dim_risco') }}
