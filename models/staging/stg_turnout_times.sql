{%- set units = ['RTW', 'NEF', 'LHF', 'DLK', 'ELW'] -%}

select
    cast(wache_nummer as varchar) as station_id,
    wache_name as station_name,
    cast(start_date as date) as period_start,
    cast(end_date as date) as period_end,
    _partition as period,
    case when _partition = 'current' then 'rolling' else 'quarter' end as period_type,
    {%- for unit in units %}
    {{ to_int('anzahl_alarmierungen_' ~ unit) }} as alarm_count_{{ unit | lower }},
    {{ to_double('mittlere_ausrueckedauer_' ~ unit) }} as mean_turnout_seconds_{{ unit | lower }},
    {%- endfor %}
    _loaded_at as loaded_at
from {{ source('bf_open_data', 'raw_turnout_times') }}
-- upstream publishes template files for quarters that have not started yet
where cast(start_date as date) <= cast(_loaded_at as date)
