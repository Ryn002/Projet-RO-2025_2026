# Hypothèses de modélisation — Projet RO "Transport de produits chimiques"

Ce document recense **toutes les hypothèses** prises pour passer de l'énoncé à un PL résoluble. Chaque hypothèse doit être justifiée dans le rapport final.

---

## 0. Feuille de route : pourquoi deux grandes étapes, et quoi décider avant de calculer

### Pourquoi deux étapes ?

Le problème brut est un **problème à deux niveaux couplés** :

- **Niveau opérationnel** : comment organiser les tournées de livraison (qui passe par quelles villes, dans quel ordre, avec quel chargement) ?
- **Niveau stratégique** : combien de camions de chaque type acheter, affecter et revendre chaque année pour minimiser le coût total sur 5 ans ?

Ces deux niveaux sont liés : la taille de flotte nécessaire dépend de la capacité effective des camions, qui dépend elle-même des tournées effectuées. Résoudre les deux simultanément mènerait à un **problème de tournées de véhicules (VRP)** combiné à un problème de gestion de flotte — NP-difficile, hors de portée d'un PL standard.

**Stratégie adoptée — découplage en deux étapes séquentielles :**

```
Étape 1 — Opérationnel (figé à la main)
  Choisir des tournées-types représentatives
  → Calculer la capacité annuelle K d'un compartiment (t/an)

Étape 2 — Stratégique (optimisé par PL)
  Données d'entrée : demandes annuelles + capacités K
  → Trouver le plan d'achat/vente/affectation optimal sur 5 ans
```

L'étape 1 est résolue **par hypothèses et calculs manuels** ; l'étape 2 est le **PL à résoudre**. Ce découplage est justifiable car les tournées sont peu variables (géographie fixe, clients fixes) et l'enjeu principal est la composition de la flotte.

---

### Ce qu'il faut impérativement fixer avant de lancer le PL

Le PL de l'étape 2 ne peut pas être écrit tant que les paramètres suivants ne sont pas arrêtés :

| # | Paramètre | Pourquoi c'est bloquant | Statut |
|---|-----------|------------------------|--------|
| 1 | **Tournées acide/base retenues** | Déterminent les capacités journalières, les distances et les besoins de flotte | ✅ Scénario hybride S3 retenu provisoirement (`tests_bases_couplage_anvers.md`) |
| 2 | **Taux d'amortissement α** | Paramètre fixe pour calculer la recette de revente `C/(1+α)^n` (ce qu'on optimise c'est *quand* vendre, pas α) | ✅ α = 0,25 par hypothèse + sensibilité |
| 3 | **Vente l'année d'achat autorisée ?** | Détermine si la variable `V_{k,t,t}` existe → structure des contraintes de flotte | ✅ Oui, autorisé |
| 4 | **Couplage aller-retour acide/base ?** | Influence directement le nombre de camions et les distances | ✅ Couplage partiel via Anvers, scénario S3 (§2) |
| 5 | **Âge initial de la flotte** | Détermine le prix de revente des camions initiaux | ✅ Tous neufs (âge 0) |
| 6 | **Demande Hasselt** | Paramètre des contraintes de couverture | ✅ Traitement annuel par livraisons minimales de 5 t |
| 7 | **Convention vente** | Détermine la disponibilité et le moment de la recette | ✅ Fin d'année t |

---

## 1. Approche générale

**Problème à deux niveaux** :
- Niveau stratégique (flotte) : achats, ventes, affectations sur 5 ans.
- Niveau opérationnel (transport) : quelle tournée, qui livre quoi à qui.

**Choix de découplage** : on **fige le transport** par des hypothèses de tournées-types, on calcule les capacités annuelles `K` d'un compartiment, puis on **optimise uniquement la flotte** via un PL.

```
Hypothèses tournées → Capacités K → PL flotte → Solution
```

---

## 2. Hypothèses sur les tournées (niveau opérationnel figé)

Les hypothèses opérationnelles principales viennent du fichier
`tests_bases_couplage_anvers.md`. Ce fichier compare trois organisations
journalières combinant acides et bases, puis recommande le scénario hybride S3.

