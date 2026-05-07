# Hypothèses de modélisation finales — Projet RO "Transport de produits chimiques"

Ce document fixe les hypothèses retenues pour le modèle principal du projet. Il
sert de référence commune pour le rapport, les tests de scénarios et la
formulation PL/PLNE.

Le problème réel combine deux niveaux :

- un niveau opérationnel : choix des tournées, ordre des villes, chargements ;
- un niveau stratégique : achats, ventes et affectations de camions sur 5 ans.

Résoudre simultanément ces deux niveaux reviendrait à coupler un problème de
tournées de véhicules avec un problème de gestion de flotte. Ce serait trop lourd
pour le cadre du projet. Le choix final est donc un découplage en deux étapes :

```text
Tournées-types fixées -> capacités journalières/annuelles -> PL/PLNE de flotte
```

L'étape opérationnelle est traitée par scénarios et calculs manuels. L'étape
stratégique utilise ces résultats comme paramètres d'entrée.

---

## 1. Hypothèses finales retenues pour le modèle principal

| Sujet | Choix retenu |
|---|---|
| Horizon | 5 années, `T = {1,2,3,4,5}` |
| Scénario opérationnel | Scénario hybride S3, issu de `tests_bases_couplage_anvers.md` |
| Jours ouvrables | 250 jours/an |
| Temps de travail | 8 h/jour/camion, soit `H^max = 2000 h/an` |
| Rechargement à Liège | Non ajouté explicitement dans S3 principal |
| Couplage acide/base | Couplage partiel via Anvers uniquement, avec camions type 2 |
| Changement d'affectation | Affectation fixe à l'année ; pas de changement en cours d'année |
| Hasselt | 350 t en année 1, 825 t en année 2, 1300 t/an en années 3 à 5 |
| Flotte initiale | 4 camions type 1, 6 camions type 2 |
| Âge initial | Camions supposés neufs au début de l'horizon, âge 0 |
| Amortissement principal | `α = 0,25` |
| Revente | Prix moyen de revente par type et par année ; pas de suivi par cohortes |
| Convention de vente | Vente en fin d'année : camion disponible pendant l'année t, retiré en t+1 |
| Variabilité | Demandes déterministes, pas de saisonnalité fine |
| Coûts de base | Achat, entretien, revente ; pas de coût kilométrique dans le modèle principal |

---

## 2. Scénario opérationnel principal : S3 hybride

Le scénario principal retenu est le **scénario hybride S3**. Il devient le
scénario de référence pour paramétrer le modèle stratégique.

Il est retenu car, parmi les trois scénarios testés, il est le meilleur compromis
sur les critères disponibles :

| Scénario | Type 1 | Type 2 | Total | Distance | Coût net de changement |
|---|---:|---:|---:|---:|---:|
| S1 : garder Anvers dans les tournées acide | 10 | 3 | 13 | 3185 km/j | 360000 € |
| S2 : retirer Anvers des tournées acide | 4 | 7 | 11 | 2880 km/j | 200000 € |
| **S3 : hybride retenu** | **5** | **6** | **11** | **2765 km/j** | **140000 €** |

Le scénario S3 combine :

- des tournées acide classiques depuis Liège vers Charleroi, Bruxelles et Gand ;
- une tournée mixte Liège-Anvers-Hasselt-Liège ;
- des rotations directes Liège-Anvers-Liège pour coupler l'acide vers Anvers et
  la base au retour ;
- des rotations base restantes si nécessaire.

Le bilan journalier de référence en régime permanent est :

| Bloc | Tournées | Type | Acide | Base | Distance |
|---|---|---|---:|---:|---:|
| CH | 2 x LI-CH-LI | T1 | 33 t | 0 | 400 km |
| CH/BR | LI-CH-LI + LI-BR-LI | T1 | 31,3 t | 0 | 400 km |
| GA/BR | LI-GA-BR-LI | T1 | 16,5 t | 0 | 280 km |
| AN/HA | LI-AN-HA-LI | T2 | 16,2 t | 5,5 t | 215 km |
| AN direct | 5 x LI-AN-LI | T2 | 25 t | 82,5 t | 1050 km |
| Base restante | 2 x LI-AN-LI | T1 | 0 | 32 t | 420 km |
| **Total** |  |  | **122 t** | **120 t** | **2765 km/j** |

S1 et S2 sont conservés uniquement comme scénarios comparatifs. Ils ne
paramètrent pas le modèle principal.

---

## 3. Cadre journalier et capacité annuelle

Le modèle principal utilise :

- 250 jours ouvrables par an ;
- 8 h de travail par jour et par camion ;
- donc `H^max = 250 x 8 = 2000 h/an`.

Une tournée acide part de Liège, dessert une ou plusieurs villes, puis revient à
Liège. Son temps est calculé par :

```text
T_r = distance_r / 70 + nombre_arrets_acide
```

Pour les bases, les tests ajoutent le chargement à Anvers et le déchargement à
Liège :

