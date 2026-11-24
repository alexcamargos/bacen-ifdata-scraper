{{ config(materialized='table') }}

{% set current_fields = source('silver', 'ifdata_2025_campos') %}

{% if execute and load_relation(current_fields) is not none %}
select
    strftime(data_base, '%Y%m%d')::integer as id_data,
    *
from {{ current_fields }}
{% else %}
select
    null::integer as id_data,
    null::varchar as escopo,
    null::varchar as relatorio,
    null::date as data_base,
    null::bigint as linha,
    null::integer as ordem_coluna,
    null::varchar as codigo,
    null::varchar as instituicao,
    null::varchar as campo_original,
    null::boolean as eh_dimensao,
    null::varchar as valor_original,
    null::decimal(38,8) as valor_numerico,
    null::varchar as formato_valor,
    null::varchar as arquivo_origem
where false
{% endif %}
