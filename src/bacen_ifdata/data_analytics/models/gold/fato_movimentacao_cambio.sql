{{ config(materialized='table') }}

SELECT
    -- Chaves Estrangeiras
    {{ generate_instituicao_id('codigo', "'Instituição de Câmbio'") }} as id_instituicao,
    strftime(data_base, '%Y%m%d')::int as id_data,
    
    -- Métricas de Operações Comerciais (Exportação/Importação)
    operacoes_comerciais_compra_numero_operacoes,
    operacoes_comerciais_compra_valor,
    operacoes_comerciais_venda_numero_operacoes,
    operacoes_comerciais_venda_valor,
    operacoes_comerciais_total_numero_operacoes,
    operacoes_comerciais_total_valor,

    -- Métricas de Operações Financeiras
    operacoes_financeiras_compra_numero_operacoes,
    operacoes_financeiras_compra_valor,
    operacoes_financeiras_venda_numero_operacoes,
    operacoes_financeiras_venda_valor,
    operacoes_financeiras_total_numero_operacoes,
    operacoes_financeiras_total_valor,

    -- Métricas do Mercado Primário
    mercado_primario_total_numero_operacoes,
    mercado_primario_total_valor,

    -- Métricas do Mercado Interbancário
    mercado_interbancario_compra_numero_operacoes,
    mercado_interbancario_compra_valor,
    mercado_interbancario_venda_numero_operacoes,
    mercado_interbancario_venda_valor,
    mercado_interbancario_total_numero_operacoes,
    mercado_interbancario_total_valor,

    -- Totais Gerais
    total_geral_numero_operacoes,
    total_geral_valor

FROM {{ source('silver', 'foreign_exchange_quarterly_foreign_currency_flow') }}
WHERE data_base IS NOT NULL
