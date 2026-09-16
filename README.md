# Student Clustering MLOps — EduCluster

## 📌 Présentation

**Student Clustering MLOps (EduCluster)** est un projet de Machine Learning et de MLOps basé sur le dataset **OULAD (Open University Learning Analytics Dataset)**.

L'objectif est d'analyser les parcours et comportements des étudiants afin de construire des profils d'apprenants à l'aide de méthodes de **clustering non supervisé**.

Le projet met en œuvre une chaîne MLOps complète :

```text
Données OULAD
     ↓
DVC — versionnement des données
     ↓
dlt — ingestion
     ↓
DuckDB — stockage
     ↓
dbt — transformation et validation
     ↓
Feature Engineering / Preprocessing
     ↓
Clustering
     ↓
Évaluation
     ↓
MLflow — suivi des expériences
     ↓
FastAPI — API REST
     ↓
Dashboard React
     ↓
Docker
     ↓
GitHub Actions — CI
     ↓
Komodo — CD / déploiement
```

---

# 👥 Équipe du projet

Projet réalisé par :

- **MOHAMMED HMIMID**
- **Chakir Abderrahmane**
- **BAHRI ILHAME**
- **Aymene Chouki**
- **Aldiebes Ghanem ISRAA**
- **Khadija Zaafa**
- **Othman SALAHI**
- **Makrani Mohamed**

Projet réalisé dans le cadre du **Master en Intelligence Artificielle**.

---

# 🎯 Objectifs

Le projet vise à :

- versionner les données avec **DVC** ;
- ingérer les données avec **dlt** ;
- stocker les données avec **DuckDB** ;
- transformer et tester les données avec **dbt** ;
- construire les variables nécessaires au clustering ;
- appliquer plusieurs algorithmes de clustering ;
- comparer et évaluer les modèles ;
- suivre les expériences avec **MLflow** ;
- exposer les résultats avec une API **FastAPI** ;
- fournir un dashboard web avec **React/Vite** ;
- conteneuriser les composants avec **Docker** ;
- automatiser les tests avec **GitHub Actions** ;
- automatiser le déploiement avec **Komodo** après validation de la CI.

---

# 🏗️ Architecture globale

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
                         │ & Data Tests    │
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
                 │ K-Means / GMM / Agglomerative │
                 │             / DBSCAN           │
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
                         │    React/Vite   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │      Docker     │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │ GitHub Actions — CI      │
                    │ Tests + Build + Images    │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                         ┌─────────────────┐
                         │     Komodo      │
                         │       CD        │
                         │ Deploy Stack    │
                         └─────────────────┘
```

---

# 📊 Dataset

Le projet utilise le dataset **OULAD — Open University Learning Analytics Dataset**.

Les principales tables utilisées sont :

| Table | Description |
|---|---|
| `assessments.csv` | Informations sur les évaluations |
| `courses.csv` | Informations sur les cours |
| `studentAssessment.csv` | Résultats des étudiants aux évaluations |
| `studentInfo.csv` | Informations sur les étudiants |
| `studentRegistration.csv` | Informations d'inscription |
| `studentVle.csv` | Interactions avec les ressources pédagogiques |
| `vle.csv` | Informations sur les ressources pédagogiques |

Les données volumineuses sont gérées avec **DVC** afin de séparer le versionnement du code et celui des données.

---

# 🔧 Technologies utilisées

## Data Engineering

- Python
- dlt
- DuckDB
- dbt

## Machine Learning

- Pandas
- NumPy
- Scikit-learn
- K-Means
- Gaussian Mixture Model (GMM)
- Agglomerative Clustering
- DBSCAN

## MLOps

- DVC
- MLflow
- Dagster
- Docker
- GitHub Actions
- Komodo

## API & Frontend

- FastAPI
- Uvicorn
- React
- Vite
- Node.js
- npm

## Versionnement

- Git
- GitHub

---

# 🔄 Pipeline Data / ML

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

# 🤖 Clustering

Le projet compare plusieurs méthodes de clustering.

### K-Means

K-Means partitionne les étudiants en `K` groupes en minimisant la distance entre les observations et les centroïdes.

### Gaussian Mixture Model — GMM

GMM représente les données comme un mélange de distributions gaussiennes et attribue aux observations des probabilités d'appartenance aux groupes.

### Agglomerative Clustering

Cette méthode hiérarchique commence avec un cluster par observation puis fusionne progressivement les clusters.

### DBSCAN

DBSCAN est une méthode basée sur la densité qui permet également d'identifier les observations considérées comme du bruit.

---

# 📏 Évaluation

Les modèles de clustering sont comparés avec plusieurs métriques.

### Silhouette Score

Mesure la cohésion des observations à l'intérieur de leur cluster et leur séparation par rapport aux autres clusters.

**Plus le score est élevé, meilleur est le résultat.**

### Calinski-Harabasz Score

Compare la dispersion entre les clusters à la dispersion à l'intérieur des clusters.

**Plus le score est élevé, meilleur est le résultat.**

### Davies-Bouldin Score

Mesure la similarité entre les clusters.

**Plus le score est faible, meilleur est le résultat.**

---

# 📈 MLflow

**MLflow** permet de suivre les expérimentations de Machine Learning.

Il permet notamment de conserver :

- les paramètres ;
- les métriques ;
- les résultats des expériences ;
- les modèles ;
- les informations nécessaires pour comparer les expérimentations.

Lancer MLflow localement :

```powershell
mlflow ui --port 5000
```

Puis ouvrir :

```text
http://localhost:5000
```

Dans Docker Compose, MLflow est exposé sur le port `5001`.

---

# 🌐 API FastAPI

L'application expose le modèle de clustering à travers une API REST avec **FastAPI**.

## Installation locale

Depuis la racine du projet :

```powershell
py -3.12 -m venv .venv-dashboard
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

