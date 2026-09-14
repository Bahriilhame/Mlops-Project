# Student Clustering MLOps

## 📌 Description

**Student Clustering MLOps** est un projet de Machine Learning et MLOps basé sur le dataset **OULAD (Open University Learning Analytics Dataset)**.

L'objectif du projet est d'analyser les comportements et les caractéristiques des étudiants afin de les regrouper en différents profils à l'aide d'algorithmes de **clustering non supervisé**.

Le projet met en place une chaîne MLOps complète, depuis la gestion et la transformation des données jusqu'à l'entraînement, l'évaluation, le suivi des expériences et l'exposition du modèle via une API.

---

## 🎯 Objectifs

- Versionner les données avec **DVC**
- Ingérer et stocker les données dans **DuckDB**
- Transformer les données avec **dbt**
- Construire les features nécessaires au Machine Learning
- Effectuer le preprocessing et le feature engineering
- Comparer plusieurs algorithmes de clustering
- Évaluer la qualité des clusters
- Suivre les expérimentations avec **MLflow**
- Orchestrer les différentes étapes du pipeline
- Exposer le modèle via une API **FastAPI**
- Fournir une interface utilisateur avec un **dashboard**
- Conteneuriser l'application avec **Docker**
- Automatiser les tests et le déploiement avec **CI/CD**

---

# 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │      OULAD      │
                         │   Raw Dataset   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │       DVC       │
                         │ Data Versioning │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │      dlt        │
                         │ Data Ingestion  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     DuckDB      │
                         │  Data Storage   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │      dbt        │
                         │ Transformation  │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │ Feature Engineering &    │
                    │      Preprocessing       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │          Clustering            │
                 │                                │
                 │ K-Means │ GMM │ Agglomerative  │
                 │         │ DBSCAN                │
                 └────────────────┬───────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Evaluation   │
                         │ Silhouette / CH │
                         │ Davies-Bouldin  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     MLflow      │
                         │ Experiment Track│
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         │    REST API     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Dashboard    │
                         │    Frontend     │
                         └─────────────────┘
```

---

# 📊 Dataset

Le projet utilise le dataset **OULAD (Open University Learning Analytics Dataset)**.

Les principales tables utilisées sont :

| Fichier                   | Description                                    |
| -------------------------- | ----------------------------------------------- |
| `assessments.csv`          | Informations sur les évaluations                |
| `courses.csv`               | Informations sur les cours                      |
| `studentAssessment.csv`    | Résultats des étudiants aux évaluations         |
| `studentInfo.csv`          | Informations sur les étudiants                  |
| `studentRegistration.csv`  | Informations d'inscription                      |
| `studentVle.csv`           | Interactions des étudiants avec les ressources  |
| `vle.csv`                  | Informations sur les ressources pédagogiques    |

---

# 🔧 Technologies utilisées

### Data Engineering

- Python
- dlt
- DuckDB
- dbt

### Machine Learning

- Pandas
- NumPy
- Scikit-learn
- K-Means
- Gaussian Mixture Model (GMM)
- Agglomerative Clustering
- DBSCAN

### MLOps

- DVC
- MLflow
- Dagster
- Docker
- GitHub Actions

### API & Frontend

- FastAPI
- Uvicorn
- Node.js
- npm
- Dashboard frontend

### Version Control

- Git
- GitHub

---

# 🔄 Pipeline MLOps

```text
OULAD
  │
  ▼
DVC
  │
  ▼
Data Ingestion
  │
  ▼
DuckDB
  │
  ▼
dbt
  │
  ▼
Data Validation
  │
  ▼
Feature Engineering
  │
  ▼
Preprocessing
  │
  ▼
Clustering
  │
  ▼
Evaluation
  │
  ▼
MLflow
  │
  ▼
FastAPI
  │
  ▼
