# Déploiement automatique EduCluster

Stack existante : `analyse_des_parcours_d_apprentissage`.

## Fonctionnement

Push sur main → tests API avec les artefacts suivis → tests/build React → build des trois images Docker → webhook signé → Komodo déploie la stack existante avec Pre Build Images.

Les trois vérifications CI fonctionnent en parallèle. Toutes doivent réussir avant l’envoi. Les pull requests et les exécutions manuelles lancent les vérifications uniquement. Aucun déploiement depuis une pull request. Le modèle et le scaler ne sont pas réentraînés, aucun DVC pull n’est imposé.

## Activation unique dans Komodo

Ouvrir la stack, puis Config :

1. Vérifier le dépôt `Bahriilhame/Mlops-Project`, la branche `main` et le fichier `docker-compose.yml`. Ne pas fixer le champ Commit à une ancienne révision.
2. Garder les variables frontend/API, les volumes, les services et Pre Build Images existants. Ne pas mettre `--build` dans Build Extra Args.
3. Dans Webhooks, activer les webhooks et choisir le type GitHub.
4. Activer Force Deploy (`webhook_force_deploy`) pour redéployer aussi lorsque seul le code applicatif change.
5. Définir un secret de webhook propre à cette stack, si cette option est disponible. Sinon, utiliser le secret de webhook configuré par l’administrateur Komodo. Ne pas utiliser une clé Periphery : elle a un autre rôle.
6. Copier l’URL du webhook Deploy de la stack. Le format attendu pour cette stack est `https://komodo.s3.fsbm.ma/listener/github/stack/6a9ff2553ddb0f28747a3daa/deploy` ; l’URL affichée dans votre instance reste la référence.

## Activation unique dans GitHub

Dans le dépôt → Settings → Secrets and variables → Actions → New repository secret :

| Secret | Valeur |
| --- | --- |
| KOMODO_WEBHOOK_URL | URL HTTPS Deploy copiée dans Komodo |
| KOMODO_WEBHOOK_SECRET | Exactement le secret configuré dans Komodo |

Ne pas envoyer ces secrets dans le chat et ne pas les écrire dans Git. Activer GitHub Actions si nécessaire.

Ne pas ajouter en plus un webhook GitHub direct « push → deploy » : il déclencherait le déploiement avant les résultats CI. Si un tel webhook existe, le désactiver pour que seul le job deploy déclenche cette stack. Vérifier aussi qu’aucun autre automatisme Komodo ne déploie indépendamment chaque push.

Puis publier les quatre nouveaux fichiers :

```powershell
cd C:\Users\ISRAA\Mlops-Project
git add .github/workflows/ci-cd.yml scripts/trigger_komodo.py tests/test_komodo_webhook.py docs/CI_CD_KOMODO.md
git commit -m "ci: validate EduCluster and trigger Komodo deployment"
git push origin main
```

## Vérifier la première exécution

Dans GitHub → Actions → EduCluster CI / Komodo CD, vérifier les trois jobs CI puis Trigger existing Komodo stack. Dans Komodo → Updates, vérifier la réussite de Deploy Stack, les trois services et la révision déployée. Une réponse HTTP positive au webhook confirme sa réception, pas la réussite finale de la construction ou du déploiement. Les alertes Komodo existantes restent utiles.

## Limites et reprises

- Les exécutions sur une même branche sont sérialisées ; un commit déjà dépassé au moment du déclenchement est ignoré.
- Komodo suit main et résout lui-même la révision au déploiement. Ce mécanisme ne verrouille pas atomiquement le SHA validé : un push survenant après la vérification peut avancer main. Pour une garantie stricte, utiliser une branche de livraison dédiée ou des images immuables et une procédure dédiée. Ce workflow conserve votre stack main existante.
- Le webhook n’est pas réessayé automatiquement en cas de délai dépassé, car le déploiement a peut-être déjà démarré. Consulter Updates avant toute relance.
- Si le secret manque ou est incorrect, le job deploy échoue sans exposer sa valeur.
- Les variables VITE_* de production restent configurées dans Komodo. Les images CI servent à vérifier la construction et ne sont pas publiées dans un registre.
- Ne pas lancer d’entraînement ni modifier les paramètres serveur pour configurer ce mécanisme.

## Références

- https://komo.do/docs/automate/webhooks
- https://github.com/moghtech/komodo/blob/main/client/core/rs/src/entities/stack.rs (webhook_enabled, webhook_secret, webhook_force_deploy)
