select
    id_student,
    code_module,
    code_presentation,
    count(*) as duplicate_count
from {{ ref('student_learning_features') }}
group by 1, 2, 3
having count(*) > 1
