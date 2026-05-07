# Test bases - couplage par Anvers

## Objectif

Comparer quatre organisations du transport des bases, produites a Anvers et
livrees a Liege, en tenant compte du transport d'acide au depart de Liege.

Les scenarios 1, 2 et 3 sont des organisations journalieres. Le scenario 4 est
une variante annuelle qui reprend le scenario 3, mais raisonne sur les quantites
annuelles au lieu d'imposer exactement la meme journee type 250 fois.

Attention : d'apres l'enonce, un changement d'affectation signifie qu'un
compartiment qui transportait de l'acide est converti pour transporter de la
base, ou inversement. Les 3 jours ne sont donc comptes que si une telle
conversion a effectivement lieu.

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
| Temps de travail | 9 h/j/camion |
| Livraison acide | 1 h/arret |
| Chargement base a Anvers | 0,5 h |
| Dechargement base a Liege | 1 h |
| Camion type 1 | 16,5 t |
| Camion type 2 | 16,5 t + 5,5 t |
| Quantite minimale livree | 5 t |
| Distance LI-AN-LI | 210 km |
| Distance LI-AN-HA-LI | 215 km |

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
T_r \le 9
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

Pour un camion type 2, le couplage autorise est :

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

Donc un camion direct base peut faire exactement deux rotations si toute sa
journee est consacree aux bases :

```math
2T_B = 9 h \le 9 h
```

Une rotation directe couplee acide-base vers Anvers dure :

```math
T_{AB} = 105/70 + 1 + 0,5 + 105/70 + 1 = 5,5 h
```

Donc une rotation couplee acide-base reste limitee a une seule rotation par
jour :

```math
2T_{AB} = 11 h > 9 h
```

Chaque camion qui ramene de la base depuis Anvers en etant couple a une livraison
d'acide ne fait donc qu'une seule rotation par jour. En revanche, un camion
dedie uniquement a la base peut faire deux rotations directes par jour.

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

Il faut donc 7 rotations type 1 directes pour les bases :

```math
\left\lceil \frac{120 - 16,5}{16,5} \right\rceil = 7
```

Avec 9 h/jour, un camion type 1 direct peut effectuer deux rotations LI-AN-LI :

```math
2T_B = 9 h
```

Le nombre de camions type 1 directs pour les bases est donc :

```math
\left\lceil \frac{7}{2} \right\rceil = 4
```

Distance :

```math
D_1 = 1715 + 7 \times 210 = 3185 \text{ km/j}
```

Bilan :

| Type 1 | Type 2 | Total camions | Base couverte | Distance |
|---:|---:|---:|---:|---:|
| 7 | 3 | 10 | 120,5 t/j | 3185 km/j |

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
T = 4,5 + 2,714 = 7,214 h \le 9 h
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

## Scenario 3 - Variante hybride

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

Nombre de rotations type 1 directes pour la base restante :

```math
\left\lceil \frac{32}{16,5} \right\rceil = 2
```

Avec 9 h/jour, ces deux rotations directes peuvent etre faites par un seul camion
type 1 :

```math
2T_B = 9 h
```

Distance :

```math
D_3 = 1295 + 5 \times 210 + 2 \times 210 = 2765 \text{ km/j}
```

Bilan :

| Type 1 | Type 2 | Total camions | Base couverte | Distance |
|---:|---:|---:|---:|---:|
| 4 | 6 | 10 | 120 t/j | 2765 km/j |

---

## Scenario 4 - Systeme annuel avec affectation stable

Ce scenario reprend la logique du scenario 3, mais exploite une difference de
modelisation :

- au lieu d'imposer 2 rotations de base restante tous les jours, on couvre la
  base restante sur l'annee avec le nombre minimal de rotations.

L'idee est de garder les 6 camions type 2 pour le couplage par Anvers, comme
dans le scenario 3, et de traiter la base restante avec 1 seul camion type 1.
Ce camion peut faire deux rotations base directes par jour, mais on planifie le
nombre exact de rotations sur l'annee au lieu d'imposer deux rotations chaque
jour.