Le dashboard est développé avec **React/Vite**.

Installation :

```powershell
cd dashboard
npm ci
```

Lancement en développement :

```powershell
npm run dev
```

Construction de production :

```powershell
npm run build
```

---

# 🐳 Docker

Le projet contient trois services Docker :

```text
┌─────────────────────┐
│        API          │
│      FastAPI        │
│       :8002         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      MLflow         │
│       :5001         │
└─────────────────────┘

┌─────────────────────┐
│     Dashboard       │
│      React/Nginx    │
│       :8080         │
└─────────────────────┘
```

Les services sont définis dans :

```text
docker-compose.yml
```

Vérifier la configuration :

```powershell
docker compose config --quiet
```

Construire les images :

```powershell
docker compose build api dashboard mlflow dagster
```

Lancer l'application :

```powershell
docker compose up -d
```

Arrêter les services :

```powershell
docker compose down
```

---

# 🔁 CI/CD avec GitHub Actions et Komodo

## 1. Principe

Le projet utilise **GitHub Actions pour la CI** et **Komodo pour la CD**.

Le pipeline est :

```text
Developer
    │
    │ git push
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Tests API
    │
    ├── Tests frontend
    │
    ├── Build frontend
    │
    ├── Validation Docker Compose
    │
    └── Build des images Docker
              │
              ▼
        CI réussie
              │
              ▼
      Webhook sécurisé
              │
              ▼
          Komodo
              │
              ▼
       Deploy Stack
              │
              ▼
      API + Dashboard + MLflow
```

**Principe important :**

> Komodo ne doit être déclenché qu'après la réussite des vérifications CI.

Ainsi, une modification qui échoue aux tests ne doit pas provoquer de déploiement.

---

# ⚙️ 2. Workflow GitHub Actions

Le workflow se trouve dans :

```text
.github/workflows/ci-cd.yml
```

Il contient quatre jobs principaux :

```text
api
 │
 ├── Installation des dépendances
 ├── Tests de l'API
 └── Tests du mécanisme Komodo

frontend
 │
 ├── npm ci
 ├── Tests React
 └── npm run build

images
 │
 ├── docker compose config
 └── docker compose build

deploy
 │
 └── Webhook signé vers Komodo
```

Les trois premiers jobs sont exécutés avant le déploiement.

Le job `deploy` dépend de :

```yaml
needs: [api, frontend, images]
```

Il ne s'exécute que lorsqu'ils ont réussi et uniquement lors d'un push sur `main`.

---

# 🔐 3. Secrets GitHub

Les secrets ne doivent jamais être écrits directement dans le code.

Dans GitHub :

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Créer :

| Secret | Valeur |
|---|---|
| `KOMODO_WEBHOOK_URL` | URL HTTPS du webhook Deploy de la stack Komodo |
| `KOMODO_WEBHOOK_SECRET` | Secret configuré pour le webhook Komodo |

⚠️ Ne jamais mettre ces valeurs dans :

- `README.md`
- `.env`
- `ci-cd.yml`
- le code Python
- un commit Git

---

# 🖥️ 4. Configuration de Komodo

Dans Komodo, ouvrir la **Stack** utilisée pour le projet.

Vérifier :

### Repository

Le dépôt doit être :

```text
Bahriilhame/Mlops-Project
```

### Branch

```text
main
```

### Compose file

```text
docker-compose.yml
```

