# Test 5 ans - modele PLNE et comparaison des 4 scenarios

## Supports de cours utilises

Les documents dans `ressources` sont lisibles. Les supports pris en compte sont :

- `cours_PLP1.pdf` : formulation d'un programme mathematique avec variables de
  decision, parametres, objectif, contraintes et domaines des variables ;
- `cours_PL_2.pdf` : rappel du role du simplexe sur les programmes lineaires
  continus ;
- `labo_bin_packing.pdf` : utilisation de PuLP/CBC pour resoudre des programmes
  lineaires en variables entieres ;
- `flowshop.pdf` : rappel de l'analyse multi-objectif et des solutions de
  Pareto, utile comme extension possible mais non utilisee ici comme objectif
  principal ;
- `enonce_projet.pdf` : donnees de flotte, demandes, distances, couts et
  changement d'affectation.

La formulation ci-dessous suit donc la structure du cours : variables de
decision, parametres, fonction objectif, contraintes, puis domaines.

---

## Objectif du fichier

On veut comparer les 4 scenarios construits dans `test_annuel.md` sur l'horizon
des 5 prochaines annees.

Contrairement a une simple comparaison de tableaux, on formule ici le choix du
scenario comme un programme lineaire en nombres entiers :

```math
\min Z
```

Le solveur choisit le scenario qui minimise le cout total sur 5 ans.

Les 4 scenarios restent :

| Scenario | Description courte |
|---|---|
| S1 | Anvers reste dans les tournees acide |
| S2 | Anvers est retire des tournees acide |
| S3 | hybride journalier strict |
| S4 | hybride annuel avec affectation stable |

---

## Donnees economiques

| Parametre | Valeur |
|---|---:|
| Achat T1 | 140000 euros |
| Achat T2 | 200000 euros |
| Entretien | 5000 euros/camion/an |
| Cout kilometrique | 0,60 euros/km |
| Cout chauffeur | 35 euros/h |
| Temps de travail | 9 h/jour/camion |
| Jours ouvrables | 250 jours/an |
| Taux de devalorisation `alpha` | 0,20 |

Le cout chauffeur annuel d'un camion utilise toute l'annee est :

```math
C^{chauffeur}
= 35 \times 9 \times 250
= 78750
```

La recette de vente d'un camion de type `k`, de prix d'achat `C_k`, vendu a
l'age `n`, est :

```math
R_{k,n} = \frac{C_k}{(1+\alpha)^n}
```

Avec `alpha = 0,20`, un camion type 2 vendu apres 1 an rapporte :

```math
R_{2,1}
= \frac{200000}{1,20}
= 166666,67
```

---

## Donnees des scenarios

On reprend les distances obtenues dans `test_annuel.md`.

| Annee | S1 | S2 | S3 | S4 |
|---:|---:|---:|---:|---:|
| 1 | 3181,4 km/j | 2793,6 km/j | 2761,4 km/j | 2748,8 km/j |
| 2 | 3183,3 km/j | 2839,2 km/j | 2763,3 km/j | 2750,7 km/j |
| 3 | 3185 km/j | 2880 km/j | 2765 km/j | 2752,4 km/j |
| 4 | 3185 km/j | 2880 km/j | 2765 km/j | 2752,4 km/j |
| 5 | 3185 km/j | 2880 km/j | 2765 km/j | 2752,4 km/j |

Les flottes necessaires par scenario sont :

| Scenario | `q_{1,s}` T1 | `q_{2,s}` T2 | Total |
|---|---:|---:|---:|
| S1 | 7 | 3 | 10 |
| S2 | 4 | 7 | 11 |
| S3 | 4 | 6 | 10 |
| S4 | 4 | 6 | 10 |

La flotte initiale est :

```math
N^0_1 = 4
\qquad
N^0_2 = 6
```

Le cout initial de changement de flotte, calcule avec la formule de revente, est :

