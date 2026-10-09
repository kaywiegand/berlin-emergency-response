-- City-wide daily series from Daily_Data (official aggregates), kept for reconciliation, trend views and the BF-style charts.
-- Response-time columns are seconds; rd1..rd5 are ambulance emergency categories (RD1/RD2 are the critical ones).
select
    mission_date,
    mission_count_all,
    mission_count_ems,
    mission_count_ems_critical,
    mission_count_ems_critical_cpr,
    mission_count_fire,
    mission_count_technical_rescue,
    mission_count_rd1,
    mission_count_rd2,
    mission_count_rd3,
    mission_count_rd4,
    mission_count_rd5,
    response_time_ems_critical_mean,
    response_time_ems_critical_median,
    response_time_ems_critical_std,
    response_time_ems_critical_cpr_mean,
    response_time_ems_critical_cpr_median,
    response_time_fire_time_to_first_pump_mean,
    response_time_fire_time_to_first_ladder_mean,
    response_time_fire_time_to_full_crew_mean,
    response_time_technical_rescue_mean,
    response_time_technical_rescue_median,
    loaded_at
from {{ ref('stg_daily_missions') }}
