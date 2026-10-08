-- City-wide daily series straight from Daily_Data, kept for reconciliation and trend views.
select
    mission_date,
    mission_count_all,
    mission_count_ems,
    mission_count_ems_critical,
    mission_count_fire,
    mission_count_technical_rescue,
    response_time_ems_critical_mean,
    response_time_ems_critical_median,
    loaded_at
from {{ ref('stg_daily_missions') }}