| Scenario | Achats | Ventes | Cout net initial `I_s` |
|---|---:|---:|---:|
| S1 | 3 T1 = 420000 | 3 T2 = 500000 | -80000 euros |
| S2 | 1 T2 = 200000 | 0 | 200000 euros |
| S3 | 0 | 0 | 0 euro |
| S4 | 0 | 0 | 0 euro |

---

## Modele PLNE 1 - choix du meilleur scenario fixe

Ce premier modele garde la meme organisation pendant les 5 ans. Il correspond a
la comparaison principale du rapport.

### Ensembles

```math
S = \{1,2,3,4\}
```

ensemble des scenarios.

```math
T = \{1,2,3,4,5\}
```

ensemble des annees.

```math
K = \{1,2\}
```

ensemble des types de camions.

### Parametres

```math
D_{s,t}
```

distance journaliere du scenario `s` pendant l'annee `t`.

```math
q_{k,s}
```

nombre de camions de type `k` necessaires dans le scenario `s`.

```math
I_s
```

cout initial de changement de flotte pour passer de la flotte actuelle au
scenario `s`.

```math
c^{km}=0,60
\qquad
c^{ent}=5000
\qquad
c^{chauffeur}=78750
```

### Variables de decision

```math
y_s =
\begin{cases}
1 & \text{si le scenario } s \text{ est choisi} \\
0 & \text{sinon}
\end{cases}
```

### Fonction objectif sans vente finale

On minimise le cout total sur 5 ans :

```math
\min Z_A
=
\sum_{s \in S} y_s
\left[
I_s
+
\sum_{t \in T}
\left(
5000 \sum_{k \in K} q_{k,s}
+
78750 \sum_{k \in K} q_{k,s}
+
0,60 \times 250 \times D_{s,t}
\right)
\right]
```

Cette fonction est lineaire, car les valeurs `I_s`, `q_{k,s}` et `D_{s,t}` sont
des parametres.

### Contrainte de choix unique

Un seul scenario est retenu :

```math
\sum_{s \in S} y_s = 1
```

### Domaine des variables

```math
y_s \in \{0,1\}
\qquad
\forall s \in S
```

Il s'agit donc d'une programmation lineaire en variables binaires.

---

## Calcul des couts annuels

Pour chaque scenario `s` et chaque annee `t`, le cout annuel est :

```math
C^{annuel}_{s,t}
=
C^{entretien}_{s}
+
C^{chauffeur}_{s}
+
C^{km}_{s,t}
```

avec :

```math
C^{entretien}_{s}
= 5000(q_{1,s}+q_{2,s})
```

```math
C^{chauffeur}_{s}
= 78750(q_{1,s}+q_{2,s})
```

```math
C^{km}_{s,t}
= 0,60 \times 250 \times D_{s,t}
```

| Annee | S1 | S2 | S3 | S4 |
|---:|---:|---:|---:|---:|
| 1 | 1314710 euros | 1340290 euros | 1251710 euros | 1249820 euros |
| 2 | 1314995 euros | 1347130 euros | 1251995 euros | 1250105 euros |
| 3 | 1315250 euros | 1353250 euros | 1252250 euros | 1250360 euros |
| 4 | 1315250 euros | 1353250 euros | 1252250 euros | 1250360 euros |
| 5 | 1315250 euros | 1353250 euros | 1252250 euros | 1250360 euros |

---

## Resolution du modele 1 - sans vente finale

Les coefficients de la fonction objectif sont :

```math
Z_{A,1} = -80000 + 6575455 = 6495455
```

```math
Z_{A,2} = 200000 + 6747170 = 6947170
```

```math
Z_{A,3} = 0 + 6260455 = 6260455
```

```math
Z_{A,4} = 0 + 6251005 = 6251005
```

La solution optimale du PLNE est donc :

```math
y_1=0
\qquad
y_2=0
\qquad
y_3=0
\qquad
y_4=1
```

et :

```math
Z_A^\star = 6251005
```

