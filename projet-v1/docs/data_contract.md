# Data Contract

The pipeline accepts flexible source column names, then standardizes them to the canonical schema below.

## Canonical Schema

| Column | Type | Required | Rule |
| --- | --- | --- | --- |
| `study_hours` | float | yes | 0 <= value <= 40 |
| `attendance_percentage` | float | yes | 0 <= value <= 100 |
| `class_participation` | float | yes | 0 <= value <= 10 |
| `total_score` | float | training only | 0 <= value <= 100 |
| `grade` | string | optional | one of A, B, C, D, F |

## Accepted Source Aliases

| Canonical Column | Accepted Aliases |
| --- | --- |
| `study_hours` | `average_weekly_self_study_hours`, `weekly_self_study_hours`, `study_hours`, `hours_studied` |
| `attendance_percentage` | `attendance_percentage`, `attendance`, `attendance_rate` |
| `class_participation` | `class_participation`, `participation`, `participation_score` |
| `total_score` | `total_score`, `final_score`, `score`, `performance_score` |
| `grade` | `grade`, `final_grade` |

## Grade Rule

| Score Range | Grade |
| --- | --- |
| `score >= 85` | A |
| `70 <= score < 85` | B |
| `55 <= score < 70` | C |
| `40 <= score < 55` | D |
| `score < 40` | F |

## Quality Checks

- No missing values in required columns.
- Numeric ranges are respected.
- Target column exists for training.
- Grade values are valid if present.
- Duplicates are monitored.
