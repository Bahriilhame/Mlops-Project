SELECT
    id_assessment,
    id_student,
    date_submitted,
    is_banked,
    score
FROM {{ source('raw', 'student_assessment') }}