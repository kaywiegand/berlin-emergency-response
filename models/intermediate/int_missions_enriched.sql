select
    m.*,
    d.district_code,
    case
        when m.mission_type like 'Rettungsdienst%' then 'ems'
        when m.mission_type = 'Brand' then 'fire'
        when m.mission_type = 'Technische Hilfeleistung' then 'technical'
        else 'other'
    end as mission_group,
    coalesce(m.dispatch_criticality, 'unknown') as criticality_tier,
    m.response_time_seconds is not null as has_response_time,
    {{ is_within_timegoal('m.response_time_seconds') }} as is_within_timegoal
from {{ ref('stg_missions') }} as m
left join {{ ref('seed_districts') }} as d
    on m.district_name = d.district_name
