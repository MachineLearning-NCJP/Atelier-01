# Atelier 1 & 2 — version V2 (travail_v2)

Ce dossier contient une version adaptée aux données de véhicules et de CO2 du catalogue nettoyé.

## Contenu

- `01_eda_vehicules.ipynb` : exploration des données, qualité, distributions, corrélations et synthèse des risques métier.
- `02_supervise_co2.ipynb` : problème de régression supervisée sur `co2_mixte`, avec groupe-split familial, comparaisons de modèles, métriques et interprétation.
- `03_non_supervise_vehicules.ipynb` : segmentation non supervisée avec standardisation, courbe du coude, silhouette, clusters et profilage métier.

## Relancer dans le bon environnement

En shell `fish` depuis la racine du repo :

```fish
cd /opt/MachineLearning/Atelier-01
source travail_v2/.venv/bin/activate.fish
jupyter nbconvert --to notebook --execute --inplace travail_v2/01_eda_vehicules.ipynb
jupyter nbconvert --to notebook --execute --inplace travail_v2/02_supervise_co2.ipynb
jupyter nbconvert --to notebook --execute --inplace travail_v2/03_non_supervise_vehicules.ipynb
```

## Choix clés

- Chargement depuis `../donnees_nettoyees/vehicules_analyse_conso_co2.csv` en respectant le chemin relatif demandé.
- Nettoyage de colonnes via `str.strip().str.lower()` pour éliminer les espaces parasites.
- Utilisation de `GroupShuffleSplit` sur la famille `lib_mrq_doss + lib_mod_doss` pour éviter les fuites entre variantes quasi identiques.
- Variables explicatives restreintes à `puiss_admin`, `puiss_max`, `masse_ordma_min`, `energ`, `hybride`, `typ_boite_nb_rapp`.
- Exclusion explicite de `conso_mixte`, `cnit` et des variables de polluants similaires.
- Modèles supervisés comparés à la baseline `DummyRegressor(strategy='mean')`.
- Standardisation obligatoire pour le clustering non supervisé.

## Limites et points ouverts

- Les données sont un catalogue de 2015 ; elles ne reflètent ni le parc actuel ni les véhicules plus récents.
- Les familles et variantes sont quasi dupliquées, ce qui a un effet sur la stabilité des clusters et les splits.
- La cible `co2_mixte` dépend fortement de la motorisation et des configurations, donc les différences de famille peuvent masquer des effets plus fins.
- Le notebook reste volontairement orienté pédagogiquement : pas de sur-optimisation ni de prédictions de production.
