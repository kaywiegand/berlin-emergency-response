with grouped as (
    select
        m.*,
        d.district_code,
        case
            when m.mission_type like 'Rettungsdienst%' then 'ems'
            when m.mission_type = 'Brand' then 'fire'
            when m.mission_type = 'Technische Hilfeleistung' then 'technical'
            else 'other'
        end as mission_group
    from {{ ref('stg_missions') }} as m
    left join {{ ref('seed_districts') }} as d
        on m.district_name = d.district_name
)

select
    *,
    coalesce(dispatch_criticality, 'unknown') as criticality_tier,
    response_time_seconds is not null as has_response_time,
    {{ is_within_timegoal('response_time_seconds', 'mission_group') }} as is_within_timegoal
from grouped
