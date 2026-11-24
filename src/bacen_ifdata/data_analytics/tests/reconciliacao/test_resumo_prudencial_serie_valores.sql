with historical as (
    select
        data_base,
        cast(codigo as varchar) as codigo,
        cast(ativo_total as decimal(38,8)) as ativo_total,
        cast(patrimonio_liquido as decimal(38,8)) as patrimonio_liquido
    from {{ source('silver', 'prudential_conglomerates_summary') }}
),
published as (
    select
        data_base, codigo, campo_original, valor_numerico,
        'cosif_desde_2025' as regime_contabil
    from {{ ref('fato_ifdata_2025_campos') }}
    where escopo = 'prudential_conglomerates'
      and relatorio = 'summary'
      and campo_original in ('Ativo Total', 'Patrimônio Líquido')
    union all
    select
        data_base, codigo, 'Ativo Total', ativo_total, 'cosif_ate_2024'
    from historical
    union all
    select
        data_base, codigo, 'Patrimônio Líquido', patrimonio_liquido,
        'cosif_ate_2024'
    from historical
),
queried as (
    select data_base, codigo, 'Ativo Total' as campo_original,
        ativo_total as valor_numerico, regime_contabil
    from {{ ref('view_resumo_prudencial_serie') }}
    union all
    select
        data_base, codigo, 'Patrimônio Líquido', patrimonio_liquido,
        regime_contabil
    from {{ ref('view_resumo_prudencial_serie') }}
)
(select * from published except all select * from queried)
union all
(select * from queried except all select * from published)
