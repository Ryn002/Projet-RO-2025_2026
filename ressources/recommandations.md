# Synthèse complète de la session questions-réponses

## Contexte général

Ce document synthétise tout ce qui a été dit et recommandé par l’assistant/professeur pendant la session de questions-réponses concernant le projet.

L’objectif principal de la session était de clarifier les attentes autour du rapport, des hypothèses de modélisation, de la stabilité des solutions, de l’utilisation d’outils comme les LLM, du code, de l’oral et des critères d’évaluation implicites.

---

# 1. Les hypothèses sont acceptées si elles sont bien justifiées

Le point le plus répété est que vous avez le droit de poser des hypothèses de modélisation, même fortes, à condition de les justifier solidement.

Un exemple discuté est l’hypothèse selon laquelle les camions TP2 à deux compartiments feraient uniquement des allers-retours entre Anvers et Liège, tandis que le reste serait géré par d’autres types de camions.

La réponse donnée est claire : ce type d’hypothèse peut être accepté si la justification semble solide, cohérente et logique. Le professeur ne pénalisera pas une hypothèse simplement parce qu’elle simplifie le problème, tant qu’elle est défendue correctement.

Il faut éviter de dire simplement :

> On fait ça parce que c’est comme ça.

Il faut plutôt montrer pourquoi cette hypothèse :

- a du sens dans le contexte du problème ;
- simplifie raisonnablement la modélisation ;
- ne détruit pas la validité des résultats ;
- repose sur du bon sens, des calculs, des données externes ou une argumentation claire.

---

# 2. La “borne” de justification : il faut convaincre, pas prouver absolument

À la question “jusqu’où faut-il justifier une hypothèse ?”, la réponse est que vous devez aller assez loin pour convaincre le lecteur.

La justification peut venir de plusieurs sources :

- calculs ;
- bon sens ;
- données trouvées sur Internet ;
- comparaison entre options ;
- logique opérationnelle ;
- impact estimé sur la solution.

Il n’est pas demandé de démontrer mathématiquement chaque hypothèse de façon ultra-théorique. Il faut surtout que l’hypothèse paraisse raisonnable et défendable.

---

# 3. L’utilisation des LLM pour rédiger le rapport n’est pas une pénalité en soi

Un étudiant demande s’il peut utiliser des LLM pour l’aide à la rédaction du rapport, surtout pour formuler le texte.

La réponse implicite est que l’utilisation d’un LLM n’est pas pénalisante en soi, tant que le travail est relu, corrigé et compris.

L’idée importante est que ce n’est pas interdit d’utiliser un LLM pour la rédaction textuelle, mais il faut maîtriser ce qui est écrit. Pendant la présentation, les étudiants pourront être interrogés sur leur raisonnement, leurs résultats et leur modèle.

Il ne faut donc pas mettre du texte généré qu’on ne comprend pas.

---

# 4. Tester la stabilité de la solution est important

Le professeur insiste sur la stabilité des résultats.

L’idée est de vérifier si votre solution dépend fortement de certains paramètres ou si elle reste robuste quand les données changent légèrement.

Exemple donné : si une demande est de 9000 tonnes et qu’on passe à 9001 tonnes, est-ce que toute la solution change radicalement ? Est-ce que la fonction coût explose ? Si oui, il faut le dire et l’analyser.

Cela peut concerner :

- des données données dans l’énoncé ;
- des paramètres que vous choisissez vous-mêmes ;
- des valeurs trouvées sur Internet ;
- des coefficients de coût ;
- la décote des camions ;
- le prix du carburant ;
- le coût au kilomètre ;
- les demandes ;
- les distances ;
- les capacités ;
- tout paramètre qui influence fortement le modèle.

Le professeur ne demande pas de grands développements théoriques sur la stabilité. Il veut plutôt voir concrètement à quel point la solution est sensible ou robuste.

Ce qu’il attend :

- faire varier certains paramètres ;
- observer si la solution change beaucoup ou peu ;
- expliquer si la solution est très dépendante d’un ou plusieurs paramètres ;
- dire si elle paraît robuste ;
- signaler les cas où un petit changement provoque une grosse modification.

---

