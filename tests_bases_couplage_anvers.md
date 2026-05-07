# Test bases - couplage par Anvers

## Objectif

Comparer trois organisations journalieres du transport des bases, produites a
Anvers et livrees a Liege, en tenant compte du transport d'acide au depart de
Liege.

Ce document est la base operationnelle du modele principal. Les scenarios 1 et 2
sont conserves comme comparaisons ; le **scenario 3 hybride (S3)** est le
scenario retenu pour parametrer le modele strategique de flotte.

Demande journaliere de reference, en regime permanent :

| Produit | Demande |
|---|---:|
| Base AN -> LI | 120 t/j |
| Acide total | 122 t/j |

Demande acide detaillee :

| Ville | AN | CH | GA | BR | HA | Total |
|---|---:|---:|---:|---:|---:|---:|
| Acide (t/j) | 36 | 48 | 8 | 24,8 | 5,2 | 122 |

Cette ligne correspond au regime permanent, c'est-a-dire aux annees ou Hasselt
est a 1300 t/an. Comme l'enonce precise que la nouvelle unite demarre dans 18
mois, Hasselt doit etre traite par annee pour respecter la livraison minimale de
5 t.

## Traitement annuel de Hasselt

Demande annuelle retenue pour Hasselt :

```math
D^{HA}_1 = 350
```

```math
D^{HA}_2 = \frac{1}{2} \times 350 + \frac{1}{2} \times 1300 = 825
```

```math
D^{HA}_3 = D^{HA}_4 = D^{HA}_5 = 1300
```

Si on livrait tous les jours, les demandes moyennes seraient :

| Annee | Demande HA | Moyenne journaliere |
|---:|---:|---:|
| 1 | 350 t/an | 1,4 t/j |
| 2 | 825 t/an | 3,3 t/j |
| 3-5 | 1300 t/an | 5,2 t/j |

Or une livraison doit contenir au moins 5 t. On ne livre donc pas Hasselt tous
les jours en annees 1 et 2. On choisit plutot :

```math
n^{HA}_t = \left\lceil \frac{D^{HA}_t}{5} \right\rceil
```

| Annee | Demande HA | Nombre de livraisons | Quantite par livraison |
|---:|---:|---:|---:|
| 1 | 350 t | 70 | 5 t |
| 2 | 825 t | 165 | 5 t |
| 3-5 | 1300 t | 250 | 5,2 t |

Cette convention respecte :

```math
q^{HA}_{liv} \ge 5
```

et :

```math
\sum_{\ell=1}^{n^{HA}_t} q^{HA}_{\ell} = D^{HA}_t
```

## Donnees

| Donnee | Valeur |
|---|---:|
| Vitesse | 70 km/h |
| Temps de travail | 8 h/j/camion |
| Jours ouvrables | 250 jours/an |
| Livraison acide | 1 h/arret |
| Chargement base a Anvers | 0,5 h |
| Dechargement base a Liege | 1 h |
| Camion type 1 | 16,5 t |
| Camion type 2 | 16,5 t + 5,5 t |
| Quantite minimale livree | 5 t |
| Distance LI-AN-LI | 210 km |
| Distance LI-AN-HA-LI | 215 km |

Les tournees du scenario principal ne rajoutent pas explicitement 0,5 h de
rechargement a Liege entre deux tournees d'acide. Cette simplification est
assumee dans le modele principal ; la variante avec rechargement explicite est
traitee separement comme analyse de sensibilite.

## Equations communes

On utilise la logique classique des modeles de RO vus au cours : une tournee est
faisable si elle respecte une contrainte de temps, et une solution est faisable
si elle couvre les demandes.

Temps d'une tournee :

```math
T_r = d_r/70 + n^A_r + 0,5 n^{chargB}_r + n^{livB}_r
```

Contrainte de faisabilite :

```math
T_r \le 8
```

Couverture de la demande de bases :

```math
\sum_r q^B_r \ge 120
```

Couverture de la demande d'acide :

```math
\sum_r q^A_{r,j} = D^A_j
\quad \forall j \in \{AN, CH, GA, BR, HA\}
```

Contraintes de capacite :

```math
0 \le q^A_r \le 16,5
\qquad
0 \le q^B_r \le 16,5
```

