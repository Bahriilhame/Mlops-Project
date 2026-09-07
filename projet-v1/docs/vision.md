# Project Vision

## Project Name

EduScore MLOps - Student Score Prediction Platform

## Problem

Schools and training centers often detect academic risk too late. By estimating a student's final score from weekly study hours, attendance, and class participation, educators can identify students who may need support before the final evaluation.

## Objectives

- Build a reproducible DataOps pipeline from raw CSV to clean analytical data.
- Train a regression model that predicts `total_score`.
- Convert the predicted score into an interpretable grade.
- Expose the model through a FastAPI service.
- Track experiments, models, metrics, and artifacts using MLflow.
- Monitor prediction requests, response time, and simple data drift.

## Target Users

- Teachers who want early academic risk indicators.
- Academic coordinators who monitor student performance.
- Data/ML teams responsible for maintaining the prediction service.

## Business Value

- Early identification of students needing support.
- Data-driven educational decisions.
- Reproducible and maintainable ML lifecycle.
- Transparent monitoring of service and model behavior.

## Data Strategy

| Layer | Description |
| --- | --- |
| Source | Kaggle CSV file |
| Ingestion | dlt pipeline loads raw records |
| Storage | DuckDB local analytical database |
| Transformation | dbt models clean and standardize columns |
| Quality | data contract, dbt tests, pytest checks |
| ML | scikit-learn training with MLflow tracking |
| Serving | FastAPI prediction endpoint |
| Monitoring | prediction logs and drift checks |

## Data Consumers

- FastAPI service
- ML training pipeline
- Data analyst dashboards
- Project presentation and evaluation team
