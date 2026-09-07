with source as (
    select * from raw.student_performance
),

renamed as (
    select
        cast(study_hours as double) as study_hours,
        cast(attendance_percentage as double) as attendance_percentage,
        cast(class_participation as double) as class_participation,
        cast(total_score as double) as total_score,
        cast(grade as varchar) as grade
    from source
)

select * from renamed