Le scenario optimal sans vente finale est donc `S4`.

---

## Modele avec vente finale

Si l'on considere que le projet s'arrete apres 5 ans, on revend la flotte
restante en fin d'horizon.

La valeur finale du scenario `s` est :

```math
R^{final}_s
=
\frac{140000q_{1,s}+200000q_{2,s}}{1,20^5}
```

La nouvelle fonction objectif devient :

```math
\min Z_B
=
\sum_{s \in S} y_s
\left[
I_s
+
\sum_{t \in T}
\left(
5000 \sum_{k \in K} q_{k,s}
+
78750 \sum_{k \in K} q_{k,s}
+
0,60 \times 250 \times D_{s,t}
\right)
-
R^{final}_s
\right]
```

La contrainte de choix reste :

```math
\sum_{s \in S} y_s = 1
```

et :

```math
y_s \in \{0,1\}
```

Valeurs finales :

| Scenario | Flotte finale | Valeur finale |
|---|---:|---:|
| S1 | 7 T1 + 3 T2 | 634967 euros |
| S2 | 4 T1 + 7 T2 | 787680 euros |
| S3 | 4 T1 + 6 T2 | 707305 euros |
| S4 | 4 T1 + 6 T2 | 707305 euros |

Coefficients de l'objectif :

```math
Z_{B,1} = 6495455 - 634967 = 5860488
```

```math
Z_{B,2} = 6947170 - 787680 = 6159490
```

```math
Z_{B,3} = 6260455 - 707305 = 5553150
```

```math
Z_{B,4} = 6251005 - 707305 = 5543700
```

La solution optimale reste :

```math
y_1=0
\qquad
y_2=0
\qquad
y_3=0
\qquad
y_4=1
```

et :

```math
Z_B^\star = 5543700
```

La vente finale ne change donc pas le choix optimal.

---

## Changement d'affectation dans le modele

L'enonce dit que changer l'affectation d'un compartiment prend 3 jours ouvrables.
Il ne faut pas confondre :

- affecter directement un camion a une mission au debut de l'annee ;
- convertir un compartiment qui etait acide pour qu'il devienne base, ou
  inversement.

On note :

```math
a_{c,t} \in \{A,B\}
```

l'affectation du compartiment `c` pendant l'annee `t`.

La variable de changement vaut :

```math
z_{c,t} =
\begin{cases}
1 & \text{si } a_{c,t} \ne a_{c,t-1} \\
0 & \text{si } a_{c,t} = a_{c,t-1}
\end{cases}
```

La perte de disponibilite est :

```math
H^{perdu}_{t}
=
9 \times 3 \sum_c z_{c,t}
```

Pour S4, la base restante est assuree par un camion type 1 affecte aux bases de
facon stable. Il n'y a donc pas de conversion dans le cas principal :

```math
z_{c,t}=0
\qquad
\forall t \in T
```

et :

```math
\sum_{t=1}^{5} z_{c,t}=0
```

Le nombre de changements d'affectation dans les 4 scenarios fixes est donc :

| Scenario | Nombre de conversions acide/base sur 5 ans |
|---|---:|
| S1 | 0 |
| S2 | 0 |
| S3 | 0 |
| S4 | 0 |

S4 reste faisable sans conversion, car la base restante demande :

```math
x_{B,t}
=
\left\lceil \frac{8000}{16,5} \right\rceil
=485
```

rotations par an, soit :

```math
4,5x_{B,t}
=
4,5 \times 485
=
2182,5 \text{ h/an}
```

Le temps disponible d'un camion type 1 affecte stablement aux bases est :

```math
9 \times 250 = 2250 \text{ h/an}
```

Donc :

```math
2182,5 \le 2250
```

S4 n'a donc pas besoin des 3 jours d'immobilisation.

Si une conversion etait imposee, la contrainte deviendrait :

```math
4,5x_{B,t}
\le
9(250-3z_{c,t})
```

