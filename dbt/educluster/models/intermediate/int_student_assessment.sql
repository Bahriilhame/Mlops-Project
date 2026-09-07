SELECT
    sa.id_student,
    a.code_module,
    a.code_presentation,

    COUNT(sa.id_assessment) AS assessment_count,

    AVG(sa.score) AS avg_assessment_score,

    MIN(sa.score) AS min_assessment_score,

    MAX(sa.score) AS max_assessment_score,

    STDDEV_POP(sa.score) AS assessment_score_std,

    AVG(
        CASE
            WHEN sa.date_submitted > a.date
            THEN 1
            ELSE 0
        END
    ) AS late_submission_rate

FROM {{ ref('stg_student_assessment') }} sa

INNER JOIN {{ ref('stg_assessments') }} a
    ON sa.id_assessment = a.id_assessment

GROUP BY
    sa.id_student,
    a.code_module,
    a.code_presentation