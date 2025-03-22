{%macro test_date_format_is_valid(model, column_name) %}

with date_validation as (
  select
    {{column_name}} as date_field
    from {{model}}
    where {{column_name}} is not null
      and (
        -- check format yyyy-mm-dd
        not regexp_like({{ column_name}}, '^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
        -- check can be cast to date type
        or try_to_date({{column_name}}) is null
        -- TODO: make sure date is not in yyyy-dd-mm format
      )
)

select *
from date_validation

{%endmacro%}