Dans le scenario retenu, l'affectation est stable sur l'annee :

```math
m_B = 0
```

Il n'y a donc pas de 3 jours d'immobilisation dans S4 si le camion type 1 est
affecte aux bases des le debut de l'annee.

Si, au contraire, on partait explicitement d'un compartiment affecte a l'acide et
qu'on le convertissait vers la base, alors il faudrait prendre `m_B = 1` et
retirer 3 jours de disponibilite. Cette variante est indiquee plus bas comme test
de sensibilite.

### Notation du petit PL annuel

On isole uniquement la partie "base restante" du scenario 3.

Parametres :

```math
J = 250
\qquad
H = 9
\qquad
\tau = 3
```

```math
Q = 16,5
\qquad
d_B = 210
\qquad
T_B = 4,5
```

avec :

- `J` : nombre de jours ouvrables par an ;
- `H` : nombre d'heures de travail par jour ;
- `tau` : immobilisation en jours ouvrables si changement d'affectation ;
- `Q` : quantite maximale de base transportee par rotation ;
- `d_B` : distance d'une rotation directe LI-AN-LI ;
- `T_B` : temps d'une rotation directe LI-AN-LI.

Variables :

```math
x_B \in \mathbb{Z}_+
```

nombre de rotations annuelles directes LI-AN-LI dediees a la base restante.

```math
y_B \in \{0,1\}
```

vaut 1 si un camion type 1 est affecte a cette base restante.

```math
m_B \in \mathbb{Z}_+
```

nombre de conversions acide/base ou base/acide du compartiment du camion dedie
aux bases.

### Demande annuelle de base restante

Dans le scenario 3, les camions type 2 couvrent :

```math
B^{T2} = 250 \times (5,5 + 5 \times 16,5)
```

```math
B^{T2} = 250 \times 88 = 22000 \text{ t/an}
```

La demande annuelle totale de base vaut :

```math
D^B = 30000 \text{ t/an}
```

La base restante vaut donc :

```math
D^{B,rest} = D^B - B^{T2}
```

```math
D^{B,rest} = 30000 - 22000 = 8000 \text{ t/an}
```

### Contraintes

Couverture de la demande :

```math
Q x_B \ge D^{B,rest}
```

c'est-a-dire :

```math
16,5 x_B \ge 8000
```

Temps disponible :

```math
T_B x_B \le H(Jy_B - \tau m_B)
```

c'est-a-dire :

```math
4,5 x_B \le 9(250y_B - 3m_B)
```

Lien logique : si le camion n'est pas affecte a la base restante, aucune rotation
de base restante n'est possible. Avec un grand `M` :

```math
x_B \le M y_B
```

Si on veut aussi limiter explicitement les changements d'affectation au camion
utilise, on peut ajouter :

```math
m_B \le M y_B
```

Pour tester le systeme principal avec un seul camion type 1 affecte aux bases
des le debut de l'annee :

```math
y_B = 1
\qquad
m_B = 0
```

### Verification numerique

Nombre minimal de rotations :

```math
x_B^{min} =
\left\lceil \frac{8000}{16,5} \right\rceil
= 485
```

Temps necessaire :

```math
485 \times 4,5 = 2182,5 \text{ h/an}
```

Temps disponible sans changement d'affectation :

```math
9 \times 250 = 2250 \text{ h/an}
```

Donc :

```math
2182,5 \le 2250
```

Le systeme est faisable sans changement d'affectation, car l'affectation base est
choisie directement pour l'annee.

### Sensibilite si une conversion est imposee

Si le camion type 1 utilise pour la base restante etait initialement affecte a
l'acide, il faudrait convertir son compartiment :

```math
m_B = 1
```

Le temps disponible deviendrait :

```math
9 \times (250 - 3) = 2223 \text{ h/an}
```

