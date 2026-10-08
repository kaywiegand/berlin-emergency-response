select
    cast(mission_date as date) as mission_date,
    mission_type,
    dispatchcode_category as dispatchcode,
    dispatchcode_criticality as dispatch_criticality,
    mission_location_district as district_name,
    {{ to_int('response_time') }} as response_time_seconds,
    cast(units_non_berlin_involed as boolean) as units_non_berlin_involved,
    cast(units_several_involved as boolean) as units_several_involved,
    cast(units_reinforcements_called as boolean) as units_reinforcements_called,
    units_organisations,
    cast(firstresponder_alarmed as boolean) as firstresponder_alarmed,
    cast(firstresponder_indication as boolean) as firstresponder_indication,
    cast(firstresponder_first_arrival as boolean) as firstresponder_first_arrival,
    units_first_type,
    cast(emergency_doctor_involved as boolean) as emergency_doctor_involved,
    {{ to_int('_partition') }} as source_year,
    _loaded_at as loaded_at
from {{ source('bf_open_data', 'raw_mission_data') }}