avec `z_{c,t}=1`, donc :

```math
2182,5 \le 2223
```

La solution resterait faisable, mais cette conversion n'est pas necessaire et
n'est donc pas retenue dans le cout principal.

---

## Modele PLNE 2 - extension avec achats et ventes par annee

Le modele precedent choisit un scenario fixe. Si l'on veut laisser le solveur
decider des achats et ventes chaque annee, on peut utiliser une formulation plus
generale.

### Ensembles supplementaires

```math
G = \{0,1,2,3,4,5\}
```

ensemble des ages possibles des camions pendant l'horizon.

### Variables supplementaires

```math
u_{s,t} =
\begin{cases}
1 & \text{si le scenario } s \text{ est utilise en annee } t \\
0 & \text{sinon}
\end{cases}
```

```math
P_{k,t} \in \mathbb{Z}_+
```

nombre de camions de type `k` achetes au debut de l'annee `t`.

```math
V_{k,g,t} \in \mathbb{Z}_+
```

nombre de camions de type `k`, d'age `g`, vendus au debut de l'annee `t`.

```math
B_{k,g,t} \in \mathbb{Z}_+
```

nombre de camions de type `k`, d'age `g`, disponibles pendant l'annee `t` apres
achats et ventes.

```math
\bar B_{k,g,t} \in \mathbb{Z}_+
```

nombre de camions de type `k`, d'age `g`, presents juste avant les decisions
d'achat et de vente de l'annee `t`.

### Contraintes de scenario annuel

Chaque annee, un seul scenario est choisi :

```math
\sum_{s \in S} u_{s,t} = 1
\qquad
\forall t \in T
```

La flotte disponible doit couvrir la flotte necessaire du scenario choisi :

```math
\sum_{g \in G} B_{k,g,t}
\ge
\sum_{s \in S} q_{k,s}u_{s,t}
\qquad
\forall k \in K,\ \forall t \in T
```

### Contraintes d'etat initial

On reprend la convention utilisee dans les calculs precedents : les camions
initiaux ont deja une valeur de revente correspondant a `n=1`.

```math
\bar B_{1,1,1}=4
```

```math
\bar B_{2,1,1}=6
```

```math
\bar B_{k,g,1}=0
\qquad
\text{pour les autres couples } (k,g)
```

Avant les achats d'une annee, aucun camion ne peut avoir un age nul :

```math
\bar B_{k,0,t}=0
\qquad
\forall k \in K,\ \forall t \in T
```

### Contraintes d'achat et de vente

On ne peut vendre que des camions presents :

```math
0 \le V_{k,g,t} \le \bar B_{k,g,t}
\qquad
\forall k,g,t
```

Les camions disponibles pendant l'annee sont ceux qui restent apres ventes, plus
les achats neufs :

```math
B_{k,0,t}=P_{k,t}
\qquad
\forall k,t
```

```math
B_{k,g,t}
=
\bar B_{k,g,t}-V_{k,g,t}
\qquad
\forall k,t,\ \forall g \ge 1
```

### Evolution des ages

Les camions conserves vieillissent d'un an :

```math
\bar B_{k,g+1,t+1}
=
B_{k,g,t}
\qquad
\forall k,\ \forall t \in \{1,2,3,4\},\ \forall g \in \{0,1,2,3,4\}
```

### Fonction objectif generale

Sans vente finale, le modele general minimise :

```math
\min Z
=
\sum_{t \in T}
\left[
\sum_{k \in K} C^{achat}_k P_{k,t}
-
\sum_{k \in K}\sum_{g \in G}
\frac{C^{achat}_k}{(1+\alpha)^g}V_{k,g,t}
+
5000 \sum_{k \in K}\sum_{g \in G} B_{k,g,t}
+
78750 \sum_{s \in S}\left(\sum_{k \in K}q_{k,s}\right)u_{s,t}
+
0,60 \times 250 \sum_{s \in S} D_{s,t}u_{s,t}
\right]
```

