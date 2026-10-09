{%- set count_cols = [
    'mission_count_all', 'mission_count_ems', 'mission_count_ems_critical',
    'mission_count_ems_critical_cpr', 'mission_count_fire', 'mission_count_technical_rescue',
    'mission_count_rd1', 'mission_count_rd2', 'mission_count_rd3', 'mission_count_rd4', 'mission_count_rd5',
] -%}
{%- set kinds = ['ems_critical', 'ems_critical_cpr', 'fire_time_to_first_pump',
    'fire_time_to_first_ladder', 'fire_time_to_full_crew', 'technical_rescue'] -%}

select
    cast(mission_created_date as date) as mission_date,
    {%- for col in count_cols %}
    {{ to_int(col) }} as {{ col }},
    {%- endfor %}
    {%- for kind in kinds %}
    {%- for stat in ['mean', 'median', 'std'] %}
    {{ to_double('response_time_' ~ kind ~ '_' ~ stat) }} as response_time_{{ kind }}_{{ stat }},
    {%- endfor %}
    {%- endfor %}
    _loaded_at as loaded_at
from {{ source('bf_open_data', 'raw_daily_mission_data') }}