Dans ce test, le couplage acide/base n'est pas libre sur tout le reseau. Il est
limite aux trajets impliquant Anvers et exploite les deux compartiments des
camions type 2. Pour un camion type 2 utilise dans ce cadre, le couplage autorise
est :

```math
q^A_r \le 16,5
\qquad
q^B_r \le 5,5
```

ou inversement :

```math
q^A_r \le 5,5
\qquad
q^B_r \le 16,5
```

Une rotation directe base seule dure :

```math
T_B = 105/70 + 0,5 + 105/70 + 1 = 4,5 h
```

Donc un camion direct base ne peut faire qu'une seule rotation :

```math
2T_B = 9 h > 8 h
```

Une rotation directe couplee acide-base vers Anvers dure :

```math
T_{AB} = 105/70 + 1 + 0,5 + 105/70 + 1 = 5,5 h
```

Donc :

```math
2T_{AB} = 11 h > 8 h
```

Chaque camion qui ramene de la base depuis Anvers ne fait donc qu'une seule
rotation par jour.

---

## Scenario 1 - Garder Anvers dans les tournees acide

Les tournees acide passant par Anvers deviennent des camions type 2 :

- grand compartiment : acide ;
- petit compartiment : base au retour.

### Faisabilite acide

| Bloc | Tournees | Type | Acide | Base | Distance |
|---|---|---|---:|---:|---:|
| CH | 2 x LI-CH-LI | T1 | 33 t | 0 | 400 km |
| CH/BR | LI-CH-LI + LI-BR-LI | T1 | 31,3 t | 0 | 400 km |
| AN | LI-AN-LI | T2 | 12,35 t | 5,5 t | 210 km |
| AN | LI-AN-LI | T2 | 12,35 t | 5,5 t | 210 km |
| AN/HA | LI-AN-HA-LI | T2 | 16,5 t | 5,5 t | 215 km |
| GA/BR | LI-GA-BR-LI | T1 | 16,5 t | 0 | 280 km |
| **Total** |  |  | **122 t** | **16,5 t** | **1715 km** |

Equation de couverture base :

```math
B_1 = 3 \times 5,5 + 6 \times 16,5 + 5 = 120,5
```

Il faut donc 7 camions type 1 directs pour les bases :

```math
\left\lceil \frac{120 - 16,5}{16,5} \right\rceil = 7
```

Distance :

```math
D_1 = 1715 + 7 \times 210 = 3185 \text{ km/j}
```

Bilan :

| Type 1 | Type 2 | Total camions | Base couverte | Distance |
|---:|---:|---:|---:|---:|
| 10 | 3 | 13 | 120,5 t/j | 3185 km/j |

---

## Scenario 2 - Retirer Anvers des tournees acide

L'acide vers Anvers est transporte uniquement par des camions type 2 directs :

- petit compartiment : acide vers Anvers ;
- grand compartiment : base vers Liege.

### Faisabilite acide

| Bloc | Tournees | Type | Acide | Base | Distance |
|---|---|---|---:|---:|---:|
| Acide hors AN-HA | CH, BR, GA | T1 | 80,8 t | 0 | 1080 km |
| AN direct | 7 x LI-AN-LI | T2 | 36 t | 115,5 t | 1470 km |
| Base restante + HA | LI-AN-LI + LI-HA-LI | T1 | 5,2 t | 5 t | 330 km |
| **Total** |  |  | **122 t** | **120,5 t** | **2880 km** |

Le dernier camion type 1 reste faisable en temps :

```math
T = (105/70 + 0,5 + 105/70 + 1) + (120/70 + 1)
```

```math
T = 4,5 + 2,714 = 7,214 h \le 8 h
```

Nombre de camions type 2 directs :

```math
\left\lceil \frac{36}{5,5} \right\rceil = 7
```

Couverture base :

```math
B_2 = 7 \times 16,5 + 5 = 120,5
```

Distance :

```math
D_2 = 1200 + 7 \times 210 + 210 = 2880 \text{ km/j}
```

Bilan :

| Type 1 | Type 2 | Total camions | Base couverte | Distance |
|---:|---:|---:|---:|---:|
| 4 | 7 | 11 | 120,5 t/j | 2880 km/j |

---

## Scenario 3 - Hybride retenu pour le modele principal

