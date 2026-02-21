{{ config(materialized='table') }}

-- Financial Conglomerates Indexer
SELECT
    {{ generate_instituicao_id('codigo', "'Conglomerado Financeiro'") }} as id_instituicao,
    strftime(try_cast(data_base as date), '%Y%m%d')::int as id_data,
    
    total_geral as total_carteira,
    
    prefixado,
    selic,
    carteira_ativa_com_indexador_cdi as cdi,
    tr_tbf as tr,
    tjlp,
    tlp,
    libor,
    
    ipca,
    igpm,
    ipcc,
    outros_indices_de_preco,
    
    outras_taxas_pos_fixadas,
    outras_taxas_flutuantes,
    outros_indexadores,
    
    total_exterior,
    
    total_nao_individualizado

FROM {{ source('silver', 'financial_conglomerates_portfolio_indexer') }}

UNION ALL

-- Financial Conglomerates SCR Indexer
-- SCR table lacks: tlp, tcr_pre, tcr_pos, trfc_pre, trfc_pos
SELECT
    {{ generate_instituicao_id('codigo', "'Conglomerado Financeiro (SCR)'") }} as id_instituicao,
    strftime(try_cast(data_base as date), '%Y%m%d')::int as id_data,
    
    total_geral as total_carteira,
    
    prefixado,
    selic,
    carteira_ativa_com_indexador_cdi as cdi,
    tr_tbf as tr,
    tjlp,
    NULL as tlp,
    libor,
    
    ipca,
    igpm,
    ipcc,
    outros_indices_de_preco,
    
    outras_taxas_pos_fixadas,
    outras_taxas_flutuantes,
    outros_indexadores,
    
    total_exterior,
    
    total_nao_individualizado

FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_indexer') }}
