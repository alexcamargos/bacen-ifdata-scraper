{% macro generate_instituicao_id(codigo_column, tipo_column=None) %}
    {% if tipo_column %}
        md5(cast(cast({{ codigo_column }} as bigint) as varchar) || {{ tipo_column }})
    {% else %}
        md5(cast(cast({{ codigo_column }} as bigint) as varchar))
    {% endif %}
{% endmacro %}

{% macro format_date_id(date_column) %}
    strftime(try_cast({{ date_column }} as date), '%Y%m%d')::int
{% endmacro %}

{% macro historic_scr_product_column(column_name) %}
    regexp_replace(
        regexp_replace(
            {{ column_name }}, '^operacoes_com_recebiveis_', 'operacoes_recebiveis_'
        ),
        '^(operacoes_recebiveis|comercio_exterior|outros_creditos)_a_vencer_de_([0-9]+)_ate_([0-9]+)_dias$',
        '\1_a_vencer_\2_a_\3_dias'
    )
{% endmacro %}