### 2.1 Convention journalière

- **Jours ouvrables** : 250 jours/an.
- **Temps de travail principal** : 8 h/jour/camion dans le test couplé.
- **Vitesse moyenne** : 70 km/h.
- **Arrêt de livraison acide** : 1 h par ville livrée.
- **Chargement de base à Anvers** : 0,5 h.
- **Déchargement de base à Liège** : 1 h.
- **Quantité minimale par livraison** : 5 t.

Demande journalière de référence en régime permanent :

| Produit / ville | Quantité |
|---|---:|
| Base AN → LI | 120 t/j |
| Acide AN | 36 t/j |
| Acide CH | 48 t/j |
| Acide GA | 8 t/j |
| Acide BR | 24,8 t/j |
| Acide HA, années 3-5 | 5,2 t/j |
| **Total acide régime permanent** | **122 t/j** |

### 2.2 Couplage acide/base par Anvers

Le couplage retenu exploite les camions de type 2 :

- un compartiment transporte de l'acide de Liège vers Anvers ;
- l'autre compartiment ramène de la base d'Anvers vers Liège.

Le scénario recommandé dans `tests_bases_couplage_anvers.md` est le **scénario 3
hybride** :

| Bloc | Tournées | Type | Acide | Base | Distance |
|---|---|---|---:|---:|---:|
| CH | 2 × LI-CH-LI | T1 | 33 t | 0 | 400 km |
| CH/BR | LI-CH-LI + LI-BR-LI | T1 | 31,3 t | 0 | 400 km |
| GA/BR | LI-GA-BR-LI | T1 | 16,5 t | 0 | 280 km |
| AN/HA | LI-AN-HA-LI | T2 | 16,2 t | 5,5 t | 215 km |
| AN direct | 5 × LI-AN-LI | T2 | 25 t | 82,5 t | 1050 km |
| Base restante | 2 × LI-AN-LI | T1 | 0 | 32 t | 420 km |
| **Total** |  |  | **122 t** | **120 t** | **2765 km/j** |

Bilan de flotte journalier du scénario S3 :

| Type 1 | Type 2 | Total camions | Base couverte | Distance |
|---:|---:|---:|---:|---:|
| 5 | 6 | 11 | 120 t/j | 2765 km/j |

Ce scénario est retenu provisoirement car il minimise la distance et le coût net
de changement de flotte parmi les trois scénarios testés :

| Scénario | Type 1 | Type 2 | Total | Distance | Coût net de changement |
|---|---:|---:|---:|---:|---:|
| S1 : garder Anvers dans les tournées acide | 10 | 3 | 13 | 3185 km/j | 360000 € |
| S2 : retirer Anvers des tournées acide | 4 | 7 | 11 | 2880 km/j | 200000 € |
| S3 : hybride | 5 | 6 | 11 | 2765 km/j | 140000 € |

### 2.3 Traitement de Hasselt dans les tournées

Hasselt n'est pas traité comme une livraison journalière constante en années 1
et 2, car la livraison minimale est de 5 t.

On retient :

| Année | Demande HA | Nombre de livraisons | Quantité par livraison |
|---:|---:|---:|---:|
| 1 | 350 t | 70 | 5 t |
| 2 | 825 t | 165 | 5 t |
| 3-5 | 1300 t | 250 | 5,2 t |

Dans les scénarios S1 et S3, Hasselt est intégré à une tournée passant déjà par
Anvers. Le surcoût d'une livraison Hasselt est donc seulement :

```text
d_AN,HA + d_HA,LI - d_AN,LI = 50 + 60 - 105 = 5 km
```

Le scénario S3 reste le plus court après correction annuelle des distances :

| Année | Scénario 1 | Scénario 2 | Scénario 3 |
|---:|---:|---:|---:|
| 1 | 3181,4 km/j | 2793,6 km/j | 2761,4 km/j |
| 2 | 3183,3 km/j | 2839,2 km/j | 2763,3 km/j |
| 3-5 | 3185 km/j | 2880 km/j | 2765 km/j |

