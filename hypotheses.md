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
| 1 | **Tournée-type acide** (route + nb de villes) | Détermine la durée d'une tournée → `K` (t/an par compartiment) | ❌ À concevoir à partir des distances |
| 2 | **Taux d'amortissement α** | Paramètre fixe pour calculer la recette de revente `C/(1+α)^n` (ce qu'on optimise c'est *quand* vendre, pas α) | ⚠️ Non donné dans l'énoncé ("entre 0 et 1") → α = 0,15 par hypothèse + sensibilité |
| 3 | **Vente l'année d'achat autorisée ?** | Détermine si la variable `V_{k,t,t}` existe → structure des contraintes de flotte | ✅ Oui, autorisé |
| 4 | **Couplage aller-retour acide/base ?** | Temps de transition 3 jours + affectation fixe par année → retour à vide, pas de couplage | ✅ Pas de couplage (§2, §3) |
| 5 | **Âge initial de la flotte** | Détermine le prix de revente des camions initiaux | ✅ Tous neufs (âge 0) |
| 6 | **Demande Hasselt** | Paramètre des contraintes de couverture | ✅ Approximation simple |
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

> À compléter une fois les tournées-types choisies.

- **Nombre de villes par tournée acide** : `m = ?` (ex. 2 ou 3 en moyenne)
- **Tournée-type acide retenue** : ex. `LI → CH → BR → LI` (à justifier : représentativité des distances, quantités)
- **Tournée base** : `LI → AN → LI` (trajet unique, pas de choix — camions basés à Liège).
- **Retour à vide** : les camions rentrent vides, pas de couplage acide/base aller-retour (décision §10, justifiée par le temps de transition de 3 j et l'affectation fixe par année).
- **Quantité par livraison** : chaque compartiment est rempli au maximum légal (16,5 t pour le grand), minimum légal 5 t par livraison.
- **Contrainte légale** : max 16,5 t d'**un même produit** par camion. Un type 2 ne peut donc pas charger de l'acide dans ses deux compartiments simultanément (16,5+5,5 = 22 t → illégal). Le petit compartiment (5,5 t) d'un type 2 affecté à l'acide reste vide sauf s'il est basculé vers la base (changement d'affectation = 3 j d'immobilisation).
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
  → Justification : 5 j/semaine × 8 h/j × 50 semaines = 2000 h. *À confirmer ou ajuster.*
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
  - **Choix retenu : approximation simple** — année 1 = 350 t, années 2–5 = 1300 t.
  - Justification : le PL travaille en pas annuels ; la transition mi-année 2 est arrondie à l'année 2 complète. Légèrement conservatif (on ne sous-estime jamais la demande).

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
- **Pas de stochasticité** : demande déterministe.
- **Pas de variabilité saisonnière** : demande constante au sein d'une année.
- **Pas de panne / indisponibilité imprévue** : `H^max` suppose déjà une disponibilité lissée.
- **Camion ≠ chauffeur** : on ignore les coûts/contraintes de personnel.

---

## 10. Questions ouvertes (à trancher avec le groupe)

- [x] Âge initial de la flotte → tous neufs (§5)
- [x] Modèle Hasselt → approximation simple (§4)
- [x] Convention vente → fin d'année (§8)
- [x] Valeur de `α` → 0,25 (standard fiscal belge 20 %/an, §6)
- [ ] Tournée-type acide : concevoir à partir des distances (§2)
- [x] Vente l'année d'achat → autorisée (§8)
- [x] Couplage aller-retour → pas de couplage, retour à vide (§2, §3)
