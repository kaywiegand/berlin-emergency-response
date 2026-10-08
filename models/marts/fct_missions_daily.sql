with enhanced_missions as (

    select * from {{ ref('int_missions_daily_enhanced') }}

),

final as (

    select
        mission_date,
        day_of_week,
        is_weekend,
        
        rescue_missions,
        fire_missions,
        total_missions,
        median_response_time_seconds,
        
        round(total_missions_7d_avg, 2) as total_missions_7d_avg,
        
        round(
            ((total_missions - total_missions_7d_avg) / nullif(total_missions_7d_avg, 0)) * 100, 
            2
        ) as pct_deviation_from_7d_avg

    from enhanced_missions

)

select * from final