SELECT
    id_assessment,
    code_module,
    code_presentation,
    assessment_type,
    date,
    weight
FROM {{ source('raw', 'assessments') }}