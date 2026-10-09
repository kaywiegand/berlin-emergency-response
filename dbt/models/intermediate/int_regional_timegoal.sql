-- LOR hierarchy is encoded in the ids: district = first 2 digits, prediction area = first 4,
-- Bezirksregion = first 6, planning room = 8.
with unioned as (
    select * from {{ ref('stg_regional_planning_room') }}
    union all by name
    select * from {{ ref('stg_regional_district_area') }}
    union all by name
    select * from {{ ref('stg_regional_prediction_area') }}
)

select
    *,
    left(region_id, 2) as district_code,
    {{ safe_pct('mission_count_ems_critical_timegoal_reached', 'mission_count_ems_critical_timegoal_computed') }}
        as ems_critical_timegoal_quote,
    {{ safe_pct('mission_count_fire_timegoal_reached', 'mission_count_fire_timegoal_computed') }}
        as fire_timegoal_quote
from unioned
