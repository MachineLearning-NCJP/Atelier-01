# Atelier 1 & 2 — version V2 (travail_v2)

Ce dossier contient les notebooks adaptés aux données de véhicules et de CO2 du catalogue nettoyé.

## Contenu

- `01_eda_vehicules.ipynb` : exploration des données, distributions, corrélations, concentration par famille et risques métier.
- `02_supervise_co2.ipynb` : régression supervisée sur `co2_mixte`, avec validation groupée répétée, ablation des variables, importance des variables et diagnostics de robustesse.
- `03_non_supervise_vehicules.ipynb` : segmentation non supervisée avec standardisation, choix de K, profils de clusters et sensibilité aux quasi-doublons.

## Relancer dans le bon environnement

En shell `fish` depuis la racine du repo :

```fish
cd (git rev-parse --show-toplevel)
source travail_v2/.venv/bin/activate.fish
jupyter nbconvert --to notebook --execute --inplace travail_v2/01_eda_vehicules.ipynb
jupyter nbconvert --to notebook --execute --inplace travail_v2/02_supervise_co2.ipynb
jupyter nbconvert --to notebook --execute --inplace travail_v2/03_non_supervise_vehicules.ipynb
```

## Choix clés

- Chargement depuis `../donnees_nettoyees/vehicules_analyse_conso_co2.csv` en respectant le chemin relatif demandé.
- Nettoyage des colonnes via `str.strip().str.lower()` pour éliminer les espaces parasites.
- Diagnostic des familles pour éviter les fuites entre variantes quasi identiques.
- Validation principale de `02` via `GroupShuffleSplit(n_splits=20, test_size=0.2, random_state=42)`.
- Plafonnement à 50 variantes par famille pour tester la sensibilité aux familles dominantes.
- Ablation des variables pour mesurer l’apport de `puiss_admin`, `masse_ordma_min`, `energ` et `hybride`.
- Standardisation obligatoire pour le clustering non supervisé.

## À RÉDIGER restants

- Notebook 1 : questions sur la concentration par famille, la qualité du dataset et les effets sur le train/test.
- Notebook 2 : questions sur la composition du split, la robustesse des modèles, l’ablation des variables et la synthèse métier.
- Notebook 3 : questions sur le K retenu, la stabilité des clusters et la valeur ajoutée du non supervisé.

## Limites et points ouverts

- Les données sont un catalogue de 2015 ; elles ne reflètent ni le parc actuel ni les véhicules plus récents.
- Les familles et variantes sont inégalement réparties, ce qui influence la stabilité des modèles et des clusters.
- `co2_mixte` dépend fortement de la motorisation et de la configuration, donc la structure familiale doit rester au centre de l’interprétation.
- Les notebooks restent pédagogiques et ne prétendent pas à une conclusion définitive de production.
