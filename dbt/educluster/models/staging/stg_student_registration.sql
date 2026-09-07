SELECT
    code_module,
    code_presentation,
    id_student,
    date_registration,
    date_unregistration
FROM {{ source('raw', 'student_registration') }}