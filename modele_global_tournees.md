# Option 2 - PLNE global par generation de tournees

## Objectif

Ce fichier decrit l'option 2 : au lieu de choisir uniquement entre les scenarios
S1, S2, S3 et S4, on construit une bibliotheque de tournees faisables et on
laisse un solveur choisir la meilleure combinaison de tournees, de camions,
d'achats et de ventes sur 5 ans.

Les fichiers precedents restent utiles :

- `test_annuel.md` fournit les tournees de depart, les temps, les distances et
  les controles de faisabilite ;
- `test_5an.md` donne une borne de comparaison : le cout de S4 est la meilleure
  solution parmi les 4 scenarios fixes ;
- le present modele cherche une solution potentiellement meilleure dans un
  espace de decisions plus large.

La structure suit les cours de RO presents dans `ressources` :

- variables de decision ;
- parametres ;
- fonction objectif ;
- contraintes ;
- domaines des variables.

Comme dans le labo PuLP/CBC, le probleme est formule comme une programmation
lineaire en nombres entiers.

---

## Idee generale

On genere un ensemble `R` de tournees candidates. Pour chaque tournee `r`, on
connait :

- le type de camion compatible ;
- la distance ;
- le temps ;
- les villes d'acide pouvant etre livrees ;
- la quantite maximale d'acide transportable ;
- la quantite maximale de base pouvant etre ramenee depuis Anvers.

Le solveur choisit ensuite :

```math
x_{r,t}
```

le nombre de fois que la tournee `r` est effectuee pendant l'annee `t`.

Il choisit aussi la flotte :

```math
N_{k,t},\ A_{k,t},\ V_{k,t}
```

c'est-a-dire le nombre de camions disponibles, achetes et vendus.

---

## Ensembles

```math
T=\{1,2,3,4,5\}
```

ensemble des annees.

```math
K=\{1,2\}
```

ensemble des types de camions.

```math
J=\{AN,CH,GA,BR,HA\}
```

ensemble des destinations acide.

```math
R
```

ensemble des tournees candidates.

---

## Parametres de demande

Demande annuelle de base :

```math
D^B_t = 30000
\qquad
\forall t \in T
```

Demandes annuelles d'acide :

```math
D^A_{AN,t}=9000
```

```math
D^A_{CH,t}=12000
```

```math
D^A_{GA,t}=2000
```

```math
D^A_{BR,t}=6200
```

Pour Hasselt :

```math
D^A_{HA,1}=350
```

```math
D^A_{HA,2}=825
```

```math
D^A_{HA,t}=1300
\qquad
t \in \{3,4,5\}
```

---

## Parametres de tournees

Pour chaque tournee candidate `r` :

```math
k(r) \in K
```

type de camion requis.

```math
d_r
```

distance d'une rotation.

```math
h_r
```

temps d'une rotation.

```math
cap^A_r
```

capacite acide maximale de la tournee.

```math
cap^B_r
```

capacite base maximale de la tournee.

```math
\delta_{r,j} =
\begin{cases}
1 & \text{si la tournee } r \text{ peut livrer de l'acide a } j \\
0 & \text{sinon}
\end{cases}
```

---

## Variables de decision

Nombre annuel de rotations :

```math
x_{r,t} \in \mathbb{Z}_+
\qquad
\forall r \in R,\ \forall t \in T
```

Quantite d'acide livree par une famille de tournees :

```math
q^A_{r,j,t} \ge 0
\qquad
\forall r \in R,\ \forall j \in J,\ \forall t \in T
```

Quantite de base ramenee :

```math
q^B_{r,t} \ge 0
\qquad
\forall r \in R,\ \forall t \in T
```

Flotte disponible :

```math
N_{k,t} \in \mathbb{Z}_+
\qquad
\forall k \in K,\ \forall t \in T
```

Achats :

```math
A_{k,t} \in \mathbb{Z}_+
\qquad
\forall k \in K,\ \forall t \in T
```

Ventes :

```math
V_{k,t} \in \mathbb{Z}_+
\qquad
\forall k \in K,\ \forall t \in T
```

Dans la version plus precise avec suivi des ages, on remplace `V_{k,t}` par
`V_{k,g,t}` comme dans `test_5an.md`. Le script associe utilise une version
simplifiee par annee pour rester lisible.

---

## Fonction objectif

