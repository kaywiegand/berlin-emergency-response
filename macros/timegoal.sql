{% macro is_within_timegoal(response_time_col) -%}
    case
        when {{ response_time_col }} is null then null
        else {{ response_time_col }} <= {{ var('timegoal_seconds') }}
    end
{%- endmacro %}


{% macro safe_pct(numerator, denominator) -%}
    case
        when {{ denominator }} is null or {{ denominator }} = 0 then null
        else cast({{ numerator }} as double) / {{ denominator }}
    end
{%- endmacro %}