### 2.4 Contraintes de capacité et de produit

- **Camion type 1** : un compartiment de 16,5 t.
- **Camion type 2** : deux compartiments, 16,5 t et 5,5 t.
- **Contrainte légale** : maximum 16,5 t d'un même produit par camion.
- **Interprétation retenue** : un camion type 2 peut coupler deux produits
  différents, par exemple 5,5 t d'acide vers Anvers et 16,5 t de base au retour,
  car la limite porte sur un même produit.
- **Quantité par livraison** : on ne force pas le remplissage complet lorsque la
  demande restante d'une ville est inférieure à la capacité ; on respecte en
  revanche le minimum de 5 t par arrêt.

### 2.5 Points de doute à signaler

- **Durée journalière** : le test couplé principal utilise 8 h/jour, tandis que
  le test acide isolé `tests_acide_type1_9h_rechargement.md` étudie une variante
  à 9 h/jour avec 0,5 h de rechargement entre deux tournées. Il faut choisir une
  convention unique dans le rapport final ou présenter 9 h comme analyse de
  sensibilité.
- **Rechargement acide à Liège** : le test couplé ne pénalise pas explicitement
  les doubles tournées acide par 0,5 h de rechargement à Liège. C'est une
  hypothèse optimiste à mentionner si le scénario S3 est utilisé tel quel.
- **Changement d'affectation des compartiments** : on suppose une affectation
  stable à l'année. Les 3 jours de nettoyage ne sont donc pas déclenchés par les
  tournées journalières.
- **Âge réel des camions initiaux** : inconnu dans l'énoncé ; l'hypothèse d'âge
  0 reste une simplification.
- **Distances (km)** (énoncé) :

|   | AN | CH | LI | GA | BR | HA |
|---|----|----|----|----|----|----|
| **AN** | — | 100 | 105 | 40 | 45 | 50 |
| **CH** | | — | 100 | 100 | 60 | 80 |
| **LI** | | | — | 140 | 100 | 60 |
| **GA** | | | | — | 40 | 60 |
| **BR** | | | | | — | 50 |

---

## 3. Capacité annuelle d'un camion

- **Vitesse moyenne** : `v = 70 km/h` (énoncé).
- **Temps d'arrêt par livraison** : `t^stop = 1 h` (énoncé).
- **Heures de travail annuelles maximales** : `H^max = 2000 h/an`
  → Justification : 250 jours ouvrables × 8 h/jour = 2000 h/an dans le scénario couplé principal.
- **Variante testée** : 9 h/jour avec 0,5 h de rechargement entre deux tournées acide (`tests_acide_type1_9h_rechargement.md`). Cette variante n'est pas encore intégrée au scénario couplé S3.
- **Immobilisation pour changement de compartiment** : `τ^change = 3 jours ouvrables` (énoncé).
  → **Hypothèse simplificatrice** : on suppose **zéro changement d'affectation en cours d'année** (affectation fixe par année). L'immobilisation est donc ignorée.

---

## 4. Demandes annuelles

- **Base** (AN → LI) : 30 000 t/an constant sur 5 ans.
- **Acide** (depuis LI) — constant sur 5 ans pour AN, CH, GA, BR :
  - Anvers : 9 000 t/an
  - Charleroi : 12 000 t/an
  - Gand : 2 000 t/an
  - Bruxelles : 6 200 t/an
- **Hasselt (cas spécial)** — "nouvelle unité dans 18 mois" :
  - **Choix retenu** : année 1 = 350 t, année 2 = 825 t, années 3–5 = 1300 t.
  - Justification : la nouvelle unité démarre dans 18 mois. L'année 2 est donc modélisée comme une demi-année à 350 t/an et une demi-année à 1300 t/an :
    `D_HA,2 = 0,5 × 350 + 0,5 × 1300 = 825`.
  - Comme la livraison minimale est de 5 t, Hasselt n'est pas forcément livré tous les jours :
    année 1 = 70 livraisons de 5 t, année 2 = 165 livraisons de 5 t, années 3–5 = 250 livraisons de 5,2 t.

---

## 5. Flotte initiale

