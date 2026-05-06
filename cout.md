# Cout explicite des scenarios

## Objectif

Ce fichier compare les trois scenarios de transport uniquement avec les couts
explicitement donnes dans l'enonce.

On ne tient donc pas encore compte :

- du prix au kilometre ;
- du carburant ;
- des chauffeurs ;
- des peages ;
- du cout d'immobilisation pendant les changements de compartiment ;
- d'un taux d'actualisation.

Ces elements pourront etre ajoutes ensuite.

## Couts donnes dans l'enonce

| Element | Valeur |
|---|---:|
| Achat camion type 1 | 140000 euros |
| Achat camion type 2 | 200000 euros |
| Entretien annuel par camion | 5000 euros/an |
| Revente camion | `C / (1 + alpha)^n` |

Avec :

```math
C = \text{prix d'achat du camion}
```

```math
\alpha \in [0,1]
```

```math
n = \text{age du camion en annees}
```

L'enonce ne donne pas de valeur numerique pour `alpha`, ni l'age exact des
camions initiaux. La revente est donc gardee sous forme symbolique.

## Flotte initiale

La flotte initiale donnee dans l'enonce est :

```math
N^0_1 = 4
\qquad
N^0_2 = 6
```

## Flottes demandees par les scenarios

Les besoins de flotte proviennent du fichier de test de couplage.

| Scenario | Type 1 demande | Type 2 demande | Total camions |
|---|---:|---:|---:|
| Scenario 1 | 10 | 3 | 13 |
| Scenario 2 | 4 | 7 | 11 |
| Scenario 3 | 5 | 6 | 11 |

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

La seule revente apparait dans le scenario 1 : on revend 3 camions type 2.

Si leur age au moment de la revente est `n`, alors :

```math
C^{vente}_{T2,n} = \frac{200000}{(1+\alpha)^n}
```

Donc :

```math
Recette^{vente}_1 = 3 \times \frac{200000}{(1+\alpha)^n}
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
| Scenario 1 | 840000 | `600000 / (1 + alpha)^n` | `840000 - 600000 / (1 + alpha)^n` |
| Scenario 2 | 200000 | 0 | 200000 |
| Scenario 3 | 140000 | 0 | 140000 |

## Cout explicite de la premiere annee

On additionne ici :

```math
cout explicite annee 1 = cout net de changement + entretien annuel
```

| Scenario | Cout net changement | Entretien annuel | Cout explicite annee 1 |
|---|---:|---:|---:|
| Scenario 1 | `840000 - 600000 / (1 + alpha)^n` | 65000 | `905000 - 600000 / (1 + alpha)^n` |
| Scenario 2 | 200000 | 55000 | 255000 |
| Scenario 3 | 140000 | 55000 | 195000 |

## Tableau comparatif

| Critere | Scenario 1 | Scenario 2 | Scenario 3 | Meilleur |
|---|---:|---:|---:|---|
| Achat initial | 840000 | 200000 | 140000 | S3 |
| Entretien annuel | 65000 | 55000 | 55000 | S2/S3 |
| Revente | `600000 / (1 + alpha)^n` | 0 | 0 | S1 |
| Cout changement | `840000 - 600000 / (1 + alpha)^n` | 200000 | 140000 | depend de `alpha,n` |
| Cout explicite annee 1 | `905000 - 600000 / (1 + alpha)^n` | 255000 | 195000 | depend de `alpha,n` |

## Lecture

Avec les seuls couts explicites de l'enonce, le scenario 3 est le moins cher en
achat et en entretien.

Le scenario 1 peut recuperer une recette de revente, mais cette recette depend
de `alpha` et de l'age `n`, qui ne sont pas fixes numeriquement par l'enonce.
Sans hypothese supplementaire sur ces deux valeurs, on ne peut pas donner un
classement numerique definitif incluant la revente.

La prochaine etape sera d'ajouter un cout kilometrique pour comparer :

```math
C^{total}_s = C^{changement}_s + C^{entretien}_s + c_{km} D_s
```