```text
T_r = distance_r / 70 + arrets_acide + 0,5 chargement_base + dechargement_base
```

La variante avec 9 h/jour et 0,5 h de rechargement à Liège entre deux tournées
est conservée comme **analyse de sensibilité**. Elle ne remplace pas le cadre
principal.

---

## 4. Rechargement à Liège

Dans le scénario S3 principal, on ne rajoute pas explicitement 0,5 h de
rechargement à Liège entre deux tournées d'acide effectuées par un même camion.

C'est une hypothèse simplificatrice et légèrement optimiste. Elle revient à
supposer que les opérations de préparation ou de rechargement sont intégrées dans
l'organisation journalière sans créer de temps supplémentaire modélisé.

Le fichier `archives/tests_acide_type1_9h_rechargement.md` conserve une variante
où le rechargement est explicitement ajouté. Cette variante sert uniquement à
tester la robustesse du dimensionnement.

---

## 5. Demandes annuelles

### Bases

La demande de base est constante :

```text
Base AN -> LI : 30000 t/an
```

Avec 250 jours ouvrables, cela correspond à :

```text
30000 / 250 = 120 t/j
```

### Acides hors Hasselt

Les demandes annuelles suivantes sont constantes sur les cinq années :

| Ville | Demande annuelle | Demande journalière |
|---|---:|---:|
| Anvers | 9000 t/an | 36 t/j |
| Charleroi | 12000 t/an | 48 t/j |
| Gand | 2000 t/an | 8 t/j |
| Bruxelles | 6200 t/an | 24,8 t/j |

### Hasselt

Hasselt est traité séparément car l'énoncé indique qu'une nouvelle unité démarre
après 18 mois.

Le modèle principal retient :

| Année | Demande HA | Justification |
|---:|---:|---|
| 1 | 350 t | Situation initiale |
| 2 | 825 t | `0,5 x 350 + 0,5 x 1300` |
| 3 à 5 | 1300 t/an | Nouvelle unité en régime plein |

Comme la quantité minimale par livraison est de 5 t, Hasselt n'est pas livré
tous les jours en années 1 et 2 :

| Année | Demande HA | Nombre de livraisons | Quantité par livraison |
|---:|---:|---:|---:|
| 1 | 350 t | 70 | 5 t |
| 2 | 825 t | 165 | 5 t |
| 3 à 5 | 1300 t | 250 | 5,2 t |

---

## 6. Couplage acide/base

Le modèle principal n'autorise pas un couplage général libre sur tout le réseau.

Le couplage retenu est **partiel et limité à Anvers** :

- certains camions type 2 livrent de l'acide de Liège vers Anvers ;
- leur autre compartiment ramène de la base d'Anvers vers Liège ;
- le couplage exploite les deux compartiments des camions type 2 ;
- les autres trajets restent traités comme des tournées acide ou base classiques.

Cette restriction garde le modèle maîtrisable et correspond au scénario S3. Elle
évite de transformer le projet en problème complet de routage multi-produits.

---

## 7. Affectation des compartiments

L'énoncé indique qu'un changement d'affectation d'un compartiment immobilise le
camion pendant 3 jours ouvrables.

Dans le modèle principal, on retient une affectation fixe à l'année :

- un compartiment garde son affectation pendant toute l'année ;
- il n'y a pas de changement d'affectation en cours d'année ;
- les 3 jours d'immobilisation ne sont donc pas activés dans les tournées
  journalières ;
- l'affectation peut être revue entre deux années dans le modèle stratégique.

C'est une simplification volontaire. Elle est défendable car le modèle cherche
une stratégie annuelle de flotte, pas un planning opérationnel quotidien complet.

---

## 8. Flotte initiale et âge initial

La flotte initiale est celle de l'énoncé :

```text
N_1,0 = 4
N_2,0 = 6
```

L'âge initial des camions est inconnu. Le modèle principal suppose que les camions
initiaux sont neufs au début de l'horizon, donc d'âge 0.

Cette hypothèse permet de calculer une valeur moyenne de revente sans introduire
un historique antérieur non fourni par l'énoncé.

---

## 9. Coûts, amortissement et revente

Les coûts explicitement donnés sont :

| Élément | Valeur |
|---|---:|
| Achat camion type 1 | 140000 € |
| Achat camion type 2 | 200000 € |
| Entretien annuel par camion | 5000 €/an |
| Revente | `C / (1 + α)^n` |

Le modèle principal retient :

```text
α = 0,25
```

Cette valeur est utilisée comme hypothèse centrale. Une analyse de sensibilité
est prévue avec :

```text
α ∈ {0,15 ; 0,25 ; 0,35}
```

### Prix moyen de revente retenu dans le modèle principal

Le modèle principal ne suit pas les cohortes détaillées d'achat et de vente.
Cette simplification permet de garder un modèle de flotte agrégé, lisible et
directement codable.

À la place, on utilise un prix moyen de revente par type et par année :

```text
\bar C^{vente}_{k,t} = C_k / (1 + α)^t
```

