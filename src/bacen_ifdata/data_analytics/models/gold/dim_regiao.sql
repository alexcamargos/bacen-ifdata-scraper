{{ config(materialized='table') }}

SELECT 
    id_regiao,
    nome_regiao,
    coluna
FROM {{ ref('seed_dim_regiao') }}
