select
    station_id,
    station_name,
    period,
    period_start,
    period_end,
    alarm_count_rtw, mean_turnout_seconds_rtw,
    alarm_count_nef, mean_turnout_seconds_nef,
    alarm_count_lhf, mean_turnout_seconds_lhf,
    alarm_count_dlk, mean_turnout_seconds_dlk,
    alarm_count_elw, mean_turnout_seconds_elw,
    loaded_at
from {{ ref('stg_turnout_times') }}
where period_type = 'quarter'
