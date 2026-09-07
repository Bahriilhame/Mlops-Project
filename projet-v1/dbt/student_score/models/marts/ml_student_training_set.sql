select
    study_hours,
    attendance_percentage,
    class_participation,
    total_score,
    case
        when total_score >= 85 then 'A'
        when total_score >= 70 then 'B'
        when total_score >= 55 then 'C'
        when total_score >= 40 then 'D'
        else 'F'
    end as derived_grade
from {{ ref('stg_student_performance') }}
where
    study_hours between 0 and 40
    and attendance_percentage between 0 and 100
    and class_participation between 0 and 10
    and total_score between 0 and 100
