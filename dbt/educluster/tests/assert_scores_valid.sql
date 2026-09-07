SELECT *
FROM {{ ref('stg_student_assessment') }}
WHERE score < 0
   OR score > 100