{#- Raw tables are all VARCHAR; numeric strings may carry a decimal part ("253.0"). -#}
{% macro to_int(col) -%}
    cast(cast({{ col }} as double) as integer)
{%- endmacro %}


{% macro to_double(col) -%}
    cast({{ col }} as double)
{%- endmacro %}


{#- Shared shape of the three Regional_Data levels (planning room, district area, prediction area). -#}
{% macro stg_regional(source_table, level, id_col, name_col) -%}
{%- set count_cols = [
    'mission_count_all', 'mission_count_ems', 'mission_count_ems_critical',
    'mission_count_ems_critical_cpr', 'mission_count_fire', 'mission_count_technical_rescue',
    'mission_count_ems_critical_timegoal_computed', 'mission_count_fire_timegoal_computed',
    'mission_count_ems_critical_timegoal_reached', 'mission_count_fire_timegoal_reached',
] -%}
{%- set kinds = ['ems_critical', 'ems_critical_cpr', 'fire_time_to_first_pump',
    'fire_time_to_first_ladder', 'fire_time_to_full_crew', 'technical_rescue'] -%}

select
    '{{ level }}' as region_level,
    {{ id_col }} as region_id,
    {{ name_col }} as region_name,
    {{ to_int('_partition') }} as data_year,
    {%- for col in count_cols %}
    {{ to_int(col) }} as {{ col }},
    {%- endfor %}
    {%- for kind in kinds %}
    {%- for stat in ['mean', 'median', 'std'] %}
    {{ to_double('response_time_' ~ kind ~ '_' ~ stat) }} as response_time_{{ kind }}_{{ stat }},
    {%- endfor %}
    {%- endfor %}
    _loaded_at as loaded_at
from {{ source('bf_open_data', source_table) }}
{%- endmacro %}
