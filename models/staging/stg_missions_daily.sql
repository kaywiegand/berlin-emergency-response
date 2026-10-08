with source as (

    select * from {{ source('berlin_emergency', 'raw_missions_daily') }}

),

renamed as (

    select
        cast(datum as date) as mission_date,
        cast(rettungsdienst_einsaetze as integer) as rescue_missions,
        cast(feuerwehr_einsaetze as integer) as fire_missions,
        cast(einsaetze_gesamt as integer) as total_missions,
        cast(antwortzeit_mediana as double) as median_response_time_seconds,
        _loaded_at as loaded_at

    from source

)

select * from renamed