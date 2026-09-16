# Cas d'usage : compléter un inventaire ancien de véhicules

Un gestionnaire dispose des chevaux fiscaux et du statut hybride, mais pas du CO₂ sur certaines fiches. L'outil propose une estimation provisoire de CO₂ déclaré, accompagnée d'une plage indicative et du nombre de familles comparables. Si l'identifiant exact est disponible, une recherche dans le catalogue est préférable.

## Résultats mesurés

- Source : catalogue local de mars 2015 ; 20 824 lignes avec cible connue.
- Entrées : chevaux fiscaux et hybride oui/non ; cible : CO₂ mixte en g/km.
- Modèle retenu par validation interne : Linéaire CV + hybride.
- Test sur 6381 lignes de 72 familles jamais vues.
- MAE globale : **34.6 g/km**, contre **43.6 g/km** pour la médiane constante.
- MAE avec un poids égal par famille de test : **24.8 g/km**.
- R² global : **-0.05**, ce qui signale une généralisation insuffisante selon ce critère.
- MAE hybrides : **25.7 g/km**, sur seulement 73 variantes de 9 familles.
- Couverture effective de la plage indicative : 60.1 % globalement et 87.7 % chez les hybrides. La plage n'est pas une garantie individuelle.

## Exemple : fiche à 7 CV, 15 000 km par an

| Profil | CO₂ estimé | Plage indicative | Scénario annuel |
|---|---:|---:|---:|
| Non hybride | 127.7 g/km | 84.6–170.8 g/km | 1.92 t/an |
| Hybride | 93.1 g/km | 62.8–123.4 g/km | 1.4 t/an |

Pour l'hybride à 7 CV, l'entraînement contient seulement 14 variantes de 5 familles. Le support est limité. Ces profils ne représentent pas le même véhicule avant/après hybridation : leur différence ne mesure pas un gain causal. Le scénario annuel multiplie une valeur déclarée par une distance hypothétique ; il ne mesure pas les émissions réelles.

## Recul indispensable

1. Le CO₂ ne résume pas la pollution locale (NOx, particules) ni le cycle de vie. Le [catalogue ADEME](https://www.data.gouv.fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france) distingue ces mesures.
2. La formule historique des CV incorporait le CO₂ : le lien appris est en partie administratif. Cela rend crédible un usage de reconstitution de fiche, mais ne démontre pas une causalité. [Source : article 62 de la loi du 2 juillet 1998](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000006320193).
3. Les données de 2015 ne valident pas un usage sur les véhicules actuels. Les électriques purs sans cible sont exclus.
4. Les variantes de catalogue ne sont pas pondérées par les ventes. La séparation par famille réduit un risque de fuite, sans supprimer toutes les dépendances entre véhicules.
5. Le type d'hybridation et le carburant manquent dans cette interface : un hybride rechargeable et un autre hybride ne sont pas interchangeables.

## Décision proposée

**Ne pas automatiser le préremplissage à ce stade.** Le R² négatif et la couverture de seulement 60.1 % montrent que le prototype n'est pas assez fiable sur l'ensemble du catalogue. Les familles SPRINTER et CRAFTER, très présentes dans le test, sont nettement sous-estimées ; leur diagnostic est exporté dans `diagnostic_familles.csv`. Elles restent dans l'évaluation : on ne les retire pas pour embellir le résultat.

Conserver le prototype pour une démonstration exploratoire et pour orienter la collecte d'informations. Retrouver la fiche exacte pour les décisions opérationnelles. Ne pas décider le remplacement d'un véhicule à partir de ces deux entrées. Les résultats meilleurs que la médiane d'entraînement ne suffisent pas à valider le cas d'usage. Le R² se compare à une autre référence : la moyenne du test, indisponible lors d'une vraie prédiction.

Avant un déploiement : fixer avec le gestionnaire l'erreur acceptable, mesurer le temps gagné par rapport à une recherche par CNIT, enrichir les caractéristiques (masse, carburant, catégorie de véhicule, type d'hybridation) et évaluer sur un catalogue plus récent. Le test ayant été analysé, les prochaines évolutions nécessiteront une nouvelle validation indépendante. Aucune validation en situation réelle n'a été réalisée.

Le notebook `Datascience_et_ML_Prediction_CO2.ipynb` contient le code exécuté, les scores, le graphique et la fonction `predire_co2(7, hybride=True, km_annuels=15000)`.
