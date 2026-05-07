# Test journalier - acide, camions type 1, 9 h/jour, rechargement 0,5 h

## Cadre du test

Ce test concerne uniquement le transport d'acide au départ de Liège avec des camions de type 1.
Hasselt est exclue.

Hypothèses testées :

- camion type 1 uniquement ;
- capacité d'un camion type 1 : 16,5 t ;
- durée maximale de travail : 9 h par camion et par jour ;
- vitesse moyenne : 70 km/h ;
- durée d'un arrêt de livraison : 1 h par ville livrée ;
- quantité minimale livrée lors d'un arrêt : 5 t ;
- rechargement à Liège : 0,5 h uniquement si le camion revient à Liège et repart pour une deuxième tournée dans la même journée ;
- le premier chargement de la journée est supposé fait avant le départ ou intégré dans l'organisation initiale.

## Demande journalière

On travaille sur 250 jours ouvrables par an.

| Ville | Demande annuelle (t/an) | Demande journalière (t/j) |
|---|---:|---:|
| Anvers | 9000 | 36 |
| Charleroi | 12000 | 48 |
| Gand | 2000 | 8 |
| Bruxelles | 6200 | 24,8 |
| **Total hors Hasselt** | **29200** | **116,8** |

La demande journalière totale à couvrir est donc :

```text
116,8 t/jour
```

## Méthode de recherche opérationnelle utilisée

### 1. Représentation par un graphe pondéré

On modélise le réseau de villes par un graphe complet non orienté :

```text
G = (V, E)
```

avec :

- `V = {LI, AN, CH, GA, BR}` ;
- `LI` est le dépôt ;
- les autres sommets sont les villes clientes ;
- chaque arête `(i,j)` porte un poids `d_ij`, égal à la distance routière donnée dans l'énoncé.

Le temps de déplacement sur une arête est :

```text
t_ij = d_ij / 70
```

Cette partie relève de la théorie des graphes : une tournée est un cycle partant du dépôt, passant par un sous-ensemble de clients, puis revenant au dépôt.

### 2. Énumération des tournées candidates

Comme la quantité minimale livrée est 5 t et que la capacité du camion est 16,5 t, une tournée ne peut pas desservir 4 villes :

```text
4 x 5 = 20 t > 16,5 t
```

Il suffit donc de tester les tournées desservant 1, 2 ou 3 villes.

Pour chaque sous-ensemble de villes, on teste tous les ordres possibles et on garde l'ordre de distance minimale.
Cela correspond à un petit problème de voyageur de commerce sur sous-ensemble de clients.

Le temps d'une tournée `r` est :

```text
T_r = distance_r / 70 + nombre_arrets_r
```

### 3. Construction des journées de camion

Une journée de camion peut contenir :

- une seule tournée ;
- ou deux tournées, si le camion revient à Liège, recharge pendant 0,5 h, puis repart.

Pour deux tournées `r1` et `r2`, la contrainte de temps est :

```text
T_r1 + 0,5 + T_r2 <= 9
```

Trois tournées sont impossibles dans ce scénario, car les tournées les plus courtes durent déjà 3,857 h :

```text
3 x 3,857 + 2 x 0,5 = 12,571 h > 9 h
```

### 4. Sélection des tournées

Après avoir généré toutes les journées faisables, le problème devient un problème de sélection de tournées, proche d'un problème de couverture avec capacités.

Pour un nombre donné de camions `m`, on cherche à maximiser la quantité livrée :

```text
max somme(q_p,r,j)
```

sous contraintes :

```text
nombre de journées sélectionnées <= m
```

```text
somme des quantités d'une tournée <= 16,5
```

```text
quantité livrée à une ville <= demande journalière de cette ville
```

```text
si une ville est servie pendant une tournée, quantité livrée >= 5
```

Une fois le premier nombre de camions qui couvre toute la demande trouvé, on garde parmi les solutions faisables celle qui minimise la distance totale.

## Tournées candidates faisables

| # | Tournée minimale | Distance (km) | Temps sans rechargement (h) |
|---:|---|---:|---:|
| 1 | LI -> BR -> LI | 200 | 3,857 |
| 2 | LI -> CH -> LI | 200 | 3,857 |
| 3 | LI -> AN -> LI | 210 | 4,000 |
| 4 | LI -> GA -> LI | 280 | 5,000 |
| 5 | LI -> AN -> BR -> LI | 250 | 5,571 |
| 6 | LI -> BR -> CH -> LI | 260 | 5,714 |
| 7 | LI -> BR -> GA -> LI | 280 | 6,000 |
| 8 | LI -> AN -> GA -> LI | 285 | 6,071 |
| 9 | LI -> AN -> CH -> LI | 305 | 6,357 |
| 10 | LI -> CH -> GA -> LI | 340 | 6,857 |
| 11 | LI -> AN -> GA -> BR -> LI | 285 | 7,071 |
| 12 | LI -> AN -> BR -> CH -> LI | 310 | 7,429 |
| 13 | LI -> BR -> GA -> CH -> LI | 340 | 7,857 |
| 14 | LI -> AN -> GA -> CH -> LI | 345 | 7,929 |

