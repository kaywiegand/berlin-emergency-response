{#- Threshold per mission group (var timegoal_seconds is a map). Groups without an entry get null:
    only the ambulance service has a time goal that maps onto a single response time per mission. -#}
{% macro is_within_timegoal(response_time_col, group_col) -%}
    case
        when {{ response_time_col }} is null then null
        {%- for group, seconds in var('timegoal_seconds').items() %}
        when {{ group_col }} = '{{ group }}' then {{ response_time_col }} <= {{ seconds }}
        {%- endfor %}
        else null
    end
{%- endmacro %}


{% macro safe_pct(numerator, denominator) -%}
    case
        when {{ denominator }} is null or {{ denominator }} = 0 then null
        else cast({{ numerator }} as double) / {{ denominator }}
    end
{%- endmacro %}
