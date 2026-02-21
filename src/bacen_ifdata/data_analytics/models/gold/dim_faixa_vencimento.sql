{{ config(materialized='table') }}

SELECT 
    id_faixa,
    nome_faixa,
    ordem,
    sufixo_coluna
FROM {{ ref('seed_dim_faixa_vencimento') }}
