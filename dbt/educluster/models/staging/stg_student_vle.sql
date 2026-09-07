SELECT
    id_student,
    code_module,
    code_presentation,
    id_site,
    date,
    sum_click
FROM {{ source('raw', 'student_vle') }}