# Architecture

## Components

| Component | Tool | Role |
| --- | --- | --- |
| Source | Kaggle CSV | Raw student performance records |
| Ingestion | dlt | Reads CSV and loads DuckDB |
| Storage | DuckDB | Local analytical database |
| Transformation | dbt | Cleans names, types, and quality rules |
| Orchestration | Dagster | Runs ingestion, transformation, training |
| Experiment Tracking | MLflow | Tracks parameters, metrics, and artifacts |
| Model | scikit-learn | Predicts final score |
| Serving | FastAPI | Exposes `/predict` and `/health` |
| Containerization | Docker | Reproducible deployment |
| CI/CD | GitHub Actions | Tests, linting, Docker build |
| Monitoring | JSONL logs | Request, latency, prediction, drift input |

## Data Flow

```mermaid
flowchart TD
    A["CSV file"] --> B["Raw DuckDB table"]
    B --> C["dbt staging"]
    C --> D["ML dataset"]
    D --> E["Training"]
    E --> F["MLflow run"]
    E --> G["Saved model"]
    G --> H["FastAPI"]
```

## Deployment View

```mermaid
flowchart TD
    A["Client"] --> B["FastAPI container"]
    B --> C["Model artifact"]
    B --> D["Prediction logs"]
    E["MLflow UI"] --> F["Experiment runs"]
```
