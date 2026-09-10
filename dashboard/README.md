# EduCluster — Dashboard local

Depuis la racine de Mlops-Project :

```powershell
python dashboard/server.py
```

Ouvrir http://127.0.0.1:8050. Arrêt : Ctrl+C. Un autre port peut être choisi avec `--port 8051`.

Python 3.10 ou supérieur, aucune dépendance supplémentaire. Le serveur écoute uniquement sur l’interface locale. Les fichiers sont lus à chaque actualisation, sans modification, sans chargement des modèles joblib et sans accès à projet-v1.

## Données

Le dashboard lit les sorties définies dans dvc.yaml : clustered_students.csv, kmeans_metrics.json et les autres artefacts de data/processed. Il présente les effectifs par inscription (un étudiant peut être inscrit à plusieurs modules), les résultats académiques par segment, les métriques globales et la comparaison des algorithmes si disponible. Les filtres module/session s’appliquent aux inscriptions, pas aux métriques globales. Les identifiants numériques des segments sont conservés : leur sens doit être validé après chaque entraînement.

Les fichiers manquants ne sont jamais remplacés par des données fictives. Les métriques constantes du code Dagster ne sont pas utilisées comme résultats observés. La présence d’un artefact n’atteste pas d’une exécution réussie. Les liens API et MLflow reprennent les ports du docker-compose du projet, sans prétendre que ces services fonctionnent.

Si les données sont absentes, restaurer les sorties depuis le stockage DVC configuré, ou exécuter le pipeline existant après avoir obtenu les données OULAD et configuré l’environnement. Le dashboard ne déclenche aucun entraînement ni aucune ingestion.