Cette fonction est lineaire, car les coefficients de revente

```math
\frac{C^{achat}_k}{(1+\alpha)^g}
```

sont des constantes connues.

Avec vente finale, on soustrait aussi la valeur des camions encore possedes en
fin d'annee 5. Comme un camion disponible pendant l'annee 5 avec l'age `g` est
revendu apres cette annee, son age de revente est `g+1` :

```math
Z^{liq}
=
Z
-
\sum_{k \in K}\sum_{g \in G}
\frac{C^{achat}_k}{(1+\alpha)^{g+1}}B_{k,g,5}
```

### Domaine des variables

```math
u_{s,t} \in \{0,1\}
```

```math
P_{k,t},V_{k,g,t},B_{k,g,t},\bar B_{k,g,t}
\in \mathbb{Z}_+
```

Ce modele est une PLNE. Il peut etre resolu avec PuLP/CBC comme dans le labo.

---

## Bilan numerique des 4 scenarios fixes

Le bilan numerique ci-dessous correspond au modele 1, c'est-a-dire au choix d'un
scenario fixe. Il reprend la convention simplifiee de `cout.md` : la valeur
finale d'un scenario fixe est calculee sur la flotte finale globale avec
`1,20^5`. Le modele 2 donne la formulation plus precise si l'on veut suivre les
achats, ventes et ages de chaque camion annee par annee dans un solveur.

### Sans vente finale

| Scenario | Cout initial | Somme couts annuels | Total 5 ans |
|---|---:|---:|---:|
| S1 | -80000 | 6575455 | 6495455 euros |
| S2 | 200000 | 6747170 | 6947170 euros |
| S3 | 0 | 6260455 | 6260455 euros |
| S4 | 0 | 6251005 | 6251005 euros |

Classement :

```text
1. S4 : 6251005 euros
2. S3 : 6260455 euros
3. S1 : 6495455 euros
4. S2 : 6947170 euros
```

### Avec vente finale

| Scenario | Total avant liquidation | Valeur finale | Total apres liquidation |
|---|---:|---:|---:|
| S1 | 6495455 | 634967 | 5860488 euros |
| S2 | 6947170 | 787680 | 6159490 euros |
| S3 | 6260455 | 707305 | 5553150 euros |
| S4 | 6251005 | 707305 | 5543700 euros |

Classement :

```text
1. S4 : 5543700 euros
2. S3 : 5553150 euros
3. S1 : 5860488 euros
4. S2 : 6159490 euros
```

---

## Interpretation

Le modele PLNE de choix de scenario selectionne `S4` dans les deux conventions.

S4 domine S3 sur le cout, car les deux scenarios utilisent la meme flotte
`4 T1 + 6 T2`, mais S4 parcourt moins de kilometres grace a la planification
annuelle des rotations restantes de base.

La difference sur 5 ans sans vente finale est :

```math
6260455 - 6251005 = 9450 \text{ euros}
```

S1 a un cout initial favorable, car la vente de 3 camions type 2 rapporte plus
que l'achat de 3 camions type 1. Mais cette economie initiale est absorbee par
les kilometres supplementaires.

S2 est penalise par l'achat d'un camion type 2 et par un cout annuel plus eleve.

---

## Conclusion

En formulation PLNE, la solution optimale parmi les 4 scenarios fixes est :

```math
y_4=1
```

donc :

```text
Scenario retenu : S4
Flotte : 4 T1 + 6 T2
Nombre de changements d'affectation sur 5 ans : 0
```

Le resultat est :

| Convention | Scenario optimal | Cout |
|---|---|---:|
| Sans vente finale | S4 | 6251005 euros |
| Avec vente finale | S4 | 5543700 euros |

Si le rapport doit rester sur une journee type stricte, alors S3 reste la
meilleure solution journaliere. Mais si l'on accepte une planification annuelle,
le modele lineaire en variables binaires choisit S4.
