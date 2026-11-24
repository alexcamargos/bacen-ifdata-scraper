{% set reports = [
    ('financial_conglomerates_portfolio_individuals_type_maturity', 'PF'),
    ('financial_conglomerates_scr_portfolio_individuals_type_maturity', 'PF'),
    ('financial_conglomerates_portfolio_legal_person_type_maturity', 'PJ'),
    ('financial_conglomerates_scr_portfolio_legal_person_type_maturity', 'PJ')
] %}

with silver_totais as (
    {% for report, tipo_pessoa in reports %}
    select
        {{ format_date_id('data_base') }} as id_data,
        '{{ tipo_pessoa }}' as tipo_pessoa,
        produto.id_produto,
        faixa.id_faixa as id_faixa_vencimento,
        count(*) as registros,
        sum(cast(valores.valor as decimal(38, 6))) as saldo
    from (
        unpivot {{ source('silver', report) }}
        on columns('_(vencido|a_vencer|vencer)_.*_dias$')
        into name coluna value valor
    ) as valores
    join {{ ref('dim_produto_credito') }} as produto
      on produto.tipo_pessoa in ('{{ tipo_pessoa }}', 'Ambos')
    join {{ ref('dim_faixa_vencimento') }} as faixa
      {% if report == 'financial_conglomerates_scr_portfolio_legal_person_type_maturity' %}
      on {{ historic_scr_product_column('valores.coluna') }} = produto.prefixo_coluna || faixa.sufixo_coluna
      {% else %}
      on valores.coluna = produto.prefixo_coluna || faixa.sufixo_coluna
      {% endif %}
    group by 1, 2, 3, 4
    {% if not loop.last %}union all{% endif %}
    {% endfor %}
),
silver as (
    select
        id_data, tipo_pessoa, id_produto, id_faixa_vencimento,
        sum(registros) as registros,
        sum(saldo) as saldo
    from silver_totais
    group by 1, 2, 3, 4
),
gold as (
    select
        id_data, tipo_pessoa, id_produto, id_faixa_vencimento,
        count(*) as registros,
        sum(cast(valor as decimal(38, 6))) as saldo
    from {{ ref('fato_carteira_credito_produto') }}
    group by 1, 2, 3, 4
)
select
    id_data, tipo_pessoa, id_produto, id_faixa_vencimento,
    silver.registros as registros_silver,
    gold.registros as registros_gold,
    silver.saldo as saldo_silver,
    gold.saldo as saldo_gold
from silver
full outer join gold
    using (id_data, tipo_pessoa, id_produto, id_faixa_vencimento)
where silver.registros is distinct from gold.registros
   or silver.saldo is distinct from gold.saldo