La faisabilite resterait verifiee :

```math
2182,5 \le 2223
```

Si on imposait plusieurs conversions dans la meme annee, il faudrait remplacer
`3` par `3m_B` dans le calcul de disponibilite :

```math
H^{disp} = 9(250 - 3m_B)
```

### Distance de la base restante

```math
D^{B,rest}_4 = d_B x_B = 210 \times 485
```

```math
D^{B,rest}_4 = 101850 \text{ km/an}
```

Dans le scenario 3 journalier, la meme partie etait approximee par deux rotations
par jour :

```math
D^{B,rest}_3 = 250 \times 2 \times 210 = 105000 \text{ km/an}
```

Le passage a un calcul annuel evite donc quelques rotations partiellement
chargees :

```math
105000 - 101850 = 3150 \text{ km/an}
```

### Bilan du scenario 4

La flotte utilisee est la flotte initiale :

```math
N_1 = 4
\qquad
N_2 = 6
```

Elle se decompose ainsi :

| Bloc | Type | Nombre de camions | Role |
|---|---:|---:|---|
| Acide CH/BR/GA | T1 | 3 | tournees acide hors Anvers-Hasselt |
| Base restante | T1 | 1 | deux rotations LI-AN-LI par jour disponible |
| Couplage Anvers | T2 | 6 | acide vers Anvers et base au retour |
| **Total** |  | **10** | flotte initiale |

Le cout de changement de flotte est nul :

```math
A_1 = A_2 = R_1 = R_2 = 0
```

```math
C^{changement}_4 = 0
```

La distance annuelle du scenario 4 est obtenue en partant de la distance annuelle
du scenario 3 et en remplacant les `105000 km/an` de base restante par
`101850 km/an` :

```math
D^{annuel}_{4,t}
= 250D_{3,t} - 105000 + 101850
```

| Annee | Distance annuelle S4 | Distance moyenne S4 |
|---:|---:|---:|
| 1 | 687200 km/an | 2748,8 km/j |
| 2 | 687675 km/an | 2750,7 km/j |
| 3-5 | 688100 km/an | 2752,4 km/j |

Ce scenario est donc meilleur que le scenario 3 si on accepte :

- une lecture annuelle de la demande de base restante ;
- un camion type 1 affecte de facon stable aux bases ;
- l'absence de contrainte imposant exactement deux rotations de base tous les
  jours.

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

| Annee | `n_HA` | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 |
|---:|---:|---:|---:|---:|---:|
| 1 | 70 | 3181,4 km/j | 2793,6 km/j | 2761,4 km/j | 2748,8 km/j |
| 2 | 165 | 3183,3 km/j | 2839,2 km/j | 2763,3 km/j | 2750,7 km/j |
| 3-5 | 250 | 3185 km/j | 2880 km/j | 2765 km/j | 2752,4 km/j |

Le classement entre les trois scenarios journaliers ne change pas : le scenario
3 reste le plus court parmi S1, S2 et S3. Le scenario 4 devient plus court si on
autorise le raisonnement annuel pour la base restante. Les 3 jours
d'immobilisation ne s'appliquent que si on convertit effectivement un
compartiment d'acide vers base ou de base vers acide.

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

Hypothese de revente en annee 1 :

```math
\alpha = 0,20
\qquad
n = 1
```

```math
V_1 = \frac{140000}{1,20} \approx 116667
\qquad
V_2 = \frac{200000}{1,20} \approx 166667
```

Formule de cout net :

```math
C^{net}_s =
140000 A_{1,s} + 200000 A_{2,s}
- 116667 R_{1,s} - 166667 R_{2,s}
```

avec :

```math
A_{k,s} = \max(0, N_{k,s} - N^0_k)
\qquad
R_{k,s} = \max(0, N^0_k - N_{k,s})
```

