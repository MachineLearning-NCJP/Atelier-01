# Guide oral — Véhicules et émissions de CO₂

Support : [présentation modifiable](output/evaluation_ds_ml_vehicules.pptx).

Durée cible : **30 minutes**, selon la demande utilisateur. Le sujet PDF ne fixe pas de durée. Les notes ci-dessous développent les slides volontairement peu textuelles. Les graphiques sont éditables.

| Partie | Slides | Intervalle | Durée |
| --- | --- | --- | --- |
| Données, thème, questions | 1–4 | 00:00–04:00 | 4 min |
| Prédiction supervisée | 5–8 | 04:00–09:00 | 5 min |
| Segmentation K-Means | 9–20 | 09:00–25:00 | 16 min |
| Recul et conclusion | 21–23 | 25:00–30:00 | 5 min |

Les nuages de clusters affichent 220 points par groupe pour rendre le petit cluster visible : les proportions affichées ne décrivent donc pas leur densité réelle. Les statistiques et profils utilisent toutes les observations. Les silhouettes utilisent un échantillon fixe de 5 000 observations.

## Repères de méthode

- K-Means : groupes par proximité.
- Standardisation : centrer et réduire.
- Silhouette : cohésion et séparation.
- ACP : projection synthétique.
- ARI : accord corrigé du hasard.
- MAE : écart absolu moyen.
- RMSE : pénalise les grandes erreurs.

## Déroulé minuté

### 01. Véhicules et émissions de CO₂ — 00:00 à 00:30

Nous étudions un catalogue français de véhicules commercialisés, édition mars 2015. La question environnementale porte sur le CO2 déclaré en g/km et les profils techniques associés. Nous allons présenter les données, résumer la prédiction supervisée puis consacrer l'essentiel du temps à la segmentation. Il s'agit de valeurs d'homologation historiques. Elles ne mesurent ni un parc roulant ni les émissions réelles ni le cycle de vie.

Source : fic_etiq_edition_40-mars-2015.csv, catalogue ADEME fourni dans le projet.

### 02. Le catalogue et son périmètre — 00:30 à 01:45

Une ligne représente une variante de véhicule, pas une vente et pas un véhicule en circulation. Le fichier brut contient 20 880 lignes et 26 colonnes. Le nettoyage ne retire ici ni doublon exact ni anomalie physique selon les règles retenues. Le jeu d'analyse garde 20 824 lignes complètes et 12 variables. Les 56 lignes exclues concernent EL, faute de consommation et CO2 renseignés : leur absence ne signifie pas CO2 nul. Les 444 familles réunissent marque et modèle. Le nettoyage normalise les textes, contrôle les absences, valeurs négatives et masses inversées. Les valeurs extrêmes plausibles restent dans l'étude.

Sources : notebook nettoyage, donnees_nettoyees/bilan_qualite.csv, donnees_nettoyees/vehicules_analyse_conso_co2.csv.

### 03. Des émissions et des familles très inégales — 01:45 à 03:00

La médiane de CO2 est 147 g/km, avec un intervalle interquartile de 122 à 180 g/km. Le graphique montre une distribution asymétrique. Les dix familles les plus fréquentes concentrent 63,1 % des lignes. Cette concentration peut orienter une moyenne, un modèle ou un clustering vers des variantes nombreuses. Nous séparons les familles pour évaluer la prédiction et plafonnons leur contribution dans une analyse de sensibilité. On observe des relations, pas des causes.

Source : donnees_nettoyees/vehicules_analyse_conso_co2.csv.

### 04. Les questions de l’étude — 03:00 à 04:00

Trois questions guident l'étude. Quelles caractéristiques accompagnent les émissions déclarées ? Peut-on estimer le CO2 d'une autre famille à partir des informations techniques disponibles ? Enfin, quels profils techniques cohérents le clustering permet-il de distinguer ? Nous relions ensuite les résultats à une décision raisonnable : prioriser une investigation ou comparer des variantes à usage comparable. Les groupes ne suffisent pas à recommander un remplacement de véhicule.

Source : problématique du projet et sujet d'évaluation finale, pages 1 à 3.