Dans cette formule, `t` est interprété comme l'âge moyen du camion vendu en fin
d'année `t`. Cette convention est cohérente avec l'hypothèse selon laquelle les
camions initiaux sont neufs au début de l'horizon et les ventes sont réalisées en
fin d'année.

Avec `α = 0,25`, les prix moyens de revente utilisés dans le modèle principal
sont :

| Année de vente `t` | Revente type 1 | Revente type 2 |
|---:|---:|---:|
| 1 | 112000 € | 160000 € |
| 2 | 89600 € | 128000 € |
| 3 | 71680 € | 102400 € |
| 4 | 57344 € | 81920 € |
| 5 | 45875,20 € | 65536 € |

Ces valeurs proviennent de :

```text
\bar C^{vente}_{1,t} = 140000 / 1,25^t
```

```text
\bar C^{vente}_{2,t} = 200000 / 1,25^t
```

Cette approximation garde une fonction objectif simple :

```text
achats + entretien - recettes de revente moyennes
```

### Extension possible : suivi détaillé par cohortes

Le suivi détaillé par cohortes est conservé comme extension possible, mais il
n'est pas retenu dans le modèle principal.

---

## 10. Convention temporelle des décisions

Les conventions temporelles finales sont :

- horizon : années `1` à `5` ;
- les achats de l'année `t` sont disponibles pendant toute l'année `t` ;
- les ventes de l'année `t` ont lieu en fin d'année ;
- un camion vendu en année `t` reste utilisable pendant l'année `t` ;
- il n'est plus disponible à partir de l'année `t+1` ;
- la recette de revente est comptée en fin d'année `t`.

Conséquence sur l'évolution de flotte :

```text
N_{k,t} = N_{k,t-1} - V_{k,t-1} + A_{k,t}
```

avec `V_{k,0} = 0`. La variable `N_{k,t}` représente donc les camions
disponibles pendant l'année `t`.

---

## 11. Conséquences sur la modélisation

Les choix précédents impliquent directement :

| Choix | Conséquence dans le modèle |
|---|---|
| S3 retenu | Les capacités et besoins de flotte viennent du scénario hybride |
| 8 h/jour, 250 jours | `H^max = 2000 h/an` |
| Rechargement non explicite | Les temps S3 ne contiennent pas de pénalité de 0,5 h à Liège |
| Hasselt annuel | Les contraintes de demande utilisent 350 / 825 / 1300 |
| Couplage limité à Anvers | Pas de variable de couplage libre sur tous les arcs |
| Affectation annuelle fixe | Pas de perte de 3 jours en cours d'année |
| Revente simplifiée | Pas de variables de cohortes `V_{k,s,t}` dans le PL principal |
| Vente en fin d'année | Les ventes réduisent la flotte disponible à partir de `t+1` |

---

## 12. Analyses de sensibilité prévues

Les variantes suivantes ne font pas partie du modèle principal, mais peuvent être
discutées dans le rapport :

- `α ∈ {0,15 ; 0,25 ; 0,35}` pour tester l'effet du taux d'amortissement ;
- variante à 9 h/jour avec 0,5 h de rechargement à Liège ;
- comparaison des scénarios S1, S2 et S3 ;
- effet d'un coût kilométrique si l'on décide d'enrichir la fonction objectif ;
- effet d'une demande Hasselt non moyennée sur l'année.

---

## 13. Extensions possibles non retenues

Les extensions suivantes sont volontairement exclues du modèle principal :

- résolution d'un VRP complet ;
- suivi détaillé des cohortes de camions achetés et vendus ;
- coûts de chauffeurs ;
- pannes et indisponibilités aléatoires ;
- saisonnalité fine des demandes ;
- coût kilométrique détaillé ;
- affectations de compartiments changeant en cours d'année ;
- couplage acide/base libre sur tous les trajets ;
- modèle multi-objectif complet.

Ces extensions peuvent être mentionnées comme limites ou pistes d'amélioration,
mais elles ne doivent pas brouiller la formulation principale.

---

## 14. Points tranchés et points de vigilance

### Points tranchés

- S3 est le scénario opérationnel principal.
- Le cadre principal reste 8 h/jour et 250 jours/an.
- La variante 9 h/rechargement est une sensibilité.
- Hasselt vaut 350 / 825 / 1300 sur les années 1 / 2 / 3-5.
- Le couplage est partiel via Anvers uniquement.
- L'affectation des compartiments est fixe à l'année.
- `α = 0,25` est la valeur principale.
- La revente est modélisée par prix moyen, sans cohortes.
- Les ventes sont en fin d'année.

### Points de vigilance à signaler dans le rapport

- L'absence de rechargement explicite dans S3 rend le scénario légèrement
  optimiste.
- La demande est moyennée sur l'année, ce qui masque les éventuels pics
  intra-annuels.
- Le prix moyen de revente est une approximation.
- Le scénario S3 est optimal en distance uniquement dans le cadre des hypothèses
  de test, pas dans un VRP général.