### Services

La stack doit utiliser les services :

```text
api
dashboard
mlflow
```

### Build

Conserver le mécanisme de build de la stack.

Le workflow GitHub vérifie déjà que les trois images peuvent être construites.

---

# 🔗 5. Webhook Komodo

Dans la configuration de la Stack Komodo :

```text
Stack
→ Config
→ Webhooks
```

Activer les webhooks et utiliser l'authentification **GitHub**.

Pour une Stack, Komodo fournit une URL de déploiement de type :

```text
https://<HOST>/listener/github/stack/<STACK_ID>/deploy
```

L'URL exacte doit toujours être copiée depuis l'interface Komodo de votre instance.

Configurer également le secret du webhook.

Le projet utilise ensuite :

```text
KOMODO_WEBHOOK_URL
KOMODO_WEBHOOK_SECRET
```

pour envoyer une requête signée depuis GitHub Actions.

---

# 🔒 6. Sécurisation du webhook

Le fichier :

```text
scripts/trigger_komodo.py
```

effectue plusieurs vérifications avant d'envoyer la requête :

- vérification que l'événement GitHub est un `push` ;
- vérification que la branche est `main` ;
- refus des suppressions de branche ;
- vérification que l'URL Komodo est en HTTPS ;
- signature HMAC-SHA256 du payload ;
- envoi de `X-GitHub-Event: push` ;
- envoi de `X-Hub-Signature-256`.

Le secret n'est donc pas exposé dans le dépôt.

---

# 🚀 7. Déclenchement du déploiement

Le développeur effectue :

```powershell
git add .
git commit -m "feat: update project"
git push origin main
```

GitHub Actions démarre automatiquement.

### Étape 1 — API

Les tests de l'API sont exécutés.

### Étape 2 — Frontend

Les tests React puis le build de production sont exécutés.

### Étape 3 — Docker

La configuration Docker Compose est vérifiée et les trois images sont construites :

```text
api
dashboard
mlflow
```

### Étape 4 — Deploy

Si les trois jobs précédents réussissent :

```text
GitHub Actions
       ↓
trigger_komodo.py
       ↓
Webhook HTTPS signé
       ↓
Komodo
       ↓
Deploy Stack
```

---

# 🧪 8. Vérification de la CI

Dans GitHub :

```text
Repository
→ Actions
→ EduCluster CI / Komodo CD
```

Vérifier que :

```text
✓ API and persisted models
✓ React tests and production build
✓ Validate Compose and build all three images
✓ Trigger existing Komodo stack
```

sont terminés avec succès.

---

# 📦 9. Vérification du déploiement dans Komodo

Après l'envoi du webhook :

```text
Komodo
→ Stack
→ Updates
```

Vérifier :

- le lancement du déploiement ;
- la récupération de la nouvelle révision ;
- la construction des services ;
- le démarrage de `api` ;
- le démarrage de `dashboard` ;
- le démarrage de `mlflow`.

Une réponse HTTP positive du webhook signifie seulement que Komodo a accepté la demande. Il faut ensuite vérifier **Updates** pour confirmer que le déploiement est réellement terminé.

---

# 🌍 10. Vérification de l'application déployée

Une fois le déploiement terminé, tester :

### API

```text
http://<SERVER>:8002
```

### Swagger

```text
http://<SERVER>:8002/docs
```

### Dashboard

```text
http://<SERVER>:8080
```

### MLflow

```text
http://<SERVER>:5001
```

Les ports et URLs publiques peuvent être différents selon la configuration de la Stack Komodo.

---

# ⚠️ 11. Ne pas configurer un deuxième déploiement GitHub

Dans cette architecture, le déploiement est déclenché par :

```text
GitHub Actions
      ↓
Webhook
      ↓
Komodo
```

Il ne faut donc pas ajouter en parallèle un webhook GitHub direct :

```text
GitHub Push
      ↓
Komodo Deploy
```

car cela pourrait provoquer un déploiement avant que la CI soit terminée.

L'objectif est de conserver :

```text
Push
 ↓
CI
 ↓
CI OK
 ↓
CD
 ↓
Komodo Deploy
```

---

# 🔄 12. DVC

DVC est utilisé pour le versionnement des données.

Vérifier le remote :

```powershell
dvc remote list
```

Récupérer les données :

```powershell
dvc pull
```

Envoyer une nouvelle version :

```powershell
dvc push
```

Le déploiement CI/CD actuel ne force pas un `dvc pull` et ne réentraîne pas automatiquement le modèle.

Le modèle et le scaler utilisés par l'API sont déjà présents dans le dépôt :