### 05. Prédire le CO₂ de familles différentes — 04:00 à 05:30

Le problème est une régression : estimer une valeur continue de CO2 en g/km. X contient puissance maximale, masse, énergie, hybridation et transmission. Les identifiants et noms de famille servent au regroupement, pas à la prédiction. Nous retirons consommation et puissance fiscale du modèle principal. La consommation est indisponible dans le scénario visé et très liée aux émissions. La puissance fiscale de cette période intègre historiquement le CO2. La corrélation seule ne prouve pas une fuite : c'est la disponibilité et le mode de construction des données qui motivent le retrait. Le test familial est isolé avant les validations croisées de l'entraînement. Chaque pipeline apprend ses transformations dans le pli d'entraînement.

Sources : travail_v2/02_supervise_co2.ipynb, travail_v2/resultats/supervise_resume.json.

### 06. Comparer les modèles sur l’entraînement — 05:30 à 06:30

La baseline prédit une constante apprise dans l'entraînement. Nous comparons ensuite des modèles de capacité différente sur cinq plis groupés par famille. La MAE moyenne, en g/km, sert à choisir le modèle avant de mesurer le test. Une MAE plus faible est préférable. Les variations entre plis rappellent que les familles diffèrent fortement. Les transformations, l'encodage et l'échelle restent dans le pipeline. Le critère fixé retient KNN 7 voisins, mais ses écarts avec la régression linéaire et la forêt sont inférieurs à 0,10 g/km. Ils sont bien plus petits que la dispersion entre plis : aucune supériorité nette n'est établie.

Source : travail_v2/resultats/supervise_validation.csv.

### 07. La performance sur le test familial — 06:30 à 08:00

Chaque point compare une valeur observée et une prédiction du modèle retenu. Une prédiction parfaite se trouve sur la diagonale. Le modèle KNN 7 voisins obtient MAE 16,78 g/km, RMSE 23,99 g/km et R2 0,629. La MAE résume l'écart absolu moyen. La RMSE pénalise davantage les grosses erreurs. R2 compare les erreurs quadratiques à une moyenne de la cible du test, et peut être négatif. Le test contient 4820 variantes de 89 familles distinctes de l'entraînement. Le graphique ne montre qu'un échantillon reproductible de points pour garder la lisibilité.

Source : travail_v2/resultats/supervise_predictions_test.csv et supervise_test.csv.

### 08. La portée de la généralisation — 08:00 à 09:00

La MAE passe d'environ 4,05 g/km en apprentissage à 12,34 en validation et 16,78 sur le test. La baseline constante obtient 41,68 g/km sur le même test. Le modèle apprend donc un signal utile, avec un optimisme important sur l'entraînement. Comparer validation et test aide à voir l'effet de la population. La validation croisée emploie uniquement l'entraînement. Le score de test dépend d'une séparation familiale fixée, dont certaines variantes avaient déjà été explorées dans les travaux précédents : nous assumons une évaluation rétrospective. Ce résultat ne constitue pas une validation prospective neuve. Le retrait de la puissance fiscale réduit le risque de reconstruire la cible à partir d'une variable qui l'incorpore. Nous limitons la conclusion au catalogue de 2015, avec des familles définies par marque et modèle. Pour décider sur une flotte actuelle, il faudra de nouvelles données et une évaluation indépendante, idéalement temporelle.

Source : travail_v2/02_supervise_co2.ipynb et travail_v2/resultats/supervise_resume.json.

### 09. Segmenter les profils techniques — 09:00 à 10:20

La segmentation regroupe les variantes par proximité dans un espace de caractéristiques. Ici, aucune variable y n'est à prédire. Le CO2 fait partie des variables descriptives, avec la puissance et la masse. Les couleurs montrent déjà la solution finale K=3, que nous allons justifier. Les étiquettes C0, C1, C2 servent à identifier les profils et n'ont pas d'ordre universel. Nous les avons ordonnées par CO2 moyen croissant pour garder la lecture cohérente. Le graphique affiche 220 points tirés dans chacun des clusters pour éviter de masquer le plus petit. Ce sous-échantillon visuel ne respecte donc pas les proportions du catalogue, indiquées séparément. Le calcul du clustering porte sur les 20 824 lignes.

