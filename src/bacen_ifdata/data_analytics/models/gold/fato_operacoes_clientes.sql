{{ config(materialized='table') }}

WITH operacoes AS (
    SELECT
        codigo,
        data_base,
        quantidade_de_clientes_com_operacoes_ativas as quantidade_clientes,
        quantidade_de_operacoes_ativas as quantidade_operacoes,
        'Conglomerado Financeiro' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_portfolio_number_clients_operations') }}
    
    UNION ALL
    
    SELECT
        codigo,
        data_base,
        quantidade_de_clientes_com_operacoes_ativas as quantidade_clientes,
        quantidade_de_operacoes_ativas as quantidade_operacoes,
        'Conglomerado Financeiro (SCR)' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_number_clients_operations') }}
)

SELECT
    {{ generate_instituicao_id('codigo', 'tipo_instituicao') }} as id_instituicao,
    {{ format_date_id('data_base') }} as id_data,
    quantidade_clientes,
    quantidade_operacoes
FROM operacoes
