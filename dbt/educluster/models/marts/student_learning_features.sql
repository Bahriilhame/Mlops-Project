SELECT

    p.id_student,
    p.code_module,
    p.code_presentation,

    -- Demographic profile
    p.gender,
    p.region,
    p.highest_education,
    p.imd_band,
    p.age_band,
    p.num_of_prev_attempts,
    p.studied_credits,
    p.disability,

    -- Engagement
    COALESCE(e.total_vle_interactions, 0)
        AS total_vle_interactions,

    COALESCE(e.total_clicks, 0)
        AS total_clicks,

    COALESCE(e.active_days, 0)
        AS active_days,

    COALESCE(e.unique_resources, 0)
        AS unique_resources,

    COALESCE(e.avg_clicks_per_event, 0)
        AS avg_clicks_per_event,

    -- Assessments
    COALESCE(a.assessment_count, 0)
        AS assessment_count,

    a.avg_assessment_score,
    a.min_assessment_score,
    a.max_assessment_score,
    a.assessment_score_std,
    a.late_submission_rate,

    -- Target retained only for analysis
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