# 5. Il faut discuter la dépendance de la solution aux paramètres

Le professeur demande de montrer si la solution optimale, ou la meilleure solution trouvée, est très dépendante des valeurs choisies.

Il veut savoir si la solution dépend :

- d’un seul paramètre ;
- de plusieurs paramètres en même temps ;
- d’une hypothèse forte ;
- d’une donnée incertaine ;
- d’un choix de modélisation.

Par exemple, si en changeant légèrement le prix du carburant ou la décote des camions, l’algorithme choisit une organisation totalement différente, c’est intéressant et il faut l’expliquer.

Il ne faut pas seulement donner un résultat final. Il faut analyser la nature de ce résultat.

---

# 6. Les données à faire varier ne viennent pas seulement de l’énoncé

Un étudiant demande si la stabilité doit être étudiée uniquement sur les données de l’énoncé.

La réponse est non.

Il y a aussi des choses qui ne sont pas forcément données dans l’énoncé et que vous devez aller chercher vous-mêmes, par exemple sur Internet.

Donc la stabilité peut être testée sur :

- les données imposées par l’énoncé ;
- les données externes ;
- les hypothèses de coût ;
- les valeurs estimées ;
- les paramètres créés par votre propre modèle.

---

# 7. Les hypothèses successives et les comparaisons entre scénarios sont une bonne méthode

Une étudiante explique qu’elle construit son rapport en faisant plusieurs hypothèses successives :

1. elle envisage deux possibilités ;
2. elle choisit l’hypothèse qui semble optimale ;
3. elle poursuit avec une nouvelle hypothèse ;
4. elle revient parfois sur une hypothèse rejetée pour voir si elle devient meilleure avec une nouvelle condition ;
5. elle discute à chaque étape.

Le professeur répond que c’est intéressant et que c’est une bonne manière de faire.

Donc une démarche progressive où vous comparez plusieurs scénarios, rejetez certains choix, puis réévaluez certains choix plus tard est acceptable.

C’est même valorisé si cela montre une vraie réflexion.

---

# 8. Il n’est pas nécessaire d’explorer entièrement tous les modèles alternatifs

Un étudiant dit que changer la granularité temporelle, par exemple passer d’un modèle annuel à un modèle journalier, obligerait à refaire tout le modèle.

Le professeur répond qu’il ne s’attend pas à recevoir cinq travaux différents dans un seul rapport.

Il n’est donc pas nécessaire de refaire complètement le modèle sous plusieurs angles.

Ce qui est recommandé :

- explorer réellement certaines variantes si cela reste raisonnable ;
- ne pas tout refaire si cela demande de reconstruire tout le modèle ;
- mentionner les pistes non explorées ;
- inclure une ou deux pages sur les extensions possibles.

---

# 9. Ajouter une section “extensions possibles” est recommandé

Le professeur recommande explicitement de mettre une ou deux pages du rapport sur les extensions possibles.

Cette section peut contenir :

- des modèles alternatifs ;
- des pistes que vous auriez pu explorer ;
- des raffinements du modèle ;
- des changements de variables ;
- une granularité temporelle différente ;
- des hypothèses plus réalistes ;
- des versions plus complexes du problème.

Il n’est pas obligatoire de les implémenter. Vous pouvez expliquer qu’elles seraient intéressantes mais non traitées dans le rapport.

Exemple : dire qu’un modèle par jour au lieu d’un modèle par année serait envisageable, mais qu’il demanderait de refaire toute la formulation.

---

# 10. Aller du simple au complexe est une bonne stratégie

Le professeur encourage l’idée de construire plusieurs “couches” de modélisation, en allant du modèle simple vers un modèle plus complexe.

Une première couche peut être très simplifiée.

Exemple donné : dans un premier modèle, on suppose qu’un camion part de Liège, va dans une ville, puis revient à Liège.

Ce type de modèle simple permet :

- de poser une première structure ;
- de comprendre le problème ;
- d’avoir une base de comparaison ;
- de complexifier ensuite progressivement.

Le professeur dit que cela peut se faire sur beaucoup d’aspects du projet, pas seulement sur la durée ou le nombre d’années.

