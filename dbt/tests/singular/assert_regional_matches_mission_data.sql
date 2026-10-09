-- Bezirksregion totals must match the mission count of the same year within 1 %.
with regional as (
    select data_year, sum(mission_count_all) as regional_count
    from {{ ref('int_regional_timegoal') }}
    where region_level = 'district_area'
    group by data_year
),

missions as (
    select source_year, count(*) as mission_count
    from {{ ref('stg_missions') }}
    group by source_year
)

select r.data_year, r.regional_count, m.mission_count
from regional as r
inner join missions as m on r.data_year = m.source_year
where abs(r.regional_count - m.mission_count) > 0.01 * m.mission_count
