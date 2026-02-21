{{ config(materialized='table') }}

SELECT 
    id_produto,
    nome_produto,
    tipo_pessoa,
    prefixo_coluna
FROM {{ ref('seed_dim_produto_credito') }}
