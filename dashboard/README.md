# EduCluster — Dashboard React

Application de présentation pour **Analyse des parcours d’apprentissage**, connectée à FastAPI. React, Vite, Tailwind CSS, Recharts et Lucide React. Le modèle, le scaler et les transformations restent exclusivement côté API.

## Démarrage local

Prérequis : Node.js 24 LTS et l’environnement Python du projet. Python 3.11 ou 3.12 est recommandé pour scikit-learn 1.5.1, version des modèles enregistrés.

Terminal API, depuis la racine du projet, dans son environnement Python activé :

```powershell
cd C:\Users\ISRAA\Mlops-Project
python -m pip install -r requirements.txt
python -m uvicorn api.main:app --host localhost --port 8002
```

Terminal frontend :

```powershell
cd C:\Users\ISRAA\Mlops-Project\dashboard
npm ci
Copy-Item .env.example .env
npm run dev
```

La copie du fichier `.env` est facultative avec les valeurs locales par défaut. Ne pas écraser un `.env` déjà personnalisé. Ouvrir **http://localhost:5173**. Garder les deux terminaux ouverts ; Ctrl+C pour arrêter. Le serveur Python de l’ancien dashboard a été remplacé par Vite.

Si vous devez créer un environnement API séparé :

```powershell
cd C:\Users\ISRAA\Mlops-Project
py -3.12 -m venv .venv-dashboard
.\.venv-dashboard\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-dashboard\Scripts\python.exe -m uvicorn api.main:app --host localhost --port 8002
```

## Configuration

| Variable | Valeur locale par défaut | Usage |
| --- | --- | --- |
| `VITE_API_URL` | `http://localhost:8002` | URL de FastAPI vue par le navigateur |
| `VITE_MLFLOW_URL` | `http://localhost:5001` | Lien de navigation MLflow |
| `DASHBOARD_PORT` | `8080` | Port hôte du service Docker dashboard |
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:4173,http://localhost:8080` | Origines frontend autorisées, séparées par des virgules |

Les variables `VITE_*` sont publiques et intégrées lors du **build**. Après leur modification, redémarrer Vite en développement ou reconstruire l’image en production. Une variable d’environnement ajoutée uniquement au conteneur Nginx ne modifie pas le bundle compilé. Ne jamais y placer de secret.

Le fichier `dashboard/.env` configure Vite en local. Le `.env` à la racine configure les arguments de build et le port dans Docker Compose. Le fichier racine `.env.example` documente ces paramètres. Pour une API lancée directement par Python, exporter `CORS_ORIGINS` dans son terminal, par exemple `$env:CORS_ORIGINS = 'http://localhost:5173'`.

## Fonctionnement

- **Dashboard** : quatre indicateurs, répartition en donut, profils des segments, évaluation et présentation du projet.
- **Prediction** : 34 champs obligatoires organisés en cinq sections, validation numérique, gestion des valeurs absentes, attente, prévention des doubles soumissions, erreurs API et affichage du cluster/profil renvoyé.
- Les valeurs restent brutes dans le navigateur. FastAPI conserve `log1p`, `StandardScaler`, puis `KMeans.predict`.
- Les comptages sont positifs ou nuls, les proportions entre 0 et 1, les notes entre 0 et 100. Les délais négatifs sont autorisés. Aucun remplissage fictif automatique.
- « At-Risk » désigne un profil de faible engagement, pas une classification certaine de l’échec.
- La navigation utilise des fragments d’URL pour fonctionner avec Nginx et un déploiement statique.

## Endpoints

Les routes existantes `GET /`, `GET /health`, `POST /predict` sont conservées. La fonction de prédiction n’est pas modifiée.

`GET /statistics` : total et effectifs/pourcentages des segments. Priorité à `cluster_sizes` dans `data/processed/kmeans_metrics.json`, puis au CSV `clustered_students.csv`. La colonne `cluster` est agrégée sans transmettre de données personnelles au navigateur. Le total est un nombre d’inscriptions segmentées ; un étudiant OULAD peut avoir plusieurs inscriptions.

`GET /model-info` : algorithme et nombre de clusters du modèle chargé, nombre de variables de l’API et métriques dans `kmeans_metrics.json`.

En l’absence de résultats locaux, `api/reference_results.json` fournit les résultats communiqués pour ce projet : 32 593 inscriptions, effectifs 25 612 / 6 981 et scores 0,4569 / 0,9109 / 24 838,61. La réponse contient `source: "reference_results"` et l’interface signale explicitement cette provenance. Ce fichier n’est pas un résultat recalculé. Les artefacts invalides retournent une erreur 503 au lieu de masquer le problème. Les métriques locales manquantes restent indisponibles, sans mélange silencieux avec les scores de référence.

L’API lit les fichiers à chaque requête. Dans Docker, les résultats présents sont copiés lors du build API : reconstruire l’image API pour inclure de nouveaux résultats. Aucun `dvc pull` n’est imposé par le dashboard.

## Docker / Komodo

Depuis la racine :

```powershell
docker compose config
docker compose build dashboard
docker compose up -d --build api dashboard
```

Dashboard : **http://localhost:8080**. Le service MLflow existant est une dépendance de l’API. Pour contrôler l’ensemble : `docker compose up -d --build`.

L’image du dashboard utilise Node 24 pour `npm ci` et `npm run build`, puis Nginx pour servir `/usr/share/nginx/html`. Un contrôle `/healthz` est inclus. Les services API et MLflow, leurs ports et leurs commandes sont conservés.

Dans Komodo :

1. Utiliser le dépôt avec ces changements et le `docker-compose.yml` racine.
2. Renseigner `VITE_API_URL`, `VITE_MLFLOW_URL`, `DASHBOARD_PORT` et `CORS_ORIGINS` dans les variables de la stack ; utiliser les URL accessibles au navigateur.
3. Conserver **Pre Build Images**. Ne jamais mettre `--build` dans **Build Extra Args**.
4. Reconstruire les images API et dashboard puis redéployer. Les modèles suivis par Git et le scaler déjà utilisé par l’API restent nécessaires à son image.
5. Vérifier la page Dashboard et une prédiction. Aucun paramètre réseau externe ou Komodo n’est modifié par cette intégration.

## Vérifications

```powershell
# Dans dashboard/
npm test
npm run build
npm run preview

# À la racine, environnement API activé
python -m unittest discover -s tests -p test_dashboard_api.py -v
docker compose config
git status
git diff
git ls-files models/
git ls-files projet-v1/
git check-ignore -v projet-v1/README.md
```

Les tests frontend vérifient aussi que les 34 clés correspondent exactement à `api/main.py`. Les tests backend utilisent les véritables modèles locaux et comparent la prédiction à la chaîne de traitement existante. Ils ne réentraînent ni ne modifient aucun artefact.

La règle `projet-v1/` est ajoutée. L’environnement refuse cependant la modification de l’index Git malgré les autorisations : les 54 fichiers déjà suivis doivent encore être retirés du suivi avec `git rm -r --cached -- projet-v1/`, depuis votre terminal à la racine du dépôt. Cette commande conserve les fichiers sur le disque. Les deux fichiers modèles restent suivis. L’intégration ne remplace aucune étape DVC, DLT, DuckDB, dbt, Dagster ou MLflow.
