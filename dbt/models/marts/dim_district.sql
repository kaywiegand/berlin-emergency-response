select
    district_code,
    district_name,
    district_short
from {{ ref('seed_districts') }}
