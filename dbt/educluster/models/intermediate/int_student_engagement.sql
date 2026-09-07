-- SELECT
--     id_student,
--     code_module,
--     code_presentation,

--     COUNT(*) AS total_vle_interactions,

--     SUM(sum_click) AS total_clicks,

--     COUNT(DISTINCT date) AS active_days,

--     COUNT(DISTINCT id_site) AS unique_resources,

--     AVG(sum_click) AS avg_clicks_per_event

-- FROM {{ ref('stg_student_vle') }}

-- GROUP BY
--     id_student,
--     code_module,
--     code_presentation

{{ config(materialized='view') }}

WITH daily_activity AS (

    SELECT
        id_student,
        code_module,
        code_presentation,
        date,
        SUM(sum_click) AS daily_clicks,
        COUNT(*) AS daily_interactions,
        COUNT(DISTINCT id_site) AS daily_unique_resources
    FROM {{ ref('stg_student_vle') }}
    GROUP BY
        id_student,
        code_module,
        code_presentation,
        date
),

activity_summary AS (

    SELECT
        id_student,
        code_module,
        code_presentation,

        SUM(daily_interactions) AS total_vle_interactions,
        SUM(daily_clicks) AS total_clicks,

        COUNT(DISTINCT date) AS active_days,
        COUNT(DISTINCT FLOOR(date / 7)) AS active_weeks,

        MIN(date) AS first_activity_day,
        MAX(date) AS last_activity_day,

        MAX(date) - MIN(date) + 1 AS activity_span_days,

        SUM(daily_unique_resources) AS unique_resource_visits,

        AVG(daily_clicks) AS avg_daily_clicks,
        MEDIAN(daily_clicks) AS median_daily_clicks,
        MAX(daily_clicks) AS max_daily_clicks,
        STDDEV_SAMP(daily_clicks) AS clicks_std,

        AVG(
            CASE
                WHEN daily_interactions > 0
                THEN daily_clicks * 1.0 / daily_interactions
                ELSE 0
            END
        ) AS avg_clicks_per_event

    FROM daily_activity

    GROUP BY
        id_student,
        code_module,
        code_presentation
),

activity_types AS (

    SELECT
        sv.id_student,
        sv.code_module,
        sv.code_presentation,

        SUM(
            CASE
                WHEN LOWER(v.activity_type) IN (
                    'oucontent',
                    'subpage',
                    'page',
                    'resource',
                    'url',
                    'folder',
                    'sharedsubpage'
                )
                THEN sv.sum_click
                ELSE 0
            END
        ) AS clicks_content,

        SUM(
            CASE
                WHEN LOWER(v.activity_type) LIKE '%forum%'
                THEN sv.sum_click
                ELSE 0
            END
        ) AS clicks_forum,

        SUM(
            CASE
                WHEN LOWER(v.activity_type) LIKE '%quiz%'
                  OR LOWER(v.activity_type) LIKE '%questionnaire%'
                THEN sv.sum_click
                ELSE 0
            END
        ) AS clicks_quiz,

        SUM(
            CASE
                WHEN LOWER(v.activity_type) LIKE '%wiki%'
                THEN sv.sum_click
                ELSE 0
            END
        ) AS clicks_wiki,

        SUM(
            CASE
                WHEN LOWER(v.activity_type) NOT IN (
                    'oucontent',
                    'subpage',
                    'page',
                    'resource',
                    'url',
                    'folder',
                    'sharedsubpage'
                )
                AND LOWER(v.activity_type) NOT LIKE '%forum%'
                AND LOWER(v.activity_type) NOT LIKE '%quiz%'
                AND LOWER(v.activity_type) NOT LIKE '%questionnaire%'
                AND LOWER(v.activity_type) NOT LIKE '%wiki%'
                THEN sv.sum_click
                ELSE 0
            END
        ) AS clicks_other

    FROM {{ ref('stg_student_vle') }} sv

    LEFT JOIN {{ ref('stg_vle') }} v
        ON sv.id_site = v.id_site

    GROUP BY
        sv.id_student,
        sv.code_module,
        sv.code_presentation
)

SELECT
    s.*,

    s.total_vle_interactions,
    s.total_clicks,
    s.active_days,
    s.active_weeks,
    s.first_activity_day,
    s.last_activity_day,
    s.activity_span_days,
    s.unique_resource_visits,
    s.avg_daily_clicks,
    s.median_daily_clicks,
    s.max_daily_clicks,
    COALESCE(s.clicks_std, 0) AS clicks_std,
    s.avg_clicks_per_event,

    COALESCE(a.clicks_content, 0) AS clicks_content,
    COALESCE(a.clicks_forum, 0) AS clicks_forum,
    COALESCE(a.clicks_quiz, 0) AS clicks_quiz,
    COALESCE(a.clicks_wiki, 0) AS clicks_wiki,
    COALESCE(a.clicks_other, 0) AS clicks_other,

    CASE
        WHEN s.total_clicks > 0
        THEN COALESCE(a.clicks_content, 0) * 1.0 / s.total_clicks
        ELSE 0
    END AS content_ratio,

    CASE
        WHEN s.total_clicks > 0
        THEN COALESCE(a.clicks_forum, 0) * 1.0 / s.total_clicks
        ELSE 0
    END AS forum_ratio,

    CASE
        WHEN s.total_clicks > 0
        THEN COALESCE(a.clicks_quiz, 0) * 1.0 / s.total_clicks
        ELSE 0
    END AS quiz_ratio,

    CASE
        WHEN s.total_clicks > 0
        THEN COALESCE(a.clicks_wiki, 0) * 1.0 / s.total_clicks
        ELSE 0
    END AS wiki_ratio,

    CASE
        WHEN s.total_clicks > 0
        THEN COALESCE(a.clicks_other, 0) * 1.0 / s.total_clicks
        ELSE 0
    END AS other_ratio

FROM activity_summary s

LEFT JOIN activity_types a
    ON s.id_student = a.id_student
    AND s.code_module = a.code_module
    AND s.code_presentation = a.code_presentation