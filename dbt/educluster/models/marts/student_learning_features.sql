-- SELECT

--     p.id_student,
--     p.code_module,
--     p.code_presentation,

--     -- Demographic profile
--     p.gender,
--     p.region,
--     p.highest_education,
--     p.imd_band,
--     p.age_band,
--     p.num_of_prev_attempts,
--     p.studied_credits,
--     p.disability,

--     -- Engagement
--     COALESCE(e.total_vle_interactions, 0)
--         AS total_vle_interactions,

--     COALESCE(e.total_clicks, 0)
--         AS total_clicks,

--     COALESCE(e.active_days, 0)
--         AS active_days,

--     COALESCE(e.unique_resources, 0)
--         AS unique_resources,

--     COALESCE(e.avg_clicks_per_event, 0)
--         AS avg_clicks_per_event,

--     -- Assessments
--     COALESCE(a.assessment_count, 0)
--         AS assessment_count,

--     a.avg_assessment_score,
--     a.min_assessment_score,
--     a.max_assessment_score,
--     a.assessment_score_std,
--     a.late_submission_rate,

--     -- Target retained only for analysis
--     p.final_result

-- FROM {{ ref('int_student_profile') }} p

-- LEFT JOIN {{ ref('int_student_engagement') }} e
--     ON p.id_student = e.id_student
--     AND p.code_module = e.code_module
--     AND p.code_presentation = e.code_presentation

-- LEFT JOIN {{ ref('int_student_assessment') }} a
--     ON p.id_student = a.id_student
--     AND p.code_module = a.code_module
--     AND p.code_presentation = a.code_presentation


{{ config(materialized='table') }}

SELECT
    p.id_student,
    p.code_module,
    p.code_presentation,

    p.gender,
    p.region,
    p.highest_education,
    p.imd_band,
    p.age_band,
    p.num_of_prev_attempts,
    p.studied_credits,
    p.disability,

    COALESCE(e.total_vle_interactions, 0)
        AS total_vle_interactions,

    COALESCE(e.total_clicks, 0)
        AS total_clicks,

    COALESCE(e.active_days, 0)
        AS active_days,

    COALESCE(e.active_weeks, 0)
        AS active_weeks,

    COALESCE(e.activity_span_days, 0)
        AS activity_span_days,

    COALESCE(e.unique_resource_visits, 0)
        AS unique_resource_visits,

    COALESCE(e.avg_daily_clicks, 0)
        AS avg_daily_clicks,

    COALESCE(e.median_daily_clicks, 0)
        AS median_daily_clicks,

    COALESCE(e.max_daily_clicks, 0)
        AS max_daily_clicks,

    COALESCE(e.clicks_std, 0)
        AS clicks_std,

    COALESCE(e.avg_clicks_per_event, 0)
        AS avg_clicks_per_event,

    COALESCE(e.clicks_content, 0)
        AS clicks_content,

    COALESCE(e.clicks_forum, 0)
        AS clicks_forum,

    COALESCE(e.clicks_quiz, 0)
        AS clicks_quiz,

    COALESCE(e.clicks_wiki, 0)
        AS clicks_wiki,

    COALESCE(e.clicks_other, 0)
        AS clicks_other,

    COALESCE(e.content_ratio, 0)
        AS content_ratio,

    COALESCE(e.forum_ratio, 0)
        AS forum_ratio,

    COALESCE(e.quiz_ratio, 0)
        AS quiz_ratio,

    COALESCE(e.wiki_ratio, 0)
        AS wiki_ratio,

    COALESCE(e.other_ratio, 0)
        AS other_ratio,

    COALESCE(a.assessment_count, 0)
        AS assessment_count,

    COALESCE(a.expected_assessment_count, 0)
        AS expected_assessment_count,

    COALESCE(a.submission_rate, 0)
        AS submission_rate,

    COALESCE(a.avg_assessment_score, 0)
        AS avg_assessment_score,

    COALESCE(a.min_assessment_score, 0)
        AS min_assessment_score,

    COALESCE(a.max_assessment_score, 0)
        AS max_assessment_score,

    COALESCE(a.assessment_score_std, 0)
        AS assessment_score_std,

    COALESCE(a.late_submission_count, 0)
        AS late_submission_count,

    COALESCE(a.late_submission_rate, 0)
        AS late_submission_rate,

    COALESCE(a.avg_submission_delay, 0)
        AS avg_submission_delay,

    COALESCE(a.median_submission_delay, 0)
        AS median_submission_delay,

    COALESCE(a.max_submission_delay, 0)
        AS max_submission_delay,

    COALESCE(a.on_time_submission_rate, 0)
        AS on_time_submission_rate,

    p.final_result

FROM {{ ref('int_student_profile') }} p

LEFT JOIN {{ ref('int_student_engagement') }} e
    ON p.id_student = e.id_student
    AND p.code_module = e.code_module
    AND p.code_presentation = e.code_presentation

LEFT JOIN {{ ref('int_student_assessment') }} a
    ON p.id_student = a.id_student
    AND p.code_module = a.code_module
    AND p.code_presentation = a.code_presentation