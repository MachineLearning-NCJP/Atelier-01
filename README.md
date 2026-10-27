# Évaluation finale — véhicules et émissions de CO₂

Étudier un catalogue automobile de mars 2015 pour comprendre les données, prédire les émissions déclarées et segmenter les véhicules selon leurs caractéristiques techniques. Les observations sont des **variantes de catalogue**, pas des ventes, des trajets ou un échantillon représentatif du parc actuel.

## Livrables à consulter

| Ordre | Fichier | Contenu |
|---|---|---|
| 0 | [Nettoyage](Datascience_et_ML_Atelier01_nettoyage.ipynb) | Prétraitements depuis le CSV brut, absences et exports contrôlés |
| 1 | [Exploration](travail_v2/01_eda_vehicules.ipynb) | Qualité, distributions, familles dominantes, corrélations et questions |
| 2 | [Supervisé](travail_v2/02_supervise_co2.ipynb) | Définition de X/y, modèles, validation et test familial, erreurs et généralisation |
| 3 | [Non supervisé](travail_v2/03_non_supervise_vehicules.ipynb) | Variables, standardisation, K-means, coude, silhouette, profils et stabilité |
| 4 | [Présentation PowerPoint](presentation/output/evaluation_ds_ml_vehicules.pptx) et [guide oral](presentation/guide_oral.md) | 23 diapositives visuelles, 30 minutes et notes orateur |

L’[étude complémentaire à deux entrées](Datascience_et_ML_Prediction_CO2.ipynb) et ses [résultats](prediction_co2/CAS_USAGE.md) sont conservés pour documenter un cas de fiche incomplète et ses difficultés de généralisation. Son protocole et ses scores diffèrent de ceux du notebook supervisé principal ; ne pas les mélanger.

Les anciens exercices sur les bâtiments ont été retirés. Aucun historique Git ni travail local préexistant n’a été réinitialisé.

## Données, thème et questions

