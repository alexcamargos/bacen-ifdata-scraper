{{ config(materialized='table') }}

SELECT 
    id_atividade,
    nome_atividade,
    prefixo_coluna
FROM {{ ref('seed_dim_atividade') }}