L’idée générale est que le modèle le plus complexe possible serait la réalité. Votre travail consiste donc à construire une approximation raisonnable, puis éventuellement à l’enrichir.

---

# 11. Le multi-objectif peut être intéressant

Un étudiant demande si faire une fonction multi-objectif sort du cadre du projet.

Le professeur répond que non, il n’est pas contre. Il trouve même que cela peut être intéressant.

Il précise qu’il y aura clairement une fonction de coût, mais qu’on peut envisager d’autres objectifs.

Par exemple, on pourrait comparer :

- minimisation du coût ;
- réduction du nombre de camions ;
- réduction des distances ;
- réduction des émissions ;
- robustesse ;
- flexibilité ;
- simplicité opérationnelle.

Un objectif supplémentaire peut enrichir le projet, surtout si cet objectif est difficile à optimiser en même temps que le coût.

Ce qui est recommandé :

- garder en tête l’objectif principal du projet ;
- ne pas perdre la fonction coût ;
- utiliser le multi-objectif pour comparer et analyser ;
- montrer les compromis entre objectifs.

---

# 12. Même un modèle simple peut être intéressant s’il est bien évalué

Un étudiant demande si un modèle simple reste intéressant si on évalue bien ses solutions.

Le professeur répond oui.

Un modèle simple n’est pas forcément mauvais. Il peut être utile s’il est :

- clair ;
- bien justifié ;
- bien analysé ;
- comparé à d’autres possibilités ;
- utilisé comme base pour comprendre le problème.

La valeur du travail ne dépend donc pas uniquement de la complexité du modèle, mais de la qualité de la réflexion.

---

# 13. Le code ne doit pas forcément être entièrement mis dans le rapport

Un étudiant demande s’il faut mettre le code dans le rapport.

Le professeur répond qu’il faut mettre ce qui semble utile, en gardant en tête la limite de pages.

Il ne demande pas nécessairement de mettre tout le code.

Ce qui compte :

- expliquer le modèle ;
- expliquer les résultats ;
- montrer ce qui est nécessaire à la compréhension ;
- être capable de défendre le travail à l’oral.

Il précise qu’il posera des questions pendant la présentation, notamment sur la nature des résultats.

Donc même si le code n’est pas dans le rapport, il faut être capable d’expliquer ce que le programme fait, pourquoi il le fait, et ce que les résultats signifient.

---

# 14. Pendant l’oral, il faut maîtriser son sujet

Le professeur dit clairement qu’il va “cuisiner” les étudiants pendant la présentation.

Cela veut dire qu’il posera des questions pour vérifier :

- la compréhension du modèle ;
- la maîtrise des hypothèses ;
- la logique des résultats ;
- la capacité à interpréter la solution ;
- la compréhension du code ou de l’implémentation ;
- la cohérence entre le rapport et la présentation.

Il ne suffit donc pas d’avoir un bon rapport écrit. Chaque membre doit être capable d’expliquer le travail.

---

# 15. Avoir des hypothèses similaires entre groupes est normal

Un étudiant demande si c’est problématique que deux groupes aient les mêmes hypothèses.

Le professeur répond que non, certaines hypothèses seront naturellement similaires entre groupes.

Exemple : le prix de l’essence. Beaucoup de groupes vont forcément devoir faire une hypothèse dessus.

Il dit qu’il ne faut pas écrire une page entière sur ce genre d’hypothèse évidente. Il suffit de dire d’où vient la valeur, par exemple qu’elle a été trouvée sur Internet.

En revanche, pour les éléments moins précis de l’énoncé, il attend des hypothèses de modélisation plus justifiées.

Il y a donc deux types d’hypothèses.

## Hypothèses banales ou évidentes

Exemple : prix du carburant.

À traiter brièvement :

- valeur utilisée ;
- source ;
- justification rapide si nécessaire.

## Hypothèses structurantes de modélisation

Exemple : organisation des trajets, affectation des camions, simplification temporelle.

À traiter plus sérieusement :

- pourquoi ce choix ;
- impact sur le modèle ;
- limites ;
- alternatives possibles.

---

# 16. Si deux groupes ont des hypothèses proches, il vérifiera que le travail est bien différent

