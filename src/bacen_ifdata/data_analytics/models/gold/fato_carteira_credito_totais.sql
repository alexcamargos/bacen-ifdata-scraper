{{ config(materialized='table') }}

WITH totais AS (
    -- =================================================================================================
    -- PESSOA JURÍDICA (PJ)
    -- =================================================================================================
    
    -- Conglomerados Financeiros - Atividade Econômica
    SELECT 
        codigo,
        data_base,
        total_carteira_pessoa_juridica as total_carteira_pj,
        total_nao_individualizado_pessoa_juridica as total_nao_individualizado_pj,
        total_exterior_pessoa_juridica as total_exterior_pj,
        NULL as total_geral_risco,
        NULL as total_carteira_pf,
        NULL as total_exterior_pf,
        'Conglomerado Financeiro' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_portfolio_legal_person_economic_activity') }}

    UNION ALL

    -- SCR - Atividade Econômica
    SELECT 
        codigo,
        data_base,
        total_da_carteira_de_pessoa_juridica as total_carteira_pj,
        NULL as total_nao_individualizado_pj,
        total_exterior_pessoa_juridica as total_exterior_pj,
        NULL as total_geral_risco,
        NULL as total_carteira_pf,
        NULL as total_exterior_pf,
        'Conglomerado Financeiro (SCR)' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_legal_person_economic_activity') }}

    UNION ALL

    -- =================================================================================================
    -- RISCO (TOTAL GERAL)
    -- =================================================================================================

    -- Conglomerados Financeiros - Risco
    SELECT
        codigo,
        data_base,
        NULL as total_carteira_pj,
        NULL as total_nao_individualizado_pj,
        NULL as total_exterior_pj,
        total_geral as total_geral_risco,
        NULL as total_carteira_pf,
        NULL as total_exterior_pf,
        'Conglomerado Financeiro' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_portfolio_risk_level') }}

    UNION ALL

    -- SCR - Risco
    SELECT
        codigo,
        data_base,
        NULL as total_carteira_pj,
        NULL as total_nao_individualizado_pj,
        NULL as total_exterior_pj,
        total_geral as total_geral_risco,
        NULL as total_carteira_pf,
        NULL as total_exterior_pf,
        'Conglomerado Financeiro (SCR)' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_risk_level') }}

    UNION ALL

    -- =================================================================================================
    -- PESSOA FÍSICA (PF)
    -- =================================================================================================

    -- Conglomerados Financeiros - PF Tipo/Vencimento
    SELECT
        codigo,
        data_base,
        NULL as total_carteira_pj,
        NULL as total_nao_individualizado_pj,
        NULL as total_exterior_pj,
        NULL as total_geral_risco,
        total_carteira_pessoa_fisica as total_carteira_pf,
        total_exterior_pessoa_fisica as total_exterior_pf,
        'Conglomerado Financeiro' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_portfolio_individuals_type_maturity') }}

    UNION ALL

    -- SCR - PF Tipo/Vencimento
    SELECT
        codigo,
        data_base,
        NULL as total_carteira_pj,
        NULL as total_nao_individualizado_pj,
        NULL as total_exterior_pj,
        NULL as total_geral_risco,
        total_da_carteira_de_pessoa_fisica as total_carteira_pf,
        total_exterior_pessoa_fisica as total_exterior_pf,
        'Conglomerado Financeiro (SCR)' as tipo_instituicao
    FROM {{ source('silver', 'financial_conglomerates_scr_portfolio_individuals_type_maturity') }}
)

SELECT
    {{ generate_instituicao_id('codigo', 'tipo_instituicao') }} as id_instituicao,
    strftime(try_cast(data_base as date), '%Y%m%d')::int as id_data,
    -- Agregando por instituição e data
    MAX(total_carteira_pj) as total_carteira_pj,
    MAX(total_nao_individualizado_pj) as total_nao_individualizado_pj,
    MAX(total_exterior_pj) as total_exterior_pj,
    MAX(total_geral_risco) as total_geral_risco,
    MAX(total_carteira_pf) as total_carteira_pf,
    MAX(total_exterior_pf) as total_exterior_pf
FROM totais
GROUP BY 1, 2