```text
models/
data/processed/scaler.joblib
```

---

# 🗄️ 13. dbt

Exécuter les transformations :

```powershell
dbt run
```

Exécuter les tests :

```powershell
dbt test
```

Le projet contient notamment les modèles :

```text
dbt/
└── educluster/
    ├── models/
    │   ├── staging/
    │   ├── intermediate/
    │   └── marts/
    └── tests/
```

---

# 🧰 14. Tests locaux avant un push

Avant de pousser sur `main`, il est recommandé de vérifier :

### API

```powershell
python -m unittest discover -s tests -p test_dashboard_api.py -v
```

### Test webhook

```powershell
python -m unittest discover -s tests -p test_komodo_webhook.py -v
```

### Frontend

```powershell
cd dashboard
npm ci
npm test
npm run build
```

### Docker

Depuis la racine :

```powershell
docker compose config --quiet
docker compose build api dashboard mlflow dagster
```

---

# 📁 Structure principale

```text
Mlops-Project/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── api/
│   ├── main.py
│   └── dashboard.py
│
├── dashboard/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dbt/
│   └── educluster/
│
├── ml/
│   ├── clustering.py
│   ├── prepare_data.py
│   ├── train_mlflow.py
│   └── visualization.py
│
├── models/
│   ├── kmeans_final.joblib
│   └── kmeans_k2.joblib
│
├── pipelines/
│   └── dagster_pipeline.py
│
├── scripts/
│   └── trigger_komodo.py
│
├── tests/
│   ├── test_dashboard_api.py
│   └── test_komodo_webhook.py
│
├── docs/
│   └── CI_CD_KOMODO.md
│
├── Dockerfile
├── Dockerfile.dagster
├── Dockerfile.mlflow
├── docker-compose.yml
├── dvc.yaml
├── dvc.lock
├── requirements.txt
├── requirements-dagster.txt
└── README.md
```

---

# 🚀 Quick Start local

## Terminal 1 — API

```powershell
py -3.12 -m venv .venv-dashboard
.\.venv-dashboard\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-dashboard\Scripts\python.exe -m uvicorn api.main:app --host localhost --port 8002
```

## Terminal 2 — Dashboard

```powershell
cd dashboard
npm ci
npm run dev
```

## Terminal 3 — MLflow

```powershell
mlflow ui --port 5000
```

---

# 🚀 Quick Start Docker

```powershell
docker compose config --quiet
docker compose build api dashboard mlflow dagster
docker compose up -d
```

Services déployés :

- Dashboard : `http://41.250.66.71:4203/`
- API : `http://41.250.66.71:4201/`
- MLflow : `http://41.250.66.71:4202/`
- Dagster : `http://41.250.66.71:4204/`

Vérifier les conteneurs :

```powershell
docker compose ps
```

Arrêter :

```powershell
docker compose down
```

---

# 🧑‍💻 Workflow de développement recommandé

```text
1. Modifier le code
       ↓
2. Tester localement
       ↓
3. git add .
       ↓
4. git commit
       ↓
5. git push origin main
       ↓
6. GitHub Actions
       ↓
7. Tests + Build
       ↓
8. CI réussie
       ↓
9. Webhook signé
       ↓
10. Komodo
       ↓
11. Deploy Stack
       ↓
12. Vérification de l'application
```

---

# 📚 Documentation Komodo

La documentation officielle Komodo décrit les webhooks entrants, leur authentification GitHub et les endpoints de déploiement des Stacks. urlDocumentation officielle Komodo — Webhookshttps://komo.do/docs/automate/webhooks

---

# 📌 Résultat final

Le projet fournit une chaîne MLOps reproductible allant de la donnée brute jusqu'au déploiement :

```text
             DATA
              │
              ▼
        DVC + dlt + DuckDB
              │
              ▼
             dbt
              │
              ▼
      Feature Engineering
              │
              ▼
         Clustering
              │
              ▼
          MLflow
              │
              ▼
           FastAPI
              │
              ▼
          Dashboard
              │
              ▼
           Docker
              │
              ▼
      GitHub Actions (CI)
              │
              ▼
        Komodo (CD)
              │
              ▼
        Production
```

L'architecture permet ainsi de séparer clairement :

- **Data Engineering** : ingestion, stockage et transformation ;
- **Machine Learning** : préparation, clustering et évaluation ;
- **MLOps** : versionnement, tracking, orchestration et reproductibilité ;
- **CI** : tests et validation automatique ;
- **CD** : déploiement automatisé avec Komodo ;
- **Application** : API et dashboard ;
- **Infrastructure** : Docker et Docker Compose.