Source : travail_v2/resultats/clustering_points.csv.

### 10. Le choix des variables — 10:20 à 11:40

Nous retenons trois dimensions complémentaires : capacité du moteur, gabarit et émission déclarée. La consommation est très liée au CO2, corrélation proche de 0,976. Inclure les deux donnerait davantage de poids à une information redondante dans la distance. Les identifiants sont exclus. Les catégories énergie et hybride servent à décrire les groupes après leur construction, sans imposer une distance arbitraire entre codes. Les variables retenues restent corrélées : puissance et CO2 environ 0,647, masse et CO2 0,625. Standardiser ne supprime pas cette corrélation. Il s'agit d'un choix d'analyse qui doit être mis à l'épreuve, par exemple en retirant le CO2.

Sources : travail_v2/resultats/correlations.csv et clustering_resume.json.

### 11. L’effet de la standardisation — 11:40 à 13:00

K-Means utilise la distance euclidienne. Sans transformation, un écart de masse de quelques centaines de kg pèserait bien davantage qu'un écart de CO2 de quelques dizaines de g/km. Chaque variable est centrée puis divisée par son écart-type : z=(x-moyenne)/écart-type. Les écarts-types initiaux sont 80,1 kW, 371,7 kg et 44,2 g/km. Après transformation ils valent tous 1, avec une moyenne nulle. Ce traitement équilibre les unités, mais conserve les corrélations et la sensibilité aux valeurs extrêmes. Ici le clustering décrit le catalogue complet : le scaler est ajusté sur ce catalogue.

Source : travail_v2/resultats/clustering_standardisation.csv.

### 12. K-Means : groupes par proximité — 13:00 à 14:20

K-Means minimise la somme des distances euclidiennes au carré entre points et centres de leurs groupes, appelée inertie. Pour un K fixé, l'algorithme choisit des centres initiaux, affecte chaque observation au centre le plus proche, recalcule les centres comme moyennes puis répète jusqu'à stabilisation. Les 20 initialisations n_init=20 limitent le risque d'une mauvaise solution locale. Le graphique est un aperçu sur puissance et masse standardisées, mais le calcul utilise bien trois variables, dont le CO2. Les centroïdes sont des profils moyens et ne désignent pas nécessairement un véhicule existant. L'algorithme produit toujours K groupes, même si les données forment un continuum.

Sources : travail_v2/03_non_supervise_vehicules.ipynb et clustering_centres_z.csv.

### 13. La courbe du coude — 14:20 à 15:40

Nous testons K de 2 à 10 avec les mêmes données standardisées et la même règle d'initialisation. L'inertie diminue mécaniquement lorsque K augmente, car on dispose de davantage de centres. Le coude cherche une zone où le gain marginal ralentit. Ici l'inertie passe de 34 972 à K=2 à 20 108 à K=3, puis baisse encore mais plus progressivement. Le coude n'est pas un test automatique et ne prouve pas le nombre naturel de catégories. Nous le croisons avec la silhouette et la possibilité d'expliquer les profils.

Source : travail_v2/resultats/clustering_choix_k.csv.

### 14. Le score de silhouette — 15:40 à 17:00

La silhouette compare la distance moyenne d'un point à son groupe et celle au groupe voisin le plus proche. Elle varie de -1 à 1. Une valeur proche de 1 indique une bonne cohésion et séparation, une valeur proche de 0 une frontière ambiguë, une valeur négative une affectation potentiellement discutable. Pour limiter le coût quadratique, chaque score utilise un échantillon reproductible de 5 000 observations, graine 42. K=3 obtient 0,470, le meilleur score testé, avec un compromis de lecture acceptable. Cela ne veut pas dire que les groupes sont parfaitement séparés. Environ 1,42 % des silhouettes individuelles échantillonnées sont négatives. Coude, silhouette et interprétation convergent vers K=3.

Sources : travail_v2/resultats/clustering_choix_k.csv et clustering_resume.json.

### 15. Les profils moyens des clusters — 17:00 à 18:20

