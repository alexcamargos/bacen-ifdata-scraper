{{ config(materialized='table') }}

-- Prudential Conglomerates (has all columns)
SELECT
    {{ generate_instituicao_id('codigo', "'Conglomerado Prudencial'") }} as id_instituicao,
    strftime(try_cast(data_base as date), '%Y%m%d')::int as id_data,
    
    -- Capital & Patrimônio de Referência
    capital_principal_para_comparacao_com_rwa as capital_principal,
    capital_complementar,
    patrimonio_referencia_nivel_i_para_comparacao_com_rwa as pr_nivel_1,
    capital_nivel_ii as capital_nivel_2,
    patrimonio_referencia_para_comparacao_com_rwa as pr_total,
    
    -- RWA (Risk Weighted Assets) e suas parcelas
    ativos_ponderados_pelo_risco_rwa as rwa_total,
    rwa_risco_credito,
    rwa_risco_mercado,
    rwa_risco_operacional,
    rwasp as rwa_servicos_pagamento,
    
    -- Detalhamento RWA Mercado
    rwacam as rwa_cambio,
    rwacom as rwa_commodities,
    rwajur as rwa_juros,
    rwaacs as rwa_acoes,
    rwacva as rwa_cva,
    rwadrc as rwa_drc,
    
    -- Exposição e Índices
    exposicao_total,
    indice_capital_principal,
    indice_capital_nivel_i,
    indice_basileia,
    razao_alavancagem,
    indice_imobilizacao,
    adicional_capital_principal

FROM {{ source('silver', 'prudential_conglomerates_capital_information') }}

UNION ALL

-- Financial Conglomerates (lacks: rwasp, rwacva, rwadrc, adicional_capital_principal)
SELECT
    {{ generate_instituicao_id('codigo', "'Conglomerado Financeiro'") }} as id_instituicao,
    strftime(try_cast(data_base as date), '%Y%m%d')::int as id_data,
    
    capital_principal_para_comparacao_com_rwa as capital_principal,
    capital_complementar,
    patrimonio_referencia_nivel_i_para_comparacao_com_rwa as pr_nivel_1,
    capital_nivel_ii as capital_nivel_2,
    patrimonio_referencia_para_comparacao_com_rwa as pr_total,
    
    ativos_ponderados_pelo_risco_rwa as rwa_total,
    rwa_risco_credito,
    rwa_risco_mercado,
    rwa_risco_operacional,
    NULL as rwa_servicos_pagamento,
    
    rwacam as rwa_cambio,
    rwacom as rwa_commodities,
    rwajur as rwa_juros,
    rwaacs as rwa_acoes,
    NULL as rwa_cva,
    NULL as rwa_drc,
    
    exposicao_total,
    indice_capital_principal,
    indice_capital_nivel_i,
    indice_basileia,
    razao_alavancagem,
    indice_imobilizacao,
    NULL as adicional_capital_principal

FROM {{ source('silver', 'financial_conglomerates_capital_information') }}
