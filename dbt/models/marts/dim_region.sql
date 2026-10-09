-- One row per LOR region and level; name from the latest year it appears in.
select
    region_level,
    region_id,
    district_code,
    case region_level
        when 'planning_room' then left(region_id, 6)
        else null
    end as district_area_id,
    case region_level
        when 'prediction_area' then null
        else left(region_id, 4)
    end as prediction_area_id,
    arg_max(region_name, data_year) as region_name,
    min(data_year) as first_year,
    max(data_year) as last_year
from {{ ref('int_regional_timegoal') }}
group by region_level, region_id, district_code
