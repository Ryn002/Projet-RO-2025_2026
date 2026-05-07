# Cout explicite des scenarios

## Objectif

Ce fichier est une annexe de comparaison des scenarios operationnels S1, S2 et
S3 avec les seuls couts explicitement donnes dans l'enonce :

- achat des camions ;
- entretien annuel ;
- recette de revente approximative.

Il ne constitue pas une fonction objectif complete avec cout kilometrique. Le
scenario **S3 hybride** reste le scenario principal retenu pour le modele de
flotte.

On ne tient donc pas encore compte :

- du prix au kilometre ;
- du carburant ;
- des chauffeurs ;
- des peages ;
- du cout d'immobilisation pendant les changements de compartiment ;
- d'un taux d'actualisation inter-annuel.

Ces elements sont des extensions possibles.

## Couts donnes dans l'enonce et hypotheses retenues

| Element | Valeur |
|---|---:|
| Achat camion type 1 | 140000 euros |
| Achat camion type 2 | 200000 euros |
| Entretien annuel par camion | 5000 euros/an |
| Revente camion | `C / (1 + alpha)^n` |

Pour le modele principal, on retient :

```math
\alpha = 0,25
```

L'age initial des camions est suppose nul au debut de l'horizon. Dans cette
convention, l'annee de vente `t` est interpretee comme l'age moyen du camion
vendu en fin d'annee `t`.

Le modele principal utilise donc le prix moyen de revente :

```math
\bar C^{vente}_{k,t} = \frac{C_k}{(1+\alpha)^t}
```

Avec `alpha = 0,25` :

```math
\bar C^{vente}_{1,t} = \frac{140000}{1,25^t}
```

```math
\bar C^{vente}_{2,t} = \frac{200000}{1,25^t}
```

| Annee de vente t | Revente type 1 | Revente type 2 |
|---:|---:|---:|
| 1 | 112000 euros | 160000 euros |
| 2 | 89600 euros | 128000 euros |
| 3 | 71680 euros | 102400 euros |
| 4 | 57344 euros | 81920 euros |
| 5 | 45875,20 euros | 65536 euros |

On ne suit pas les cohortes detaillees dans le modele principal. Ce suivi reste
une extension possible. Une sensibilite sur
`alpha ∈ {0,15 ; 0,25 ; 0,35}` pourra etre faite plus tard.

## Flotte initiale

La flotte initiale donnee dans l'enonce est :

```math
N^0_1 = 4
\qquad
N^0_2 = 6
```

## Flottes demandees par les scenarios

Les besoins de flotte proviennent du fichier `tests_bases_couplage_anvers.md`.

| Scenario | Type 1 demande | Type 2 demande | Total camions | Statut |
|---|---:|---:|---:|---|
| Scenario 1 | 10 | 3 | 13 | comparaison |
| Scenario 2 | 4 | 7 | 11 | comparaison |
| **Scenario 3** | **5** | **6** | **11** | **scenario principal** |

## Achats et ventes necessaires

On compare chaque scenario a la flotte initiale.

```math
A_{k,s} = \max(0, N_{k,s} - N^0_k)
```

```math
R_{k,s} = \max(0, N^0_k - N_{k,s})
```

| Scenario | Achat T1 | Achat T2 | Vente T1 | Vente T2 |
|---|---:|---:|---:|---:|
| Scenario 1 | 6 | 0 | 0 | 3 |
| Scenario 2 | 0 | 1 | 0 | 0 |
| Scenario 3 | 1 | 0 | 0 | 0 |

## Cout d'achat

```math
C^{achat}_s = 140000 A_{1,s} + 200000 A_{2,s}
```

| Scenario | Calcul | Cout d'achat |
|---|---|---:|
| Scenario 1 | `6 x 140000` | 840000 euros |
| Scenario 2 | `1 x 200000` | 200000 euros |
| Scenario 3 | `1 x 140000` | 140000 euros |

## Entretien annuel

```math
C^{entretien}_s = 5000 (N_{1,s} + N_{2,s})
```

| Scenario | Nombre de camions | Entretien annuel |
|---|---:|---:|
| Scenario 1 | 13 | 65000 euros/an |
| Scenario 2 | 11 | 55000 euros/an |
| Scenario 3 | 11 | 55000 euros/an |

## Recette de revente

Dans cette comparaison de premiere annee, la seule revente apparait dans le
scenario 1 : on revend 3 camions type 2 en fin d'annee 1.

Avec `alpha = 0,25` et l'annee de vente `t = 1` :

```math
Recette^{vente}_1 = 3 \times \frac{200000}{1,25} = 480000
```

Pour les scenarios 2 et 3 :

```math
Recette^{vente}_2 = Recette^{vente}_3 = 0
```

## Cout net de changement de flotte

```math
C^{changement}_s = C^{achat}_s - Recette^{vente}_s
```

| Scenario | Cout d'achat | Recette de revente | Cout net de changement |
|---|---:|---:|---:|
| Scenario 1 | 840000 | 480000 | 360000 euros |
| Scenario 2 | 200000 | 0 | 200000 euros |
| Scenario 3 | 140000 | 0 | 140000 euros |

## Cout explicite de la premiere annee

On additionne ici :

```math
cout explicite annee 1 = cout net de changement + entretien annuel
```

| Scenario | Cout net changement | Entretien annuel | Cout explicite annee 1 |
|---|---:|---:|---:|
| Scenario 1 | 360000 | 65000 | 425000 euros |
| Scenario 2 | 200000 | 55000 | 255000 euros |
| Scenario 3 | 140000 | 55000 | 195000 euros |

## Tableau comparatif

| Critere | Scenario 1 | Scenario 2 | Scenario 3 | Meilleur |
|---|---:|---:|---:|---|
| Achat initial | 840000 | 200000 | 140000 | S3 |
| Entretien annuel | 65000 | 55000 | 55000 | S2/S3 |
| Revente estimee | 480000 | 0 | 0 | S1 |
| Cout changement | 360000 | 200000 | 140000 | S3 |
| Cout explicite annee 1 | 425000 | 255000 | 195000 | S3 |

## Lecture

Avec les seuls couts explicites de l'enonce et l'hypothese centrale
`alpha = 0,25`, le scenario 3 est le moins cher pour le changement de flotte et
pour le cout explicite de premiere annee.

Le scenario 1 recupere une recette de revente, mais il demande beaucoup plus
d'achats de camions type 1. Cette recette ne suffit pas a compenser l'achat
initial plus eleve dans l'hypothese principale.

Le scenario 3 est donc coherent avec le choix operationnel retenu : il minimise
la distance dans le test de couplage et il donne aussi le plus faible cout de
changement parmi les trois scenarios.

Une extension possible serait d'ajouter un cout kilometrique :

```math
C^{total}_s = C^{changement}_s + C^{entretien}_s + c_{km} D_s
```
