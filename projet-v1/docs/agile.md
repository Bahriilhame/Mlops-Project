# Agile Organization

## Roles

| Role | Responsibility |
| --- | --- |
| Product Owner | Defines the educational value and validates features |
| Scrum Master | Organizes sprints and removes blockers |
| Data Engineer | Builds ingestion, DuckDB, dbt, and data quality |
| ML Engineer | Builds training, MLflow, registry, and model serving |
| Data Analyst | Explores data, validates metrics, prepares insights |

## Product Backlog

| ID | User Story | Priority |
| --- | --- | --- |
| US-01 | As a teacher, I want to predict a student's final score so that I can identify academic risk early. | High |
| US-02 | As a data engineer, I want raw data to be ingested automatically so that the pipeline is reproducible. | High |
| US-03 | As an ML engineer, I want experiments tracked in MLflow so that model versions can be compared. | High |
| US-04 | As a user, I want an API endpoint so that predictions can be consumed by other applications. | High |
| US-05 | As a project evaluator, I want data quality tests so that I can trust the pipeline. | High |
| US-06 | As a team, I want CI/CD so that code quality is checked automatically. | Medium |
| US-07 | As an operator, I want prediction monitoring so that I can detect service or data problems. | Medium |

## Sprint Planning

### Sprint 1 - Data Foundation

- Download dataset
- Create dlt ingestion pipeline
- Store data in DuckDB
- Create dbt staging model
- Define data contract

### Sprint 2 - Machine Learning

- Build preprocessing pipeline
- Train baseline and Random Forest models
- Evaluate using MAE, RMSE, and R2
- Track experiments with MLflow
- Save model artifact

### Sprint 3 - Deployment and Monitoring

- Create FastAPI service
- Add Docker support
- Add GitHub Actions workflow
- Add prediction logging
- Add simple drift monitoring
- Prepare final demo

## Sprint Review Template

| Sprint | Completed | Demo Evidence | Feedback |
| --- | --- | --- | --- |
| 1 | Data pipeline created | dlt + DuckDB + dbt run | Validate column names after Kaggle download |
| 2 | Model trained and tracked | MLflow run with metrics | Compare with another model if time allows |
| 3 | API and monitoring ready | `/health` and `/predict` working | Prepare final presentation |

## Sprint Retrospective Template

| Sprint | What Went Well | What To Improve | Action |
| --- | --- | --- | --- |
| 1 | Clear dataset and target | Dataset download requires Kaggle token | Document setup |
| 2 | Training reproducible | Need explainability | Add feature importance |
| 3 | API simple to demo | Monitoring is basic | Add dashboard later |
