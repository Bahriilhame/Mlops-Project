SELECT
    id_site,
    code_module,
    code_presentation,
    activity_type,
    week_from,
    week_to
FROM {{ source('raw', 'vle') }}