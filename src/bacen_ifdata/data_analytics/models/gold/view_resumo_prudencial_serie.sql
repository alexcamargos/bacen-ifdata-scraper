{{ config(materialized='view') }}

with historico as (
    select
        t.data as data_base,
        cast(i.codigo_origem as varchar) as codigo,
        r.nome_instituicao_historico as instituicao,
        cast(r.ativo_total as decimal(38,8)) as ativo_total,
        cast(r.patrimonio_liquido as decimal(38,8)) as patrimonio_liquido,
        'cosif_ate_2024' as regime_contabil
    from {{ ref('fato_resumo_financeiro') }} r
    join {{ ref('dim_instituicao') }} i using (id_instituicao)
    join {{ ref('dim_tempo') }} t using (id_data)
    where i.tipo_instituicao = 'Conglomerado Prudencial'
),
atual as (
    select
        data_base,
        codigo,
        instituicao,
        max(valor_numerico) filter (
            where campo_original = 'Ativo Total'
        ) as ativo_total,
        max(valor_numerico) filter (
            where campo_original = 'Patrimônio Líquido'
        ) as patrimonio_liquido,
        'cosif_desde_2025' as regime_contabil
    from {{ ref('fato_ifdata_2025_campos') }}
    where escopo = 'prudential_conglomerates'
      and relatorio = 'summary'
      and campo_original in ('Ativo Total', 'Patrimônio Líquido')
    group by data_base, codigo, instituicao
)
select
    *,
    'prudential_conglomerates' as escopo,
    'BRL mil' as unidade
from (
    select * from historico
    union all by name
    select * from atual
)
