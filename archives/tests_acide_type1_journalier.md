# Tests journaliers - acide uniquement, camions type 1, sans Hasselt

## Objectif du test

On veut dimensionner uniquement le transport journalier d'acide avec des camions de type 1.
Hasselt est complètement écartée du test.

La procédure suivie est :

1. commencer avec un seul camion type 1 ;
2. tester tous les trajets journaliers possibles respectant les contraintes ;
3. calculer la quantité maximale d'acide livrable ;
4. si la demande journalière totale est couverte, s'arrêter ;
5. sinon ajouter un camion et recommencer.

Quand le nombre minimal de camions est trouvé, on retient parmi les solutions faisables celle qui minimise la distance totale parcourue.

## Données utilisées

Données directement utilisées depuis l'énoncé :

- acide au départ de Liège ;
- villes considérées : Anvers, Charleroi, Gand, Bruxelles ;
- Hasselt exclue ;
- camion type 1 : 1 compartiment de 16,5 t ;
- quantité maximale transportable d'un même produit : 16,5 t ;
- vitesse moyenne : 70 km/h ;
- durée d'un arrêt de livraison : 1 h ;
- quantité minimale livrée à une ville lors d'un arrêt : 5 t.

Convention journalière :

- on prend 250 jours ouvrables par an ;
- cela correspond à 2000 h/an avec 8 h/jour.

La demande journalière d'acide hors Hasselt est donc :

| Ville | Demande annuelle (t/an) | Demande journalière (t/j) |
|---|---:|---:|
| Anvers | 9000 | 36 |
| Charleroi | 12000 | 48 |
| Gand | 2000 | 8 |
| Bruxelles | 6200 | 24,8 |
| **Total** | **29200** | **116,8** |

## Règles de faisabilité

Une tournée commence à Liège, passe par une ou plusieurs villes, puis revient à Liège.

Le temps d'une tournée est :

```text
temps = distance totale / 70 + nombre d'arrêts
```

Un camion peut faire plusieurs tournées dans la journée si la somme des temps ne dépasse pas 8 h.

Comme chaque arrêt doit livrer au moins 5 t et qu'un camion type 1 transporte au maximum 16,5 t, une tournée ne peut pas desservir plus de 3 villes :

```text
4 villes x 5 t = 20 t > 16,5 t
```

## Tournées faisables en une journée

Pour chaque ensemble de villes, l'ordre retenu ci-dessous est l'ordre le plus court.

| # | Tournée | Distance (km) | Temps (h) |
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

Un camion peut aussi combiner deux tournées dans la même journée si leur temps total est inférieur ou égal à 8 h.
Par exemple :

- LI -> BR -> LI puis LI -> CH -> LI : 7,714 h ;
- LI -> BR -> LI puis LI -> AN -> LI : 7,857 h ;
- LI -> CH -> LI puis LI -> AN -> LI : 7,857 h ;
- LI -> AN -> LI puis LI -> AN -> LI : 8,000 h.

Trois tournées dans la même journée sont impossibles, car les tournées les plus courtes durent 3,857 h chacune et :

```text
3 x 3,857 = 11,571 h > 8 h
```

## Résultat de l'incrémentation du nombre de camions

Le tableau suivant donne, pour chaque nombre de camions, la quantité maximale livrable en respectant les demandes journalières par ville.

| Nombre de camions type 1 | Quantité maximale livrée (t/j) | Demande restante (t/j) | Conclusion |
|---:|---:|---:|---|
| 1 | 33,0 | 83,8 | insuffisant |
| 2 | 66,0 | 50,8 | insuffisant |
| 3 | 97,5 | 19,3 | insuffisant |
| 4 | 113,8 | 3,0 | insuffisant |
| 5 | 116,8 | 0,0 | demande couverte |

Conclusion du test :

```text
Nombre minimal de camions type 1 nécessaires = 5
```

## Pourquoi 4 camions ne suffisent pas

Un camion peut transporter au maximum 33 t/j s'il effectue deux tournées complètes.
Une borne de capacité brute donne donc :

```text
ceil(116,8 / 33) = 4 camions
```

Mais cette borne ne tient pas compte de la géographie et de la répartition par ville.
Avec 4 camions, le meilleur test trouvé livre :

| Ville | Demandé (t/j) | Livré avec 4 camions (t/j) | Manque (t/j) |
|---|---:|---:|---:|
| Anvers | 36 | 33 | 3 |
| Charleroi | 48 | 48 | 0 |
| Gand | 8 | 8 | 0 |
| Bruxelles | 24,8 | 24,8 | 0 |
| **Total** | **116,8** | **113,8** | **3** |

Il manque donc encore 3 t/j pour Anvers. Ce manque ne peut pas être ajouté sans dépasser les 8 h d'un des camions ou modifier une tournée d'une manière qui réduit une autre livraison.

## Planning minimal retenu avec 5 camions

Parmi les solutions qui couvrent exactement les 116,8 t/j, le planning ci-dessous minimise la distance totale parcourue.

Distance totale :

```text
1705 km/jour
```

Temps total utilisé :

```text
33,357 h de camion par jour sur 40 h disponibles
```

| Camion | Tournées | Quantités livrées | Temps (h) | Distance (km) |
|---:|---|---|---:|---:|
| 1 | LI -> BR -> LI | BR = 16,5 t | 3,857 | 200 |
| 2 | LI -> BR -> LI ; LI -> AN -> LI | BR = 8,3 t ; AN = 16,5 t | 7,857 | 410 |
| 3 | LI -> CH -> LI ; LI -> CH -> LI | CH = 16,5 t ; CH = 16,5 t | 7,714 | 400 |
| 4 | LI -> CH -> LI ; LI -> AN -> LI | CH = 15 t ; AN = 11 t | 7,857 | 410 |
| 5 | LI -> AN -> GA -> LI | AN = 8,5 t ; GA = 8 t | 6,071 | 285 |

## Vérification finale par ville

| Ville | Demande journalière (t/j) | Quantité livrée (t/j) | Écart |
|---|---:|---:|---:|
| Anvers | 36 | 36 | 0 |
| Charleroi | 48 | 48 | 0 |
| Gand | 8 | 8 | 0 |
| Bruxelles | 24,8 | 24,8 | 0 |
| **Total** | **116,8** | **116,8** | **0** |

Toutes les contraintes testées sont respectées :

- chaque camion travaille au maximum 8 h/jour ;
- chaque tournée transporte au maximum 16,5 t ;
- chaque arrêt livre au moins 5 t ;
- Hasselt est exclue ;
- seuls les camions type 1 sont utilisés ;
- seule la demande d'acide est considérée.
