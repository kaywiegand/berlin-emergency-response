with daily_missions as (

    select * from {{ ref('stg_missions_daily') }}

),

enhanced as (

    select
        mission_date,
        dayname(mission_date) as day_of_week,
        case 
            when dayofweek(mission_date) in (0, 6) then true 
            else false 
        end as is_weekend,
        
        rescue_missions,
        fire_missions,
        total_missions,
        median_response_time_seconds,

        -- 7-Tage rollierender Mittelwert
        avg(total_missions) over (
            order by mission_date
            rows between 6 preceding and current row
        ) as total_missions_7d_avg

    from daily_missions

)

select * from enhanced