Nous décrivons maintenant les groupes en unités réelles. C0 contient 11060 variantes, soit 53,1 % du catalogue d'analyse. C'est le profil le moins puissant, le plus léger et le moins émetteur en moyenne. C1 contient 7963 variantes, soit 38,2 %, et se distingue par la masse moyenne la plus élevée, environ 2 147 kg. C2 contient 1801 variantes, soit 8,6 %, avec puissance et CO2 très supérieurs. Les profils sont des résumés, pas des catégories commerciales officielles. Les distributions individuelles peuvent se chevaucher.

Source : travail_v2/resultats/clustering_profils.csv.

### 16. Une vue des clusters en deux dimensions — 18:20 à 19:40

L'ACP projette les trois variables standardisées sur deux axes synthétiques. Les axes 1 et 2 expliquent 67,1 % et 26,2 % de la variance, soit 93,3 % cumulés. La projection conserve donc une grande part de la variabilité. L'ACP ne sert pas ici à construire les clusters : nous colorons la projection avec les groupes calculés dans l'espace initial standardisé. Une séparation apparente en 2D n'est pas une nouvelle validation indépendante. Le chevauchement et les frontières doivent se lire avec la silhouette et la sensibilité. Les 660 points affichés sont un tirage équilibré par cluster, pas la répartition réelle des effectifs.

Sources : travail_v2/resultats/clustering_points.csv, clustering_acp_variance.csv.

### 17. Les motorisations dans chaque groupe — 19:40 à 21:00

Les énergies servent ici à interpréter les groupes après leur construction. GO signifie gazole et ES essence. C1 comporte près de 80 % de lignes GO, tandis que C2 comporte environ 96 % de lignes ES. C0 est plus mixte, avec environ 57 % de GO et 36 % d'ES. Les autres codes restent regroupés dans la catégorie autres pour la lisibilité, sans être assimilés à des électriques purs. Les hybrides représentent de petites parts de chaque groupe, environ 5,4 %, 4,7 % et 3,1 %. Ces distributions établissent une association descriptive. Elles ne prouvent pas qu'un carburant explique à lui seul la formation d'un groupe ou le niveau de CO2.

Sources : travail_v2/resultats/clustering_energies_pct.csv et clustering_hybrides_pct.csv.

### 18. La stabilité selon l’initialisation — 21:00 à 22:20

L'ARI mesure l'accord de deux partitions en corrigeant l'accord dû au hasard. Il vaut 1 pour deux partitions identiques à permutation d'étiquettes près, environ 0 pour un accord comparable au hasard, et peut être négatif. Nous comparons les partitions de cinq graines à la référence. La stabilité d'initialisation est proche de 1 pour toutes les graines, et les rééchantillonnages à 80 % donnent des ARI compris entre 0,9948 et 1. Le calcul compare les affectations sur une population commune par prédiction du modèle réajusté. Cela indique que la solution est numériquement stable pour cette population et ces variables. Cela ne garantit ni sa pertinence métier, ni sa robustesse à une population différente.

Source : travail_v2/resultats/clustering_stabilite.csv.

### 19. Le poids des familles dominantes — 22:20 à 23:40

Nous limitons maintenant chaque famille à 50 variantes, ce qui laisse 6248 lignes. Nous réajustons le scaler et K-Means puis comparons les affectations sur le catalogue complet. L'ARI tombe à 0,548, bien plus bas que lors des seules initialisations. La composition du catalogue modifie donc sensiblement les frontières. Retirer le CO2 donne ARI 0,809, ce qui montre aussi l'effet du choix des variables. Ces expériences ne rendent pas automatiquement le jeu plafonné plus représentatif d'une flotte : aucune pondération par les ventes ou kilomètres n'est disponible. L'objectif est de rendre la sensibilité visible.

Sources : travail_v2/resultats/clustering_stabilite.csv et clustering_profils_plafonnes.csv.

### 20. L’utilité environnementale de la segmentation — 23:40 à 25:00