On minimise le cout total sur 5 ans :

```math
\min Z =
\sum_{t \in T}
\left[
\sum_{k \in K} C^{achat}_k A_{k,t}
-
\sum_{k \in K} \frac{C^{achat}_k}{(1+\alpha)^t}V_{k,t}
+
5000\sum_{k \in K}N_{k,t}
+
78750\sum_{k \in K}N_{k,t}
+
0,60\sum_{r \in R}d_r x_{r,t}
\right]
```

avec :

```math
C^{achat}_1=140000
\qquad
C^{achat}_2=200000
\qquad
\alpha=0,20
```

Le terme `78750 N_{k,t}` correspond au cout chauffeur annuel d'un camion
mobilise :

```math
35 \times 9 \times 250 = 78750
```

Cette convention est coherente avec `cout.md`. Une variante plus fine pourrait
remplacer ce terme par :

```math
35\sum_{r \in R} h_r x_{r,t}
```

si on souhaite payer uniquement les heures effectivement utilisees.

---

## Contraintes de couverture

Chaque demande d'acide doit etre satisfaite exactement :

```math
\sum_{r \in R} q^A_{r,j,t}
=
D^A_{j,t}
\qquad
\forall j \in J,\ \forall t \in T
```

La demande de base doit etre satisfaite exactement :

```math
\sum_{r \in R} q^B_{r,t}
=
D^B_t
\qquad
\forall t \in T
```

---

## Contraintes de capacite des tournees

On ne peut livrer de l'acide a une ville que si la tournee passe par cette ville :

```math
q^A_{r,j,t}
\le
cap^A_r \delta_{r,j} x_{r,t}
\qquad
\forall r,j,t
```

La quantite totale d'acide d'une rotation ne peut pas depasser sa capacite :

```math
\sum_{j \in J}q^A_{r,j,t}
\le
cap^A_r x_{r,t}
\qquad
\forall r,t
```

La base ramenee est bornee par la capacite base de la tournee :

```math
q^B_{r,t}
\le
cap^B_r x_{r,t}
\qquad
\forall r,t
```

Ces contraintes remplacent le choix manuel des chargements dans `test_annuel.md`.

### Livraison minimale par arret

L'enonce impose une quantite minimale livree de 5 tonnes. Pour les tournees
candidates retenues dans le script, une tournee qui passe par une ville d'acide
livre cette ville a chaque rotation. On ajoute donc :

```math
q^A_{r,j,t}
\ge
5 \delta_{r,j} x_{r,t}
\qquad
\forall r,j,t
```

Cette contrainte empeche le solveur d'utiliser une tournee multi-villes pour
livrer seulement quelques centaines de kilos dans une ville. Si l'on voulait
autoriser qu'une tournee candidate passe parfois par une ville et parfois non,
il faudrait introduire une variable binaire supplementaire par ville et par
rotation-type.

---

## Contraintes de temps et de flotte

Le temps total de travail demande aux camions de type `k` ne peut pas depasser
leur disponibilite annuelle :

```math
\sum_{r \in R:\ k(r)=k} h_r x_{r,t}
\le
9 \times 250 \times N_{k,t}
\qquad
\forall k \in K,\ \forall t \in T
```

La flotte evolue avec les achats et les ventes.

Annee 1 :

```math
N_{1,1}=4+A_{1,1}-V_{1,1}
```

```math
N_{2,1}=6+A_{2,1}-V_{2,1}
```

Annees suivantes :

```math
N_{k,t}=N_{k,t-1}+A_{k,t}-V_{k,t}
\qquad
\forall k \in K,\ t \in \{2,3,4,5\}
```

On ne vend pas plus de camions que ceux disponibles avant vente :

```math
V_{1,1}\le 4
\qquad
V_{2,1}\le 6
```

```math
V_{k,t}\le N_{k,t-1}
\qquad
\forall k \in K,\ t \in \{2,3,4,5\}
```

---

## Changement d'affectation

L'enonce precise qu'un changement d'affectation prend 3 jours ouvrables. Dans ce
modele, il ne s'agit pas d'une simple affectation initiale, mais d'une conversion
acide/base ou base/acide d'un compartiment.

On peut ajouter :

```math
z_{c,t} =
\begin{cases}
1 & \text{si le compartiment } c \text{ change d'acide vers base ou inversement} \\
0 & \text{sinon}
\end{cases}
```

