SELECT
    id_student,
    code_module,
    code_presentation,

    COUNT(*) AS total_vle_interactions,

    SUM(sum_click) AS total_clicks,

    COUNT(DISTINCT date) AS active_days,

    COUNT(DISTINCT id_site) AS unique_resources,

    AVG(sum_click) AS avg_clicks_per_event

FROM {{ ref('stg_student_vle') }}

GROUP BY
    id_student,
    code_module,
    code_presentation