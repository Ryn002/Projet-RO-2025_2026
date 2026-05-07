# Couts des scenarios

## Objectif

Ce fichier compare les scenarios de transport avec :

- les achats et ventes de camions ;
- l'entretien annuel ;
- le cout du trajet, compose ici du cout kilometrique et du cout chauffeur ;
- la devalorisation des camions dans la recette de revente.

Tous les montants sont pris **HTVA**. Les peages et la redevance kilometrique
belge sont ignores dans le modele.

---

## Parametres de cout retenus

| Element | Valeur |
|---|---:|
| Achat camion type 1 | 140000 euros |
| Achat camion type 2 | 200000 euros |
| Entretien annuel par camion | 5000 euros/an |
| Cout kilometrique hors peage | 0,60 euros/km |
| Cout chauffeur | 35 euros/h |
| Temps de travail | 9 h/jour/camion |
| Jours ouvrables | 250 jours/an |
| Taux d'amortissement `alpha` | 0,20 |
| Peage / Viapass | 0 euro/km |

Le cout chauffeur s'applique a tout le temps de travail :

- conduite ;
- livraison acide ;
- chargement de base a Anvers ;
- dechargement de base a Liege ;
- rechargement a Liege avant une deuxieme tournee.

Donc un camion mobilise :

```math
35 \times 9 \times 250 = 78750 \text{ euros/an}
```

---

## Justification de `alpha`

L'enonce impose la formule de revente :

```math
C^{vente}_{k,n} = \frac{C_k}{(1+\alpha)^n}
```

mais ne fixe pas `alpha`. On retient :

```math
\alpha = 0,20
```

Cette valeur est une approximation simple et proche du contexte :