Le professeur dit que si deux groupes ont des hypothèses similaires, ce n’est pas automatiquement suspect.

Mais il vérifiera :

- que les travaux sont réellement différents ;
- que les groupes ont travaillé indépendamment ;
- que chacun maîtrise son sujet ;
- que le rapport n’est pas une copie.

Le problème n’est donc pas d’avoir une même hypothèse logique. Le problème serait d’avoir un travail identique sans maîtrise réelle.

---

# 17. On peut lisser une demande sur l’année, mais il faut justifier l’impact

Un étudiant demande s’il peut supposer qu’un changement de besoin au cours d’une année est absorbé par une moyenne annuelle.

Exemple : au lieu de considérer qu’une demande passe brutalement à une nouvelle valeur après six mois, on prend une moyenne sur l’année.

Le professeur dit que cela peut se faire.

Mais il faut :

- justifier cette hypothèse ;
- expliquer que c’est une simplification ;
- analyser à quel point cette simplification modifie les résultats ;
- se demander si la solution resterait applicable sans cette simplification.

Point important : une simplification peut être acceptable même si elle éloigne un peu de la réalité, mais il faut en être conscient et l’expliquer.

---

# 18. Il faut évaluer si une simplification rend la solution inapplicable

Le professeur insiste sur une question importante :

> Si je fais cette simplification, est-ce que le résultat obtenu serait encore applicable dans le vrai problème ?

Ce n’est pas parce qu’une simplification change les résultats qu’elle est automatiquement mauvaise. Mais il faut discuter son effet.

Exemple avec la moyenne annuelle :

- si la moyenne donne presque les mêmes besoins logistiques, c’est probablement acceptable ;
- si elle cache un pic important de demande, elle peut rendre la solution irréaliste ;
- dans ce cas, il faut le signaler.

---

# 19. Le coût final ne sera pas le critère principal de comparaison entre groupes

Un étudiant demande si le professeur peut donner une valeur de référence du coût final pour savoir s’ils sont loin ou proches d’une bonne solution.

Le professeur répond qu’il ne va pas juger les groupes en disant simplement :

> Le groupe A a un coût plus faible que le groupe B, donc le groupe A est meilleur.

Il dit que l’évaluation est plus complexe.

Le coût final est important, mais ce n’est pas le critère principal isolé.

Ce qui compte davantage :

- la démarche ;
- la modélisation ;
- la justification ;
- l’implémentation ;
- l’analyse des résultats ;
- la capacité à interpréter les solutions ;
- la cohérence globale.

---

# 20. Le résultat final compte, mais surtout son analyse

Le professeur dit que les résultats sont importants, mais qu’il ne va pas s’attarder sur “qui a le meilleur coût”.

Il veut surtout voir si vous savez analyser vos résultats.

Il faut donc éviter de présenter seulement :

> Notre coût final est X.

Il faut expliquer :

- pourquoi ce coût apparaît ;
- quelles décisions le modèle a prises ;
- quelles hypothèses influencent ce coût ;
- si le résultat est robuste ;
- si le résultat est réaliste ;
- quelles sont les limites ;
- ce qui pourrait être amélioré.

---

# 21. Une bonne idée mal implémentée n’est pas suffisante

Le professeur dit qu’avoir de bonnes idées ne suffit pas si l’implémentation est mauvaise.

Il faut réussir à tirer des résultats cohérents de votre modélisation.

Il dit en substance que si vous avez des idées mais que vous les appliquez n’importe comment, ou si vous n’arrivez pas à tirer des résultats à partir de votre modélisation, alors ce n’est pas terrible.

Le projet doit donc combiner :

- bonnes hypothèses ;
- bonne formulation ;
- implémentation correcte ;
- résultats exploitables ;
- analyse claire.

---

# 22. Le rapport doit montrer une vraie démarche de réflexion

La démarche est centrale dans l’évaluation.

Le professeur insiste plusieurs fois sur le fait qu’il valorise :

- la réflexion ;
- la justification ;
- la construction du modèle ;
- la discussion des hypothèses ;
- l’analyse des résultats ;
- la capacité à reconnaître les limites ;
- la comparaison entre plusieurs possibilités.