- Année 0 : `N_{1,0} = 4`, `N_{2,0} = 6` (énoncé).
- **Âge des camions initiaux** : **choix retenu — tous neufs (âge = 0 au début de l'année 1)**.
  - Justification : l'énoncé ne donne aucune information sur l'historique d'achat ; on modélise uniquement l'horizon de 5 ans.

---

## 6. Coûts et financier

- **Achat** : type 1 = 140 000 € ; type 2 = 200 000 € (énoncé).
- **Entretien** : 5 000 €/an/camion (énoncé, quel que soit le type).
- **Revente** : `C / (1+α)^n`
  - **Taux d'amortissement α** : non donné par l'énoncé (indiqué seulement "entre 0 et 1").
    - **Choix retenu : α = 0,25.**
    - Justification : le standard fiscal belge pour les véhicules utilitaires est 20 %/an (durée usuelle 5 ans, amortissement linéaire — SPF Finances / [myfid.be](https://www.myfid.be/ressources/fiscalite/amortissement/)). Dans la formule exponentielle `C/(1+α)^n`, cela correspond à α = r/(1−r) = 0,20/0,80 = **0,25**. Un camion de 140 000 € vaut ainsi ~46 000 € après 5 ans.
    - Une analyse de sensibilité sur α ∈ {0,15 ; 0,25 ; 0,35} sera menée.
  - **n = âge du camion** à la revente → nécessite de tracker les cohortes (choix A).
- **Actualisation des flux** : aucune (pas de taux d'actualisation inter-annuel). Justification : horizon court (5 ans), pas mentionné dans l'énoncé.

---

## 7. Suivi des cohortes de camions (choix A)

Pour calculer correctement la recette de revente `C/(1+α)^n`, on suit les **générations d'achat** :

- `A_{k,s}` : camions de type k achetés en année s.
- `V_{k,s,t}` : camions de type k, achetés en s, vendus en t (âge = t − s).
- Flotte initiale traitée comme une cohorte `s = 0` avec âge initial fixé par hypothèse §5.

---

## 8. Conventions temporelles

- Horizon : `T = {1, 2, 3, 4, 5}`.
- Année 1 = première année à compter du début du projet.
- Toutes les décisions (achat, vente, affectation) sont prises **en début d'année**.
- Un camion acheté en année t est disponible pour toute l'année t.
- Un camion vendu en année t est **disponible pendant toute l'année t**, la recette de revente est perçue en **fin d'année t**, et il n'est plus disponible en t+1.

---

## 9. Simplifications qu'on assume explicitement

- **Pas de VRP** : les tournées sont figées, pas de routage optimisé.
- **Couplage limité** : le couplage acide/base est testé uniquement via Anvers et les compartiments du type 2.
- **Pas de stochasticité** : demande déterministe.
- **Pas de variabilité saisonnière** : demande constante au sein d'une année.
- **Pas de panne / indisponibilité imprévue** : `H^max` suppose déjà une disponibilité lissée.
- **Camion ≠ chauffeur** : on ignore les coûts/contraintes de personnel.
- **Rechargement acide non intégré au scénario S3** : contrairement au test acide isolé à 9 h, le scénario couplé S3 ne rajoute pas explicitement 0,5 h de rechargement entre deux tournées acide.

---

## 10. Questions ouvertes (à trancher avec le groupe)

- [x] Âge initial de la flotte → tous neufs (§5)
- [x] Modèle Hasselt → traitement annuel avec minimum 5 t/livraison (§4)
- [x] Convention vente → fin d'année (§8)
- [x] Valeur de `α` → 0,25 (standard fiscal belge 20 %/an, §6)
- [x] Tournées acide/base → scénario hybride S3 retenu provisoirement (§2)
- [x] Vente l'année d'achat → autorisée (§8)
- [x] Couplage aller-retour → couplage partiel par Anvers avec type 2 (§2)
- [ ] Décider si le rapport final garde 8 h/jour comme scénario principal ou passe à 9 h/jour avec rechargement.
- [ ] Décider si le rechargement acide à Liège doit être ajouté au scénario couplé S3.