Les profils offrent une lecture synthétique du catalogue. Ils peuvent aider à constituer des groupes comparables pour examiner une anomalie, choisir des variantes à étudier plus précisément ou prioriser un audit documentaire. Les émissions moyennes par cluster sont 123,9, 176,9, 244,6 g/km. Cependant le CO2 a servi à construire les groupes : retrouver un écart de CO2 n'est donc pas une découverte indépendante. Il faut confronter les groupes à des variables externes et à un besoin professionnel précis. Les noms moins émetteurs, plus lourds et plus puissants résument leurs moyennes relatives. On ne peut pas décider d'un remplacement à partir du seul cluster. Nous devons connaître usage, kilométrage, cycle de vie et contraintes fonctionnelles.

Source : travail_v2/resultats/clustering_profils.csv.

### 21. L’usage change la lecture environnementale — 25:00 à 26:40

Ce scénario illustratif montre une limite de l'indicateur g/km. À la moyenne C0, rouler 20 000 km par an correspond à environ 2,48 tonnes de CO2 déclaré, alors qu'à la moyenne C2, rouler 5 000 km correspond à 1,22 tonnes. Le classement par émission annuelle peut donc différer du classement par g/km. Ce calcul multiplie simplement une valeur d'homologation par un kilométrage hypothétique : il ne mesure pas des émissions réelles. Le jeu ne contient pas l'usage, la conduite, la recharge ni le cycle de vie. Par ailleurs, K-Means découpe même un continuum. Silhouette moyenne 0,470, chevauchements en projection et sensibilité au plafonnement invitent à traiter les clusters comme des profils descriptifs plutôt que des catégories naturelles fermées.

Source des moyennes : travail_v2/resultats/clustering_profils.csv. Kilométrages : hypothèses illustratives explicites. Formule : g/km × km/an / 1 000 000 = t/an.

### 22. Les prochaines expériences — 26:40 à 28:20

Nous proposons des expériences ciblées. Premièrement, un catalogue récent et un test temporel permettront d'évaluer la transférabilité. Deuxièmement, une pondération par usage réel ou une analyse à l'échelle des familles permettra de limiter la domination des nombreuses variantes. Troisièmement, une standardisation robuste et d'autres méthodes, par exemple clustering hiérarchique ou DBSCAN, éprouveront la dépendance à la distance et aux formes de clusters. Enfin, kilométrage, type d'usage, recharge et facteurs de cycle de vie permettront de discuter une véritable décision environnementale. Les méthodes facultatives ne remplacent pas l'interprétation. Avant un usage décisionnel, il faudra définir une erreur acceptable, vérifier les sous-populations, confronter les profils à des catégories externes et obtenir une validation indépendante.

Sources : limites des notebooks 02 et 03, sujet d'évaluation finale page 3.

### 23. Ce que permet cette étude — 28:20 à 30:00

Nous retenons trois enseignements reliés. Le modèle supervisé améliore nettement la baseline sur ce test familial, mais l'écart entre entraînement, validation et test limite la généralisation. La segmentation K=3 est interprétable en termes techniques et très stable face aux initialisations. Cependant son accord tombe à ARI 0,548 lorsqu'on plafonne les familles : la représentation du catalogue compte davantage que le seul hasard de l'algorithme. La valeur actuelle est donc exploratoire : comparer des profils et décider quelles données rechercher ensuite. Pour une décision environnementale ou professionnelle, il faut des données adaptées à l'usage, une population récente et une validation indépendante. Répondre explicitement à la question initiale : nous pouvons décrire des profils du catalogue et produire une estimation pédagogique du CO2, avec des limites documentées.

Sources : travail_v2/resultats/supervise_test.csv, clustering_resume.json, clustering_stabilite.csv.

## Préparation avant restitution

- Répéter avec chronomètre et limiter la partie supervisée à 5 minutes.
- Expliquer les axes et unités de chaque graphique avant le résultat.
- Dire que le test est une évaluation rétrospective au sein du catalogue, déjà exploré, et qu’une validation indépendante reste nécessaire.
- Distinguer stabilité aux graines et sensibilité au poids des familles.
- Préciser que le CO₂ participe à la construction des clusters : les écarts de CO₂ entre groupes ne sont pas une validation indépendante.
- Préparer une réponse sur les 56 lignes EL exclues, le caractère historique des données et les variables d’usage absentes.