Il ne cherche pas simplement une solution numérique finale.

---

# 23. Il ne faut pas surdévelopper les détails peu importants

Exemple donné : le prix de l’essence.

Le professeur dit clairement qu’il ne faut pas écrire une page entière sur ce genre de point.

Pour les hypothèses évidentes ou peu centrales, il suffit de :

- donner la valeur ;
- citer l’origine ;
- expliquer brièvement.

Il faut réserver l’espace du rapport aux choix importants de modélisation.

---

# 24. Le rapport peut contenir des pistes non explorées

Dans la section extensions possibles, vous pouvez parler de choses non implémentées.

Il est acceptable de dire :

- On aurait pu modéliser le temps par jour.
- On aurait pu intégrer un autre objectif.
- On aurait pu complexifier les trajets.
- On aurait pu tester une autre organisation des camions.
- On aurait pu prendre des demandes non moyennées.

Ces pistes ne doivent pas forcément être développées complètement, mais elles montrent que vous avez conscience des limites de votre modèle.

---

# 25. Les étudiants peuvent encore envoyer des mails

À la fin, un étudiant demande s’ils peuvent encore envoyer des mails avant la remise.

Le professeur répond oui.

Il reste donc possible de poser des questions par mail avant la deadline.

---

# 26. Informations pratiques sur l’oral

Le professeur précise plusieurs éléments pratiques.

L’oral aura lieu en session, car ils n’ont pas le droit d’évaluer les étudiants hors période d’évaluation.

La date exacte sera fixée en fonction des contraintes des étudiants et des autres examens.

Il envisage probablement une demi-journée pendant laquelle tous les groupes passent.

Le format annoncé :

- 10 minutes de présentation ;
- 10 minutes de questions.

Il semble que la défense se fasse devant lui uniquement, d’après la réponse donnée à la question.

---

# 27. Informations pratiques sur la remise

Le professeur rappelle que la remise est prévue le vendredi suivant, donc environ une semaine et un jour après la session de questions-réponses.

Il dit qu’il ne pense pas qu’il y aura une autre réunion avant la remise.

Il mentionne qu’il sera en contact avec certains responsables ou étudiants pour fixer la date de défense.

---

# 28. Stratégie recommandée pour le rapport

La stratégie recommandée est la suivante :

1. Poser clairement les hypothèses.
2. Justifier chaque hypothèse importante.
3. Ne pas surdévelopper les hypothèses évidentes.
4. Construire éventuellement un modèle simple.
5. Complexifier progressivement si utile.
6. Comparer plusieurs scénarios.
7. Tester la stabilité de la solution.
8. Montrer l’impact des paramètres.
9. Discuter les limites.
10. Ajouter une section sur les extensions possibles.
11. Présenter des résultats exploitables.
12. Savoir expliquer les résultats à l’oral.

---

# 29. Ce qu’il faut éviter

Il faut éviter :

- poser une hypothèse sans justification ;
- dire “on a choisi ça comme ça” ;
- chercher uniquement le coût minimum sans analyser ;
- mettre des résultats sans expliquer leur sens ;
- faire un modèle trop complexe qu’on ne maîtrise pas ;
- remplir le rapport avec des détails secondaires ;
- mettre du texte généré par LLM sans le comprendre ;
- cacher les limites du modèle ;
- prétendre qu’une simplification est neutre sans l’avoir discutée ;
- ne pas savoir défendre le code ou les résultats à l’oral.

---

# 30. Conclusion générale de la session

Le professeur valorise surtout la qualité de la démarche.

Il ne cherche pas seulement une solution optimale au sens numérique. Il veut voir que vous êtes capables de :

- formuler un problème réel en modèle mathématique ;
- faire des hypothèses raisonnables ;
- justifier ces hypothèses ;
- implémenter correctement le modèle ;
- analyser les résultats ;
- tester la robustesse de la solution ;
- reconnaître les limites ;
- proposer des extensions ;
- défendre votre travail oralement.

Le message global est donc :

> Une solution imparfaite mais bien construite, bien justifiée et bien analysée peut être meilleure qu’une solution avec un coût faible mais mal expliquée ou mal maîtrisée.