La contrainte de temps devient alors :

```math
\sum_{r \in R:\ k(r)=k} h_r x_{r,t}
\le
9 \left(250N_{k,t}-3\sum_{c \in C_k}z_{c,t}\right)
\qquad
\forall k,t
```

Dans le script associe, on garde des affectations stables et on pose :

```math
z_{c,t}=0
```

car aucun changement d'affectation n'est necessaire dans la solution S4 de
reference. Le mecanisme est neanmoins indique pour montrer comment l'ajouter.

---

## Domaine des variables

```math
x_{r,t},N_{k,t},A_{k,t},V_{k,t}\in\mathbb{Z}_+
```

```math
q^A_{r,j,t},q^B_{r,t}\ge 0
```

Le modele est donc une PLNE, car il combine :

- variables entieres de rotations et de flotte ;
- variables continues de quantites transportees ;
- objectif et contraintes lineaires.

---

## Lien avec les scenarios precedents

Les scenarios S1, S2, S3 et S4 deviennent des solutions candidates du modele.
Par exemple, S4 correspond a une combinaison particuliere de tournees :

- tournees acide hors Anvers ;
- tournees type 2 couplees Anvers/base ;
- rotations directes base restantes planifiees annuellement.

Le cout de S4 donne donc une borne superieure :

```math
Z^\star \le Z_{S4}
```

Si le solveur trouve une solution moins chere que S4, alors il a ameliore la
meilleure solution actuelle. S'il retrouve S4 ou une solution tres proche, cela
renforce la justification du scenario retenu.

---

## Script associe

Le script associe est :

```text
scripts/optimisation_tournees_pulp.py
```

Il implemente une version candidate de ce modele avec PuLP/CBC :

- generation manuelle d'une bibliotheque limitee de tournees faisables ;
- variables entieres de rotations ;
- variables continues de quantites transportees ;
- variables entieres de flotte, achats et ventes ;
- objectif achat - revente + entretien + chauffeur + kilometres ;
- contraintes de demande, capacite, temps et flotte.

Cette implementation est une base de travail : elle permet de tester l'option 2
et d'ajouter progressivement d'autres tournees candidates si l'on veut se
rapprocher davantage de l'optimum global.

---

## Resultat obtenu avec le script

Le script a ete execute avec PuLP/CBC dans un environnement virtuel local. Le
solveur retourne le statut :

```text
Optimal
```

Le cout total obtenu, sans liquidation finale, est :

```math
Z = 4413805 \text{ euros}
```

La flotte choisie est :

| Annee | T1 disponibles | T1 achetes | T1 vendus | T2 disponibles | T2 achetes | T2 vendus |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 0 | 1 | 4 | 0 | 2 |
| 2 | 3 | 0 | 0 | 4 | 0 | 0 |
| 3 | 3 | 0 | 0 | 4 | 0 | 0 |
| 4 | 3 | 0 | 0 | 4 | 0 | 0 |
| 5 | 3 | 0 | 0 | 4 | 0 | 0 |

La strategie trouvee est donc plus agressive que S4 : elle vend 1 camion type 1
et 2 camions type 2 en debut d'horizon, puis exploite fortement les 4 camions
type 2 restants sur les rotations Anvers/base.

La comparaison avec S4 est :

```math
6251005 - 4413805 = 1837200 \text{ euros}
```

Ce resultat ne signifie pas encore que l'on a prouve l'optimum absolu du probleme
reel. Il signifie :

```text
optimum de la bibliotheque de tournees generee = 4413805 euros
```

Pour transformer ce resultat en optimum global plus solide, il faudrait enrichir
la bibliotheque `R` avec toutes les tournees faisables raisonnables :

- autres combinaisons de deux villes ;
- autres combinaisons de trois villes ;
- variantes avec ou sans Anvers ;
- variantes type 1 et type 2 ;
- suivi plus precis des ages de camions dans la revente ;
- variables de changement d'affectation si on autorise des conversions.

Dans le rapport, la formulation prudente est donc :

```text
Le PLNE global par bibliotheque de tournees ameliore la meilleure solution S4
dans l'ensemble de tournees teste. Il fournit une meilleure borne superieure,
mais l'optimalite globale depend de l'exhaustivite de la bibliotheque de
tournees candidates.
```