| Critere | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 |
|---|---:|---:|---:|---:|
| Flotte demandee T1 | 7 | 4 | 4 | 4 |
| Flotte demandee T2 | 3 | 7 | 6 | 6 |
| Achats T1 | 3 | 0 | 0 | 0 |
| Achats T2 | 0 | 1 | 0 | 0 |
| Reventes T1 | 0 | 0 | 0 | 0 |
| Reventes T2 | 3 | 0 | 0 | 0 |
| **Cout net** | **-80000 euros** | **200000 euros** | **0 euro** | **0 euro** |

---

## Comparaison

| Critere | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 | Meilleur |
|---|---:|---:|---:|---:|---|
| Total camions | 10 | 11 | 10 | 10 | S1/S3/S4 |
| Type 1 | 7 | 4 | 4 | 4 | S2/S3/S4 |
| Type 2 | 3 | 7 | 6 | 6 | S1 |
| Distance regime permanent | 3185 | 2880 | 2765 | 2752,4 | S4 |
| Base couverte | 120,5 | 120,5 | 120 | 120 en annuel | S3/S4 |
| Cout net changement | -80000 | 200000 | 0 | 0 | S1 |

## Justification de minimalite du scenario 3 en distance journaliere stricte

Une borne inferieure sur le nombre de rotations transportant des bases est :

```math
N_B \ge \left\lceil \frac{120}{16,5} \right\rceil = 8
```

Il faut donc au moins 8 rotations transportant de la base. Avec 9 h/jour, un
camion direct base peut faire deux rotations, mais cela ne change pas la borne
sur le nombre de rotations physiques necessaires.

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

Il est donc minimal en distance dans le cadre journalier strict des hypotheses
retenues pour ce test :

- 8 rotations physiques avec base sont necessaires ;
- une rotation couplee acide-base ne peut pas etre doublee dans la meme journee ;
- un camion direct base peut faire deux rotations en 9 h, ce qui reduit le
  nombre de camions necessaires mais pas le nombre de rotations ;
- demandes journalieres moyennes pour AN, CH, GA et BR ;
- Hasselt traite par nombre annuel de livraisons de minimum 5 t ;
- quantite minimale de 5 t par livraison ;
- tournees construites avec les distances de l'enonce ;
- couplage uniquement via les compartiments du type 2.

Le scenario 4 ne contredit pas cette borne : il change le cadre du test. Il
utilise la convention de 9 h/jour, autorise deux rotations directes base par jour
pour un camion type 1, et raisonne sur la demande annuelle de base restante. La
reduction de distance vient du fait que les rotations de base restante sont
planifiees au plus juste sur l'annee :

```math
485 \text{ rotations/an}
```

au lieu de :

```math
2 \times 250 = 500 \text{ rotations/an}
```

## Choix selon le critere

| Cas | Scenario preferable | Raison |
|---|---|---|
| Minimiser le nombre total de camions | S1/S3/S4 | 10 camions |
| Minimiser la distance avec raisonnement journalier strict | S3 | 2765 km/j |
| Minimiser la distance avec raisonnement annuel pour la base restante | S4 | 2752,4 km/j en regime permanent |
| Minimiser le cout net de changement seul | S1 | revente de 3 camions type 2, mais trajet plus long |
| Eviter les achats et ventes | S3/S4 | flotte initiale conservee |
| Minimiser les camions type 2 | S1 | 3 camions type 2 |
| Garder une variante conservative | S1 | moins de dependance aux type 2 |

## Conclusion

Le scenario 3 est le meilleur compromis si on garde une lecture journaliere
stricte des tournees et si chaque jour doit ressembler au jour moyen.

Le scenario 4 devient meilleur si on accepte une planification annuelle de la
base restante. Il utilise la flotte initiale `4 T1 + 6 T2`, ne demande aucun
achat, ne declenche pas de changement d'affectation dans le cas principal, et
couvre la base restante avec un seul camion type 1 affecte aux bases.

Le scenario 1 reste utile comme variante si le PL final penalise fortement les
camions type 2.