On garde une tournee mixte Anvers-Hasselt, puis on livre le reste de l'acide vers
Anvers par rotations directes type 2.

### Faisabilite acide

| Bloc | Tournees | Type | Acide | Base | Distance |
|---|---|---|---:|---:|---:|
| CH | 2 x LI-CH-LI | T1 | 33 t | 0 | 400 km |
| CH/BR | LI-CH-LI + LI-BR-LI | T1 | 31,3 t | 0 | 400 km |
| GA/BR | LI-GA-BR-LI | T1 | 16,5 t | 0 | 280 km |
| AN/HA | LI-AN-HA-LI | T2 | 16,2 t | 5,5 t | 215 km |
| AN direct | 5 x LI-AN-LI | T2 | 25 t | 82,5 t | 1050 km |
| Base restante | 2 x LI-AN-LI | T1 | 0 | 32 t | 420 km |
| **Total** |  |  | **122 t** | **120 t** | **2765 km** |

Details Anvers :

```math
q^A_{AN} = 11 + 5 \times 5 = 36
```

Couverture base :

```math
B_3 = 5,5 + 5 \times 16,5 + 32 = 120
```

Nombre de camions type 1 directs pour la base restante :

```math
\left\lceil \frac{32}{16,5} \right\rceil = 2
```

Distance :

```math
D_3 = 1295 + 5 \times 210 + 2 \times 210 = 2765 \text{ km/j}
```

Bilan :

| Type 1 | Type 2 | Total camions | Base couverte | Distance |
|---:|---:|---:|---:|---:|
| 5 | 6 | 11 | 120 t/j | 2765 km/j |

---

## Effet annuel de Hasselt sur les distances

Les bilans precedents utilisent la distance du regime permanent, ou Hasselt est
livre chaque jour ouvrable. Pour les annees 1 et 2, on corrige seulement les
distances, car les livraisons de Hasselt sont moins frequentes.

Dans les scenarios 1 et 3, Hasselt est integre a une tournee passant deja par
Anvers. Le surcout d'une livraison Hasselt est donc seulement :

```math
d_{AN,HA} + d_{HA,LI} - d_{AN,LI} = 50 + 60 - 105 = 5 \text{ km}
```

Distance annuelle de la partie Anvers-Hasselt :

```math
D^{ANHA}_t = 250 \times 210 + 5 n^{HA}_t
```

Dans le scenario 2, Hasselt est livre par une tournee separee ajoutee au camion
type 1 qui fait la base restante. Le surcout d'une livraison Hasselt est donc :

```math
d_{LI,HA} + d_{HA,LI} = 120 \text{ km}
```

Correction annuelle :

```math
D^{HA}_t = 120 n^{HA}_t
```

Distance moyenne journaliere corrigee :

| Annee | `n_HA` | Scenario 1 | Scenario 2 | Scenario 3 |
|---:|---:|---:|---:|---:|
| 1 | 70 | 3181,4 km/j | 2793,6 km/j | 2761,4 km/j |
| 2 | 165 | 3183,3 km/j | 2839,2 km/j | 2763,3 km/j |
| 3-5 | 250 | 3185 km/j | 2880 km/j | 2765 km/j |

Le classement en distance ne change pas : le scenario 3 reste le plus court
chaque annee. C'est donc ce scenario qui est retenu comme reference
operationnelle dans le modele principal.

---

## Cout de changement de flotte

Flotte initiale :

```math
N^0_1 = 4
\qquad
N^0_2 = 6
```

Prix :

```math
C_1 = 140000
\qquad
C_2 = 200000
```

Hypothese de revente moyenne en fin d'annee 1 :

```math
\alpha = 0,25
\qquad
t = 1
```

```math
\bar C^{vente}_{1,1} = \frac{140000}{1,25} = 112000
\qquad
\bar C^{vente}_{2,1} = \frac{200000}{1,25} = 160000
```

Formule de cout net :

```math
C^{net}_s =
140000 A_{1,s} + 200000 A_{2,s}
- 112000 R_{1,s} - 160000 R_{2,s}
```

avec :

```math
A_{k,s} = \max(0, N_{k,s} - N^0_k)
\qquad
R_{k,s} = \max(0, N^0_k - N_{k,s})
```

