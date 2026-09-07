SELECT
    code_module,
    code_presentation,
    module_presentation_length
FROM {{ source('raw', 'courses') }}