## Doubles tournées possibles avec rechargement

Avec 9 h de travail et 0,5 h de rechargement entre deux tournées, les seules doubles tournées possibles sont :

| Double tournée | Temps total avec rechargement (h) | Distance (km) |
|---|---:|---:|
| LI -> BR -> LI ; LI -> BR -> LI | 8,214 | 400 |
| LI -> BR -> LI ; LI -> CH -> LI | 8,214 | 400 |
| LI -> BR -> LI ; LI -> AN -> LI | 8,357 | 410 |
| LI -> CH -> LI ; LI -> CH -> LI | 8,214 | 400 |
| LI -> CH -> LI ; LI -> AN -> LI | 8,357 | 410 |
| LI -> AN -> LI ; LI -> AN -> LI | 8,500 | 420 |

Exemple de calcul :

```text
LI -> BR -> LI ; rechargement ; LI -> AN -> LI
= (200/70 + 1) + 0,5 + (210/70 + 1)
= 3,857 + 0,5 + 4,000
= 8,357 h
```

Les tournées passant par Gand sont trop longues pour être combinées avec une deuxième tournée dans une journée de 9 h.

## Incrémentation du nombre de camions

| Nombre de camions type 1 | Quantité maximale livrée (t/j) | Demande restante (t/j) | Conclusion |
|---:|---:|---:|---|
| 1 | 33,0 | 83,8 | insuffisant |
| 2 | 66,0 | 50,8 | insuffisant |
| 3 | 97,5 | 19,3 | insuffisant |
| 4 | 113,8 | 3,0 | insuffisant |
| 5 | 116,8 | 0,0 | demande couverte |

Le nombre minimal de camions type 1 nécessaires est donc :

```text
5 camions
```

## Pourquoi 4 camions restent insuffisants

Même avec 9 h par jour, 4 camions ne suffisent pas.

La meilleure quantité livrable avec 4 camions est :

```text
113,8 t/jour
```

Il manque donc :

```text
116,8 - 113,8 = 3 t/jour
```

La difficulté vient de la ville de Gand.
Gand a une petite demande journalière, 8 t/jour, mais elle impose une tournée longue.
La tournée simple Liège-Gand-Liège prend déjà :

```text
280/70 + 1 = 5 h
```

et une tournée efficace incluant Gand et Anvers prend :

```text
LI -> AN -> GA -> LI = 285/70 + 2 = 6,071 h
```

Ces tournées ne peuvent pas être combinées avec une deuxième tournée dans la même journée lorsqu'on ajoute le rechargement.

## Planning minimal retenu avec 5 camions

Parmi les solutions qui couvrent exactement la demande journalière, le planning ci-dessous minimise la distance totale.

Distance totale :

```text
1705 km/jour
```

Temps total utilisé :

```text
34,857 h de camion par jour sur 45 h disponibles
```

| Camion | Tournées | Quantités livrées | Temps total (h) | Distance (km) |
|---:|---|---|---:|---:|
| 1 | LI -> BR -> LI | BR = 16,5 t | 3,857 | 200 |
| 2 | LI -> BR -> LI ; rechargement ; LI -> AN -> LI | BR = 8,3 t ; AN = 16,5 t | 8,357 | 410 |
| 3 | LI -> CH -> LI ; rechargement ; LI -> CH -> LI | CH = 16,5 t ; CH = 16,5 t | 8,214 | 400 |
| 4 | LI -> CH -> LI ; rechargement ; LI -> AN -> LI | CH = 15 t ; AN = 11 t | 8,357 | 410 |
| 5 | LI -> AN -> GA -> LI | AN = 8,5 t ; GA = 8 t | 6,071 | 285 |

## Vérification des demandes

| Ville | Demande journalière (t/j) | Quantité livrée (t/j) | Écart |
|---|---:|---:|---:|
| Anvers | 36 | 36 | 0 |
| Charleroi | 48 | 48 | 0 |
| Gand | 8 | 8 | 0 |
| Bruxelles | 24,8 | 24,8 | 0 |
| **Total** | **116,8** | **116,8** | **0** |

## Conclusion

Avec des journées de 9 h et un rechargement de 0,5 h uniquement lorsqu'un camion effectue une deuxième tournée, le nombre minimal de camions type 1 nécessaires pour couvrir la demande journalière d'acide hors Hasselt est :

```text
5 camions type 1
```

Ce scénario est plus réaliste que le scénario sans rechargement, car il tient compte du retour à Liège entre deux tournées.
Il reste toutefois moins conservateur qu'un scénario à 8 h avec rechargement, dans lequel les doubles tournées deviennent beaucoup plus difficiles à faire.
