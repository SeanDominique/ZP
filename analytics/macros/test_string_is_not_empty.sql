{% macro test_string_is_not_empty(model, column_name) %}

with validation as (
    select
        {{ column_name }} as string_field
    from {{ model }}
),

validation_errors as (
    select
        string_field
    from validation
    where string_field = ''
       or regexp_like(string_field, '^\s*$')
)

select * from validation_errors

{% endmacro %}
