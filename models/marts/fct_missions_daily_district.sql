{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        unique_key='mission_date'
    )
}}

-- Grain: day x district x mission group x criticality tier.
-- Ingestion replaces whole year partitions with a fresh _loaded_at, so the incremental
-- filter re-aggregates every day of a reloaded year; delete+insert on mission_date
-- removes stale combinations of those days.
select
    mission_date,
    district_code,
    mission_group,
    criticality_tier,
    count(*) as mission_count,
    count(*) filter (where has_response_time) as mission_count_with_response_time,
    count(*) filter (where is_within_timegoal) as mission_count_within_timegoal,
    median(response_time_seconds) as response_time_median_seconds,
    avg(response_time_seconds) as response_time_mean_seconds,
    max(loaded_at) as loaded_at
from {{ ref('int_missions_enriched') }}
{% if is_incremental() %}
where loaded_at > (select max(loaded_at) from {{ this }})
{% endif %}
group by mission_date, district_code, mission_group, criticality_tier
