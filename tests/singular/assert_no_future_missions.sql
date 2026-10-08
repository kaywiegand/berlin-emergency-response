select mission_date
from {{ ref('stg_missions') }}
where mission_date > current_date
