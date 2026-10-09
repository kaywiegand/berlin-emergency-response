-- Official Hilfsfrist figures per LOR region and year (Regional_Data, 2024 onward).
-- Note: the population of "critical" EMS missions changes between 2024 and 2025 (see seed_events).
select
    region_level,
    region_id,
    data_year,
    mission_count_all,
    mission_count_ems,
    mission_count_ems_critical,
    mission_count_ems_critical_timegoal_computed as ems_critical_timegoal_computed,
    mission_count_ems_critical_timegoal_reached as ems_critical_timegoal_reached,
    ems_critical_timegoal_quote,
    mission_count_fire,
    mission_count_fire_timegoal_computed as fire_timegoal_computed,
    mission_count_fire_timegoal_reached as fire_timegoal_reached,
    fire_timegoal_quote,
    response_time_ems_critical_mean,
    response_time_ems_critical_median,
    response_time_ems_critical_cpr_median,
    response_time_fire_time_to_first_pump_median,
    response_time_fire_time_to_full_crew_median,
    response_time_technical_rescue_median,
    loaded_at
from {{ ref('int_regional_timegoal') }}
