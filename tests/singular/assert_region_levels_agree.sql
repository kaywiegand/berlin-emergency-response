-- The three Regional_Data levels cover the same missions: yearly totals must be equal.
with totals as (
    select
        data_year,
        region_level,
        sum(mission_count_all) as total_missions
    from {{ ref('int_regional_timegoal') }}
    group by data_year, region_level
)

select data_year
from totals
group by data_year
having count(distinct total_missions) > 1