- le CNR observe, pour le transport routier belge, que les transporteurs
  conservent les tracteurs environ 7 ans en moyenne, avec des contrats de leasing
  souvent centres autour de 60 mois
  ([CNR, transport routier belge 2021](https://www.cnr.fr/download/file/publications/CNR%20-%20Le%20transport%20routier%20de%20marchandises%20belge%20-%202021%20.pdf)) ;
- en Belgique, les vehicules professionnels sont souvent amortis sur 5 ans, soit
  20 %/an en lineaire
  ([myfid, amortissement Belgique](https://www.myfid.be/ressources/fiscalite/amortissement/)).

Avec la formule de l'enonce :

```math
\frac{1}{1,20^5} \approx 0,40
\qquad
\frac{1}{1,20^7} \approx 0,28
```

Un camion garde donc environ 40 % de sa valeur apres 5 ans et 28 % apres 7 ans.

---

## Fonction de cout

La fonction economique sur 5 ans est :

```math
\min Z =
\sum_{t,k} C^{achat}_k A_{k,t}
+ \sum_{t,k} C^{entretien} N_{k,t}
+ \sum_t C^{trajet}_t
- \sum_{k,s,t} \frac{C^{achat}_k}{(1+\alpha)^{t-s}} V_{k,s,t}
```

avec :

```math
C^{trajet}_t = C^{km}_t + C^{chauffeur}_t
```

```math
C^{km}_t = 0,60 \times D^{annuel}_t
```

```math
C^{chauffeur}_t = 35 \times 9 \times 250 \times (N_{1,t}+N_{2,t})
```

La devalorisation n'est donc pas un cout ajoute automatiquement chaque annee.
Elle intervient dans la recette de vente : plus `alpha` ou l'age `n` est grand,
plus la recette de vente est faible.

---

## Flotte initiale

```math
N^0_1 = 4
\qquad
N^0_2 = 6
```

Avec la convention 9 h/jour, le fichier `test_annuel.md` montre
que le scenario 3 est faisable avec cette flotte initiale :

```math
N_1 = 4
\qquad
N_2 = 6
```

Il n'est donc plus necessaire d'acheter un camion type 1 supplementaire.

---

## Scenarios disponibles

| Scenario | Type 1 | Type 2 | Total | Lecture |
|---|---:|---:|---:|---|
| S1 | 7 | 3 | 10 | garder Anvers dans les tournees acide |
| S2 | 4 | 7 | 11 | retirer Anvers des tournees acide |
| S3 | 4 | 6 | 10 | hybride journalier |
| S4 | 4 | 6 | 10 | hybride annuel avec affectation stable |

Distances moyennes corrigees :

| Annee | S1 | S2 | S3 | S4 |
|---:|---:|---:|---:|---:|
| 1 | 3181,4 km/j | 2793,6 km/j | 2761,4 km/j | 2748,8 km/j |
| 2 | 3183,3 km/j | 2839,2 km/j | 2763,3 km/j | 2750,7 km/j |
| 3-5 | 3185 km/j | 2880 km/j | 2765 km/j | 2752,4 km/j |

---

## Cout de changement initial

On compare chaque scenario a la flotte initiale `4 T1 + 6 T2`.

Avec `alpha = 0,20`, la revente d'un camion type 2 apres 1 an vaut :

```math
\frac{200000}{1,20} \approx 166667
```

| Scenario | Achats | Ventes | Cout net de changement |
|---|---:|---:|---:|
| S1 | `3 T1 = 420000` | `3 T2 ≈ 500000` | -80000 euros |
| S2 | `1 T2 = 200000` | 0 | 200000 euros |
| S3 | 0 | 0 | 0 euro |
| S4 | 0 | 0 | 0 euro |

Le cout net negatif de S1 signifie qu'on recupere plus en vendant 3 camions type
2 qu'on ne depense pour acheter 3 camions type 1. Mais S1 parcourt beaucoup plus
de kilometres.

---

## Cout annuel par scenario

On additionne :

```math
C^{annuel}_{s,t}
= C^{entretien}_s
+ C^{chauffeur}_s
+ C^{km}_{s,t}
```

| Annee | S1 | S2 | S3 | S4 |
|---:|---:|---:|---:|---:|
| 1 | 1314710 euros | 1340290 euros | 1251710 euros | 1249820 euros |
| 2 | 1314995 euros | 1347130 euros | 1251995 euros | 1250105 euros |
| 3 | 1315250 euros | 1353250 euros | 1252250 euros | 1250360 euros |
| 4 | 1315250 euros | 1353250 euros | 1252250 euros | 1250360 euros |
| 5 | 1315250 euros | 1353250 euros | 1252250 euros | 1250360 euros |

---

## Cout total sur 5 ans par scenario fixe

Sans actualisation et sans liquidation finale de la flotte :

```math
C^{total}_s =
C^{changement}_s
+ \sum_{t=1}^{5} C^{annuel}_{s,t}
```

| Scenario | Cout changement | Somme couts annuels | Cout total 5 ans |
|---|---:|---:|---:|
| S1 | -80000 | 6575455 | 6495455 euros |
| S2 | 200000 | 6747170 | 6947170 euros |
| S3 | 0 | 6260455 | 6260455 euros |
| S4 | 0 | 6251005 | 6251005 euros |

---

## Proposition 1 - Ne pas changer la flotte, garder S3

On conserve la flotte initiale :

```math
4 T1 + 6 T2
```

On applique le scenario 3 chaque annee.

Il n'y a ni achat ni vente :

```math
C^{changement} = 0
```

Le cout total sur 5 ans est :

```math
C^{P1} = 6260455 \text{ euros}
```

---

## Proposition 2 - Autoriser achats/ventes et changer le trajet

On laisse le modele choisir le scenario le moins couteux parmi S1, S2, S3 et S4,
en tenant compte :

- des achats ;
- des ventes avec devalorisation ;
- de l'entretien ;
- du cout du trajet.

Le meilleur choix est S4 :

```math
4 T1 + 6 T2
```

donc la flotte ne change pas. Le gain vient seulement du trajet : S4 planifie la
base restante sur l'annee et reduit les rotations de base restante de 500 a 485
par an. Les 3 jours d'immobilisation ne s'appliqueraient que si un compartiment
etait effectivement converti d'acide vers base ou de base vers acide.

Le cout total sur 5 ans est :

```math
C^{P2} = 6251005 \text{ euros}
```

Comparaison :

```math
C^{P1} - C^{P2}
= 6260455 - 6251005
= 9450 \text{ euros}
```

La proposition 2 est donc meilleure, mais pas parce qu'elle vend ou achete des
camions. Elle est meilleure parce qu'elle choisit un trajet annuel legerement
plus court avec la meme flotte.

---

## Effet d'une liquidation finale

Si le PL autorise la vente des camions en fin d'annee 5, alors le solveur vendra
logiquement tous les camions restants, car il n'y a plus de demande apres
l'horizon.

Pour S3 et S4, la flotte finale est la meme :

```math
4 T1 + 6 T2
```

La valeur residuelle commune vaut :

```math
4 \times \frac{140000}{1,20^5}
+ 6 \times \frac{200000}{1,20^5}
\approx 707305 \text{ euros}
```

Donc :

| Proposition | Cout avant liquidation | Valeur finale | Cout apres liquidation |
|---|---:|---:|---:|
| P1 : S3 fixe | 6260455 | 707305 | 5553150 euros |
| P2 : choix optimal | 6251005 | 707305 | 5543700 euros |

La liquidation finale ne change pas le classement, car les deux propositions
gardent la meme flotte finale.

---

## Conclusion

Avec la formule complete du cout, la flotte **ne change pas au cours des 5 ans**
dans la meilleure solution trouvee. Acheter ou vendre des camions ne compense pas
la hausse du cout de trajet des autres scenarios.

La meilleure strategie est :

```text
garder 4 T1 + 6 T2 pendant les 5 ans
utiliser S4 si on accepte la planification annuelle de la base restante
sinon utiliser S3 comme meilleur scenario journalier strict
```

La devalorisation est bien prise en compte dans les ventes, mais elle ne pousse
pas le modele a vendre/racheter, car les scenarios avec changement de flotte ont
un trajet plus cher ou davantage de camions.
