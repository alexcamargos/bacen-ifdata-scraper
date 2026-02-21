{{ config(materialized='table') }}

SELECT 
    id_porte,
    nome_porte,
    coluna
FROM {{ ref('seed_dim_porte') }}
