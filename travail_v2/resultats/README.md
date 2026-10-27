# Résultats utilisés dans la soutenance

Ces fichiers sont régénérés par les trois notebooks du dossier parent. Ils constituent les données sources des graphiques et des chiffres du support, pas une nouvelle source externe. Les CSV utilisent la virgule comme séparateur.

| Préfixe / fichier | Origine et usage |
|---|---|
| `eda_resume.json`, `energies.csv`, `familles.csv`, `correlations.csv`, `statistiques_descriptives.csv` | Notebook 01 : qualité, composition, concentration et associations |
| `donnees_graphiques.csv` | Notebook 01 : observations sélectionnées pour les graphiques |
| `supervise_validation*.csv` | Notebook 02 : comparaison des modèles sur cinq plis groupés dans l’entraînement |
| `supervise_partitions.csv`, `supervise_repartition.csv` | Notebook 02 : attribution des lignes et contrôle des familles disjointes |
| `supervise_train.csv`, `supervise_test.csv`, `supervise_predictions_test.csv`, `supervise_resume.json` | Notebook 02 : résultats du modèle retenu et de la baseline ; prédictions permettant de recalculer les métriques |
| `supervise_ablation.csv`, `supervise_plafonnement.csv` | Notebook 02 : diagnostics sur l’entraînement ; ne constituent pas de nouveaux tests indépendants |
| `supervise_erreurs_*.csv`, `supervise_importances.csv` | Notebook 02 : diagnostics du test déjà évalué, dont importance par permutation après l’évaluation ; aucune resélection du modèle |
| `clustering_choix_k.csv`, `clustering_resume.json` | Notebook 03 : inertie, silhouette sur 5 000 points et choix de K |
| `clustering_profils*.csv`, `clustering_centres_z.csv`, `clustering_energies_pct.csv`, `clustering_hybrides_pct.csv` | Notebook 03 : effectifs et profils en unités réelles ou standardisées |
| `clustering_points.csv`, `clustering_silhouettes_points.csv`, `clustering_acp*.csv`, `clustering_standardisation.csv` | Notebook 03 : visualisations et données des transformations |
| `clustering_stabilite.csv` | Notebook 03 : ARI pour initialisations, rééchantillonnages, plafonnement familial et retrait du CO₂ |

Les clusters principaux sont renumérotés par CO₂ moyen croissant. Les labels d’autres ajustements ne s’alignent pas automatiquement : l’ARI compare les partitions sans dépendre des numéros. Le nombre de variantes n’est pas une pondération par les ventes.

Les résultats du dossier racine `prediction_co2/` appartiennent à l’étude complémentaire à deux entrées et ne doivent pas être confondus avec ces exports.