| Critere | Scenario 1 | Scenario 2 | Scenario 3 |
|---|---:|---:|---:|
| Flotte demandee T1 | 10 | 4 | 5 |
| Flotte demandee T2 | 3 | 7 | 6 |
| Achats T1 | 6 | 0 | 1 |
| Achats T2 | 0 | 1 | 0 |
| Reventes T1 | 0 | 0 | 0 |
| Reventes T2 | 3 | 0 | 0 |
| **Cout net** | **360000 euros** | **200000 euros** | **140000 euros** |

---

## Comparaison

| Critere | Scenario 1 | Scenario 2 | Scenario 3 | Meilleur |
|---|---:|---:|---:|---|
| Total camions | 13 | 11 | 11 | S2/S3 |
| Type 1 | 10 | 4 | 5 | S2 |
| Type 2 | 3 | 7 | 6 | S1 |
| Distance | 3185 | 2880 | 2765 | S3 |
| Base couverte | 120,5 | 120,5 | 120 | S3 |
| Cout net changement | 360000 | 200000 | 140000 | S3 |

## Justification d'optimalite du scenario 3 en distance dans le cadre du test

Une borne inferieure sur le nombre de rotations transportant des bases est :

```math
N_B \ge \left\lceil \frac{120}{16,5} \right\rceil = 8
```

Comme chaque rotation base prend au moins 4,5 h, un camion ne peut en faire
qu'une seule par jour. Il faut donc au moins 8 camions impliques dans le flux
base.

Le scenario 3 utilise exactement 8 rotations avec base :

```math
1 \text{ rotation AN-HA}
+ 5 \text{ rotations T2 directes}
+ 2 \text{ rotations T1 base}
= 8
```

Pour l'acide hors Anvers-Hasselt, les tournees CH, BR et GA necessitent au moins
les blocs suivants :

```math
3 \text{ passages vers CH}
\quad + \quad
1 \text{ passage vers BR}
\quad + \quad
1 \text{ passage vers GA-BR}
```

Le scenario 3 atteint cette structure avec 3 camions type 1 hors Anvers.

La distance minimale associee aux 8 rotations de base est :

```math
7 \times 210 + 215 = 1685 \text{ km}
```

La distance des tournees acide hors Anvers est :

```math
400 + 400 + 280 = 1080 \text{ km}
```

Donc une borne coherente avec les tournees retenues est :

```math
D \ge 1685 + 1080 = 2765 \text{ km/j}
```

Le scenario 3 atteint cette borne :

```math
D_3 = 2765 \text{ km/j}
```

Il est donc optimal en distance dans le cadre restreint des hypotheses retenues
pour ce test, et non dans un probleme de tournees general :

- une seule rotation base par camion et par jour ;
- demandes journalieres moyennes pour AN, CH, GA et BR ;
- Hasselt traite par nombre annuel de livraisons de minimum 5 t ;
- quantite minimale de 5 t par livraison ;
- tournees construites avec les distances de l'enonce ;
- couplage uniquement via les compartiments du type 2.

## Sensibilite et limites

Les points suivants ne modifient pas le scenario principal, mais doivent etre
signales dans le rapport :

- le rechargement a Liege entre deux tournees d'acide n'est pas ajoute
  explicitement dans S3 ;
- Hasselt est traite par nombre annuel de livraisons, ce qui moyenne la demande
  au sein de chaque annee ;
- le couplage acide/base reste limite a Anvers ;
- l'optimalite en distance vaut seulement pour les tournees candidates et les
  conventions de ce document ;
- les scenarios 1 et 2 restent des alternatives comparees, pas la base du modele
  principal.

## Choix selon le critere

| Cas | Scenario preferable | Raison |
|---|---|---|
| Minimiser le nombre total de camions | S2 ou S3 | 11 camions |
| Minimiser la distance | S3 | 2765 km/j |
| Minimiser le cout de changement | S3 | 140000 euros |
| Minimiser les camions type 2 | S1 | 3 camions type 2 |
| Garder une variante conservative | S1 | moins de dependance aux type 2 |

## Conclusion

Le scenario 3 est le meilleur compromis et le scenario retenu pour le PL de
flotte. Il est a egalite avec le scenario 2 sur le nombre total de camions, mais
il minimise la distance parcourue et le cout net de changement de flotte.

Le scenario 1 reste utile comme variante si le PL final penalise fortement les
camions type 2.
