# Notebooks de l’évaluation finale

Le [README principal](../README.md) contient les attendus, la checklist, le protocole et les commandes de reproduction. Ce dossier constitue le parcours principal de l’étude véhicules et CO₂ :

1. [Exploration des données](01_eda_vehicules.ipynb).
2. [Prédiction supervisée](02_supervise_co2.ipynb).
3. [Segmentation K-means](03_non_supervise_vehicules.ipynb).

Le [nettoyage depuis le CSV brut](../Datascience_et_ML_Atelier01_nettoyage.ipynb) se lance depuis la racine. Les trois notebooks ci-dessus se lancent dans ce dossier et lisent `../donnees_nettoyees/vehicules_analyse_conso_co2.csv`.

`resultats/` contient les mesures exportées pour la présentation : ces sorties se régénèrent en exécutant les notebooks dans l’ordre. Les dépendances sont dans [requirements.txt](requirements.txt). Les environnements locaux et caches sont exclus de Git.
