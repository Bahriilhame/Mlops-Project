-- SELECT
--     sa.id_student,
--     a.code_module,
--     a.code_presentation,

--     COUNT(sa.id_assessment) AS assessment_count,

--     AVG(sa.score) AS avg_assessment_score,

--     MIN(sa.score) AS min_assessment_score,

--     MAX(sa.score) AS max_assessment_score,

--     STDDEV_POP(sa.score) AS assessment_score_std,

--     AVG(
--         CASE
--             WHEN sa.date_submitted > a.date
--             THEN 1
--             ELSE 0
--         END
--     ) AS late_submission_rate

-- FROM {{ ref('stg_student_assessment') }} sa

-- INNER JOIN {{ ref('stg_assessments') }} a
--     ON sa.id_assessment = a.id_assessment

-- GROUP BY
--     sa.id_student,
--     a.code_module,
--     a.code_presentation





{{ config(materialized='view') }}

WITH assessment_data AS (

    SELECT
        sa.id_student,
        a.code_module,
        a.code_presentation,
        sa.id_assessment,
        sa.date_submitted,
        a.date AS assessment_date,
        sa.score,

        CASE
            WHEN sa.date_submitted IS NOT NULL
             AND a.date IS NOT NULL
            THEN sa.date_submitted - a.date
            ELSE NULL
        END AS submission_delay

    FROM {{ ref('stg_student_assessment') }} sa

    INNER JOIN {{ ref('stg_assessments') }} a
        ON sa.id_assessment = a.id_assessment
),

student_assessment AS (

    SELECT
        id_student,
        code_module,
        code_presentation,

        COUNT(DISTINCT id_assessment) AS assessment_count,

        AVG(score) AS avg_assessment_score,
        MIN(score) AS min_assessment_score,
        MAX(score) AS max_assessment_score,
        STDDEV_SAMP(score) AS assessment_score_std,

        SUM(
            CASE
                WHEN submission_delay > 0 THEN 1
                ELSE 0
            END
        ) AS late_submission_count,

        AVG(
            CASE
                WHEN submission_delay > 0 THEN 1.0
                ELSE 0.0
            END
        ) AS late_submission_rate,

        AVG(submission_delay) AS avg_submission_delay,
        MEDIAN(submission_delay) AS median_submission_delay,
        MAX(submission_delay) AS max_submission_delay,

        AVG(
            CASE
                WHEN submission_delay <= 0 THEN 1.0
                ELSE 0.0
            END
        ) AS on_time_submission_rate

    FROM assessment_data

    GROUP BY
        id_student,
        code_module,
        code_presentation
),

expected_assessments AS (

    SELECT
        code_module,
        code_presentation,
        COUNT(DISTINCT id_assessment) AS expected_assessment_count

    FROM {{ ref('stg_assessments') }}

    GROUP BY
        code_module,
        code_presentation
)

SELECT
    sa.id_student,
    sa.code_module,
    sa.code_presentation,

    sa.assessment_count,
    ea.expected_assessment_count,

    CASE
        WHEN ea.expected_assessment_count > 0
        THEN sa.assessment_count * 1.0 / ea.expected_assessment_count
        ELSE 0
    END AS submission_rate,

    sa.avg_assessment_score,
    sa.min_assessment_score,
    sa.max_assessment_score,

    COALESCE(sa.assessment_score_std, 0)
        AS assessment_score_std,

    sa.late_submission_count,
    sa.late_submission_rate,

    COALESCE(sa.avg_submission_delay, 0)
        AS avg_submission_delay,

    COALESCE(sa.median_submission_delay, 0)
        AS median_submission_delay,

    COALESCE(sa.max_submission_delay, 0)
        AS max_submission_delay,

    sa.on_time_submission_rate

FROM student_assessment sa

LEFT JOIN expected_assessments ea
    ON sa.code_module = ea.code_module
    AND sa.code_presentation = ea.code_presentation