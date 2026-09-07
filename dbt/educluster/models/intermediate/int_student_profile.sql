{{ config(materialized='view') }}

SELECT
    id_student,
    code_module,
    code_presentation,

    gender,
    region,
    highest_education,
    imd_band,
    age_band,
    num_of_prev_attempts,
    studied_credits,
    disability,
    final_result

FROM {{ ref('stg_student_info') }}