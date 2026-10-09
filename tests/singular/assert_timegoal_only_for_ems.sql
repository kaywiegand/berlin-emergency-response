-- Only the ambulance service has a per-mission response-time goal; other groups must not carry the flag.
select mission_group, count(*) as flagged
from {{ ref('int_missions_enriched') }}
where is_within_timegoal is not null and mission_group <> 'ems'
group by 1
