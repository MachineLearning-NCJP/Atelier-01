# Atelier Data Science et Machine Learning

## Cas choisi

Ce projet étudie un catalogue de véhicules et leurs émissions de CO2. Le cas choisi est l'analyse de caractéristiques techniques de véhicules afin de :

- comprendre la structure et la qualité des données ;
- prédire les émissions de CO2 d'un véhicule ;
- identifier des profils de véhicules similaires sans utiliser de cible ;
- mesurer l'influence des familles de véhicules sur la validation et l'interprétation.

Le sujet est traité à partir du fichier nettoyé `donnees_nettoyees/vehicules_analyse_conso_co2.csv`. Les données correspondent à un catalogue automobile de 2015 et ne représentent pas nécessairement le parc automobile actuel.

## Cas d'usage

Un constructeur, un organisme d'homologation ou un analyste de catalogue pourrait utiliser cette démarche pour :

- repérer les véhicules présentant des profils techniques et d'émissions proches ;
- estimer le niveau de CO2 à partir d'informations disponibles lors de la description d'un véhicule ;
- détecter les familles ou motorisations pour lesquelles les prédictions sont moins fiables ;
- éviter de tirer des conclusions trop optimistes lorsque certaines familles sont surreprésentées.

Le modèle n'est pas présenté comme un outil réglementaire ou comme une preuve de causalité. Il s'agit d'une étude pédagogique reproductible, destinée à comparer des méthodes et à discuter leurs limites.

## Données étudiées

Le dataset contient 20 824 lignes et 12 colonnes après nettoyage. Les principales variables sont :

- `co2_mixte` : émissions de CO2 en g/km, utilisée comme cible dans la régression ;
- `conso_mixte` : consommation mixte, examinée mais exclue des variables prédictives pour éviter une fuite d'information ;
- `puiss_admin`, `puiss_max` : indicateurs de puissance ;
- `masse_ordma_min`, `masse_ordma_max` : masses minimales et maximales ;
- `energ`, `hybride`, `typ_boite_nb_rapp` : variables décrivant l'énergie, l'hybridation et la transmission ;
- `cnit` : identifiant technique, exclu des variables prédictives ;
- `lib_mrq_doss` et `lib_mod_doss` : utilisées pour construire une famille de véhicules.

Le catalogue comporte 444 familles. Les 10 familles les plus fréquentes représentent 63,12 % des lignes, ce qui constitue un risque important de biais si les variantes proches sont réparties aléatoirement entre apprentissage et test.

## Questions étudiées

1. Quelle est la qualité du dataset et comment est-il structuré ?
2. Peut-on prédire `co2_mixte` à partir des caractéristiques techniques sans utiliser `conso_mixte` ?
3. Les performances restent-elles cohérentes lorsque la validation sépare les familles de véhicules ?
4. Quels groupes de véhicules apparaissent avec une méthode de clustering ?
5. Les résultats changent-ils lorsque l'influence des familles très représentées est plafonnée ?

## Organisation des notebooks

### `travail_v2/01_eda_vehicules.ipynb`

Exploration des données : dimensions, types, valeurs manquantes, distributions, familles dominantes, doublons et corrélations. Cette étape justifie les choix de variables et la validation par famille.

### `travail_v2/02_supervise_co2.ipynb`

Régression supervisée de `co2_mixte` avec :

- une baseline par moyenne ;
- une régression linéaire ;
- un arbre de décision ;
- un Random Forest ;
- un KNN ;
- une validation groupée répétée par famille ;
- une comparaison avec un jeu plafonné à 50 variantes par famille ;
- une ablation des variables et une analyse des erreurs.

Sur le jeu complet, la régression linéaire obtient le meilleur R² moyen parmi les modèles comparés : `0,8499`, avec un MAE moyen de `11,28 g/km`. Sur le jeu plafonné, le Random Forest atteint un R² moyen de `0,8819`. Cette différence montre que le classement dépend de la composition du catalogue et doit être interprété avec prudence.

### `travail_v2/03_non_supervise_vehicules.ipynb`

Segmentation des véhicules avec KMeans après standardisation de la puissance, de la masse et du CO2. Le choix de `K=3` est fondé sur le meilleur score de silhouette observé (`0,4726`) et sur l'interprétabilité des profils. Une ACP permet ensuite de visualiser la structure en deux dimensions.

## Choix méthodologiques importants

- `random_state=42` est utilisé pour rendre les résultats reproductibles.
- Les familles sont construites avec `lib_mrq_doss` et `lib_mod_doss`.
- La validation groupée empêche une même famille d'apparaître à la fois dans l'entraînement et dans le test.
- `conso_mixte` est exclue de la prédiction du CO2 car elle est très fortement corrélée à `co2_mixte` et pourrait rendre l'évaluation artificiellement favorable.
- Les transformations sont placées dans des pipelines afin d'éviter les fuites entre les partitions.
- Le plafonnement à 50 lignes par famille sert d'analyse de sensibilité, pas de remplacement automatique du dataset original.
- Les résultats de clustering sont descriptifs et ne constituent pas des catégories métier officielles.

## Limites

- Le dataset est un catalogue de 2015 ; les résultats ne sont pas généralisables automatiquement aux véhicules récents.
- Les familles sont très déséquilibrées et certaines variantes peuvent être proches ou dupliquées.
- La forte corrélation entre `puiss_admin` et `puiss_max` rend l'interprétation des coefficients délicate.
- Les performances peuvent varier selon la population ciblée : catalogue complet, familles plafonnées ou usage réel.
- Les importances de variables mesurent une dépendance prédictive et ne prouvent pas un effet causal.
- KMeans est sensible à l'échelle des variables, aux valeurs extrêmes et au choix de `K`.

## Reproduire l'étude

Depuis la racine du dépôt, avec le shell `fish` :

```fish
source travail_v2/.venv/bin/activate.fish
jupyter nbconvert --to notebook --execute --inplace travail_v2/01_eda_vehicules.ipynb
jupyter nbconvert --to notebook --execute --inplace travail_v2/02_supervise_co2.ipynb
jupyter nbconvert --to notebook --execute --inplace travail_v2/03_non_supervise_vehicules.ipynb
```

Les dépendances utilisées sont listées dans `travail_v2/requirements.txt`. Les notebooks lisent les données existantes et ne réécrivent pas le fichier source.
