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