Source locale : [catalogue brut](fic_etiq_edition_40-mars-2015.csv), rattaché au [catalogue ADEME/UTAC des véhicules commercialisés en France](https://www.data.gouv.fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france). Le fichier fourni est la référence des calculs ; aucun catalogue récent ne lui est substitué.

- **20 880 lignes brutes, 26 colonnes** ; aucun doublon exact ni anomalie physique n’a été retiré par le nettoyage.
- **56 lignes de code énergie `EL`** présentent des mesures manquantes et sont exclues du sous-ensemble analytique, sans leur inventer une cible.
- **20 824 lignes, 12 colonnes** dans [le sous-ensemble d’analyse](donnees_nettoyees/vehicules_analyse_conso_co2.csv).
- **444 familles** selon marque/modèle commercial ; les dix plus fréquentes regroupent **63,12 %** des variantes.
- `co2_mixte` est exprimé en **g/km**, `masse_ordma_min` en **kg** et `puiss_max` en **kW**. Les émissions sont déclarées selon les conventions du catalogue, sans mesure des conditions réelles d’usage.

Questions étudiées : quels profils techniques dominent le catalogue ? Peut-on estimer le CO₂ sur des familles absentes de l’apprentissage ? Quels profils de masse, puissance et émissions K-means distingue-t-il ? Ces groupes restent-ils cohérents quand les familles très représentées pèsent moins ? Quelles décisions ces résultats peuvent-ils raisonnablement éclairer ?

## Protocole et précautions

Le parcours principal utilise une régression de `co2_mixte` et une segmentation descriptive. Pour la prédiction, les familles sont séparées avant la sélection des modèles : validation interne sur l’apprentissage, puis évaluation finale sur le test réservé. Les transformations sont apprises dans des pipelines, uniquement sur les observations d’entraînement de chaque pli. Le protocole corrigé réserve le test pour cette exécution, mais les données ont déjà été explorées dans les versions antérieures : il ne s’agit pas d’une validation prospective sur des données restées totalement inconnues. Une confirmation externe demanderait de nouvelles familles ou un nouveau catalogue.

`conso_mixte` est exclue des entrées prédictives : c’est une mesure d’homologation quasi redondante avec le CO₂, indisponible dans le scénario d’estimation retenu. **Une forte corrélation ne constitue pas à elle seule une fuite d’information.** La [puissance fiscale a historiquement incorporé le CO₂](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000006320193/1998-07-03) ; elle est écartée du modèle principal et examinée à titre de comparaison. Un coefficient ou une importance ne prouve aucun effet causal.

En clustering, `puiss_max`, `masse_ordma_min` et `co2_mixte` sont des variables descriptives standardisées. Le CO₂ n’y est **pas une cible à prédire**. Coude, silhouette et interprétabilité guident le choix de K. L’ACP facilite la lecture graphique ; elle ne prouve pas l’existence de catégories naturelles. Le plafonnement familial constitue un contrôle de sensibilité et non une correction automatique du catalogue.

## Résultats vérifiés

Les [exports des notebooks](travail_v2/resultats/) servent de source aux graphiques de la soutenance. Les scores ci-dessous concernent le **parcours principal**, sans puissance fiscale.

| Régression | MAE (g/km) | RMSE (g/km) | R² |
|---|---:|---:|---:|
| KNN 7 voisins — entraînement | 4,05 | 6,88 | 0,975 |
| KNN 7 voisins — test familial | 16,78 | 23,99 | 0,629 |
| Moyenne constante — même test | 41,68 | 49,53 | −0,582 |

La sélection est faite sur cinq plis groupés dans les **16 004 lignes / 355 familles d’entraînement**. Le test contient **4 820 lignes / 89 autres familles**. La MAE de validation du KNN est de **12,34 ± 2,44 g/km** (moyenne et écart-type des cinq plis). L’écart avec la régression linéaire (12,39) et la forêt (12,44) est très faible au regard de cette dispersion : ne pas présenter un vainqueur universel. L’erreur de test supérieure à celle de validation montre les limites de généralisation ; le faible score d’entraînement ne décrit pas la performance sur une nouvelle famille.

Pour la segmentation, **K = 3**, silhouette **0,470 sur 5 000 points** ; les deux axes de l’ACP restituent **93,29 %** de la variance standardisée. Les groupes sont ordonnés par CO₂ moyen, et leurs numéros sont des étiquettes sans ordre naturel.

| Profil descriptif | Variantes | Puissance moyenne (kW) | Masse moyenne (kg) | CO₂ moyen (g/km) |
|---|---:|---:|---:|---:|
| 0 — moins émetteurs dans ce catalogue | 11 060 | 115,69 | 1 541 | 123,88 |
| 1 — plus lourds | 7 963 | 139,19 | 2 147 | 176,87 |
| 2 — plus puissants et émetteurs | 1 801 | 363,24 | 1 977 | 244,59 |

L’accord entre partitions (ARI, corrigé du hasard) est proche de 1 selon les initialisations, mais tombe à **0,548** après plafonnement à 50 variantes par famille. Les groupes sont donc reproductibles pour un catalogue fixé, tout en restant sensibles à sa composition. Ce sont des profils descriptifs ; ils ne démontrent ni trois catégories naturelles ni un bénéfice causal d’un changement de véhicule.

## Checklist des attendus

Référence principale : [sujet final fourni](SUJET/Sujet_Evaluation_Finale_Data_Science_ML.pdf), 3 pages. Ce document est analysé comme sujet du devoir. L’[ancienne consigne](SUJET/EVAL-CONSIGNES.pdf) reste une référence complémentaire pour les contrôles supervisés ; son ancien format 10–12 minutes / 5–8 slides ne s’applique pas à cette demande. **Le minutage 4 / 5 / 16 / 5 et le parti pris visuel viennent de l’utilisateur**, pas du sujet final. Celui-ci ne contient pas de barème chiffré ni de nombre de slides imposé.

Les cases attestent une présence vérifiée dans les fichiers, pas une garantie de note. Les cases ouvertes demandent une action humaine ou une vérification encore à terminer.

### 1. Données et enjeux — 4 minutes · sujet p. 1

- [x] Présenter le thème environnemental, l’origine, l’unité d’observation et la structure des données.
- [x] Expliquer les valeurs manquantes, doublons, valeurs atypiques et traitements retenus.
- [x] Préserver le nettoyage reproductible depuis les données brutes.
- [x] Illustrer les enseignements de l’EDA avec des graphiques adaptés.
- [x] Poser les questions étudiables et distinguer catalogue, parc réel et émissions d’usage.

### 2. Problématique supervisée — 5 minutes · sujet p. 1

- [x] Définir le besoin d’estimation, la cible y et les variables X disponibles au moment de prédire.
- [x] Comparer une baseline et au moins deux modèles avec MAE, RMSE et R².
- [x] Réserver le test par famille avant la sélection ; limiter la validation croisée à l’entraînement.
- [x] Comparer performances d’entraînement et de test ; expliquer erreurs et généralisation.
- [x] Interpréter l’utilité et les limites, sans causalité ni promesse de déploiement.

### 3. K-means et segmentation — 16 minutes · sujet p. 2–3

- [x] Définir les observations à regrouper et l’objectif environnemental de segmentation.
- [x] Justifier les variables retenues et écartées ; éviter les dimensions redondantes.
- [x] Expliquer la standardisation et son rôle dans la distance euclidienne.
- [x] Définir brièvement K-means : « groupes par proximité » ; appliquer plusieurs valeurs de K.
- [x] Présenter **la courbe du coude ET le score de silhouette**.
- [x] Justifier K avec ces deux diagnostics et la lisibilité des profils.
- [x] Donner effectifs, moyennes en unités réelles et caractéristiques distinctives de chaque cluster.
- [x] Visualiser les groupes et expliquer le rôle et les limites de l’ACP, si utilisée.
- [x] Relier les profils à une interprétation métier et une utilité environnementale prudente.
- [x] Examiner la stabilité et la sensibilité à la composition familiale, sans comparer naïvement les numéros de clusters.

DBSCAN et classification hiérarchique sont **facultatifs** dans le sujet p. 3. Leur absence ne bloque pas la checklist obligatoire.

### 4. Recul et conclusion — 5 minutes · sujet p. 3

- [x] Résumer les enseignements du non supervisé et son complément au supervisé.
- [x] Discuter « groupes distincts ou découpage d’un continuum ? ».
- [x] Exposer les limites du catalogue ancien, de la pondération des variantes, des variables et de K-means.
- [x] Proposer des améliorations concrètes : nouvelles variables, données récentes, contrôles et méthodes adaptées.
- [x] Distinguer ce que les résultats permettent de conclure des décisions non validées.

### Livraison et soutenance · sujet p. 3 et demande utilisateur

- [x] Notebooks propres, commentés, exécutés sans erreur et avec interprétations rédigées.
- [x] Résultats de la présentation traçables vers les sorties des notebooks.
- [x] Présentation visuelle : graphiques, comparaisons, quelques mots par notion et peu de texte.
- [x] Notes orateur et minutage **4 + 5 + 16 + 5 = 30 minutes**.
- [x] Vérifier le rendu de chaque slide et l’absence de chiffres périmés.
- [ ] Renseigner les noms des membres du groupe si nécessaire et organiser la prise de parole.
- [ ] Répéter l’oral en groupe et vérifier le temps réel ainsi que le matériel de projection.

## Reproduire l’étude

Python **3.12** est recommandé. Depuis la racine, dans un terminal zsh/bash :

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r travail_v2/requirements.txt
python -m ipykernel install --user --name atelier-ml --display-name "Atelier ML"
```

Le nettoyage est conservé et peut être relancé pour régénérer les CSV. Il réécrit uniquement les quatre exports du dossier `donnees_nettoyees/`, jamais le brut :

```bash
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=atelier-ml --ExecutePreprocessor.timeout=1800 Datascience_et_ML_Atelier01_nettoyage.ipynb
```

Exécuter ensuite les trois notebooks dans l’ordre avec le [script portable](travail_v2/executer_notebooks.py). Il utilise le Python de l’environnement actif et le bon répertoire de travail, sans dépendre du kernel enregistré dans les notebooks :

```bash
python travail_v2/executer_notebooks.py
```

Pour une reprise ciblée : `python travail_v2/executer_notebooks.py 03_non_supervise_vehicules.ipynb`. Les fichiers sont réexécutés sur place, avec vérification de l’absence d’erreurs.

Les sorties destinées au support sont regroupées dans `travail_v2/resultats/`. Les graines et paramètres figurent dans le code. De faibles écarts numériques entre systèmes restent possibles. Une exécution reproductible n’établit pas que les données représentent le parc actuel ni que les modèles sont validés en production.