Dashboard
```

---

# 📦 Gestion des données avec DVC

DVC est utilisé pour versionner les données du projet séparément du code source.

Le projet utilise un remote Google Drive pour le stockage des données.

### Vérifier le remote

```bash
dvc remote list
```

### Récupérer les données

```bash
dvc pull
```

### Envoyer les données vers le remote

```bash
dvc push
```

---

# 🗄️ dbt

Les données sont transformées et préparées avec **dbt**.

### Exécuter les modèles

```bash
dbt run
```

### Exécuter les tests

```bash
dbt test
```

---

# 🤖 Clustering

Le projet compare plusieurs méthodes de clustering.

## K-Means

K-Means partitionne les étudiants en K groupes en minimisant la distance entre les observations et les centroïdes.

## Gaussian Mixture Model

GMM représente les données comme un mélange de distributions gaussiennes.

## Agglomerative Clustering

Cette méthode hiérarchique commence avec un cluster par observation puis fusionne progressivement les clusters.

## DBSCAN

DBSCAN est une méthode basée sur la densité permettant également d'identifier les observations considérées comme du bruit.

---

# 📏 Évaluation

Les modèles sont comparés avec plusieurs métriques :

### Silhouette Score

Mesure la cohésion des clusters et leur séparation.

**Plus élevé = meilleur.**

### Calinski-Harabasz Score

Mesure le rapport entre la dispersion inter-clusters et intra-clusters.

**Plus élevé = meilleur.**

### Davies-Bouldin Score

Mesure la similarité entre les différents clusters.

**Plus faible = meilleur.**

---

# 📈 MLflow

MLflow est utilisé pour suivre les expérimentations de Machine Learning.

Il permet notamment de conserver :

- les paramètres
- les métriques
- les résultats des expérimentations
- les modèles expérimentés

### Lancer MLflow

```bash
mlflow ui --port 5000
```

MLflow sera disponible sur :

```text
http://localhost:5000
```

---

# 🌐 FastAPI

L'application expose le modèle à travers une API **FastAPI**.

## Installation

Depuis la racine du projet :

```powershell
cd Mlops-Project
```

Créer l'environnement virtuel :

```powershell
py -3.12 -m venv .venv-dashboard
```

Installer les dépendances :

```powershell
.\.venv-dashboard\Scripts\python.exe -m pip install -r requirements.txt
```

## Lancer l'API

```powershell
.\.venv-dashboard\Scripts\python.exe -m uvicorn api.main:app --host localhost --port 8002
```

API :

```text
http://localhost:8002
```

Documentation Swagger :

```text
http://localhost:8002/docs
```

---

# 🖥️ Dashboard

Le projet possède un dashboard permettant d'interagir avec l'application.

## Installation

Ouvrir un deuxième terminal :

```powershell
cd Mlops-Project\dashboard
```

Installer les dépendances :

```powershell
npm ci
```

Lancer le dashboard :

```powershell
npm run dev
```

L'URL locale du dashboard est affichée dans le terminal.

---

# 🔗 Communication Dashboard / API

```text
                  User
                   │
                   ▼
              Dashboard
                   │
                   │ HTTP Request
                   ▼
             FastAPI :8002
                   │
                   ▼
          Clustering Model
                   │
                   ▼
                Result
                   │
                   ▼
              Dashboard
```

---

# 🐳 Docker

Construire l'image Docker :

```bash
docker build -t student-clustering-mlops-api .
```

Lancer le conteneur :

```bash
docker run -p 8002:8002 student-clustering-mlops-api
```

---

# 🔁 CI/CD

Le projet utilise une approche CI/CD afin d'automatiser les différentes étapes du cycle de développement.

```text
git push
   │
   ▼
CI/CD Pipeline
   │
   ├── Tests
   │
   ├── Validation
   │
   ├── Build
   │
   ├── Docker
   │
   └── Deploy
```

La CI permet de vérifier automatiquement le projet après chaque modification.

La CD permet d'automatiser la livraison et le déploiement de l'application.

---

# 📁 Structure du projet

```text
Mlops-Project/
│
├── api/
│   └── main.py
│
├── dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dbt/
│   ├── models/
│   ├── tests/
│   └── dbt_project.yml
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   └── evaluation/
│
├── tests/
│
├── .dvc/
├── .github/
│   └── workflows/
│
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# 🚀 Quick Start

## Terminal 1 — Backend

```powershell
cd Mlops-Project

py -3.12 -m venv .venv-dashboard

.\.venv-dashboard\Scripts\python.exe -m pip install -r requirements.txt

.\.venv-dashboard\Scripts\python.exe -m uvicorn api.main:app --host localhost --port 8002
```

## Terminal 2 — Dashboard

```powershell
cd Mlops-Project\dashboard

npm ci

npm run dev
```

## Terminal 3 — MLflow

```powershell
mlflow ui --port 5000
```

---

# 👥 Projet académique

Projet réalisé dans le cadre du **Master en Intelligence Artificielle**.

Ce projet met en pratique les concepts de :

- Machine Learning
- Data Engineering
- MLOps
- Data Versioning
- Experiment Tracking
- API REST
- Containerisation
- CI/CD

---

# 📌 Résultat attendu

Le système permet de construire une chaîne complète de Machine Learning pour la segmentation des étudiants :

```text
Raw Data
   ↓
Data Versioning
   ↓
Data Engineering
   ↓
Feature Engineering
   ↓
Clustering
   ↓
Model Evaluation
   ↓
Experiment Tracking
   ↓
API
   ↓
Dashboard
   ↓
Deployment
```

L'objectif final est de disposer d'une solution **reproductible, versionnée, automatisée et déployable** suivant les bonnes pratiques MLOps.