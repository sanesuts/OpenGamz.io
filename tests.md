# Tests pour le Centre de Jeux Multijoueurs

Ce fichier décrit tous les tests fonctionnels et cas d'utilisation pour les fonctions du projet.

---

## 1. Profil

### 1.1 `creer_profil()`
- Entrée : nom utilisateur valide
- Entrée : nom vide (doit renvoyer None)
- Entrée : nom existant (doit renvoyer None et avertir)
- Vérifier création du fichier JSON
- Vérifier initialisation de `total_score`, `parties` et `succes`
- Vérifier clear du terminal après création

### 1.2 `charger_profil()`
- Aucun profil existant (doit renvoyer None avec message d'erreur)
- Choix numéro invalide ou hors limites (doit renvoyer None)
- Profil JSON corrompu (doit renvoyer None)
- Profil valide (doit renvoyer le dict avec clear et message de succès)

### 1.3 `sauvegarder_donnees(profil)`
- Profil None (ne fait rien)
- Profil valide :
  - Vérifier écriture du fichier JSON
  - Vérifier mise à jour de `data/classements.json`
  - Vérifier clear et message
- Fichier classements inexistant ou corrompu

## 2. Jeux

### 2.1 `jouer_devinette(profil)`
- Difficultés : 1, 2, 3 (easy, average, hard)
- Entrée invalide (lettre, nombre hors limite)
- Nombre trouvé : vérifier score, ajout à `parties`, total_score
- Nombre non trouvé : score = 0
- Vérifier affichage des messages corrects et couleur

### 2.2 `jouer_calcul(profil)`
- Calculs aléatoires + réponse correcte / incorrecte
- Vérifier `correct_answers`, score calculé avec `calculer_points`
- Vérifier ajout à `parties` et total_score
- Vérifier gestion d'erreur entrée invalide
- Vérifier affichage temps restant et messages corrects

### 2.3 `jouer_pendu(profil)`
- Mot choisi via `charger_mots()`
- Lettre correcte / incorrecte
- Proposer le mot entier correct / incorrect
- Vérifier ascii_pendu affiché correctement
- Vérifier score et ajout à `parties`
- Vérifier clear à chaque essai

### 2.4 `jouer_rpsls(profil)`
- Tester 15 coups
- Vérifier victoire / égalité / défaite
- Vérifier calcul distance pour victoire (logique `(index_joueur - index_ordi) % nombre_de_coups`)
- Vérifier mise à jour `performance` (wins, rounds)
- Vérifier score via `calculer_points` et ajout à `parties`
- Vérifier affichage couleur et clear terminal entre tours

### 2.5 `charger_mots()`
- Fichier inexistant (retourne mot fallback)
- Fichier JSON invalide (retourne mot fallback)
- Thème choisi : numéro correct
- Thème choisi : nom correct
- Thème aléatoire (0 ou vide)
- Contenu JSON vide ou mots invalides (fallback)

## 3. Classements et succès

### 3.1 `afficher_classements()`
- Fichier inexistant (message correct)
- Classement vide (message correct)
- Classement avec joueurs : tri par score décroissant, affichage avec couleurs

### 3.2 `verifier_succes(profil)`
- Profil None (ne fait rien)
- Nombre de parties : 1, 5, 20, 50, 100
- Score total : 100, 500, 1000, 5000
- Jeux spécifiques : 5 parties minimum pour chaque jeu
- Vérifier affichage nouveaux succès
- Vérifier ajout au `profil['succes']`

## 4. Utilitaires

### 4.1 `calculer_points(game, performance)`
- Devine le nombre : différents niveaux de difficulté et essais restants
- Calcul mental : nombre de bonnes réponses
- Pendu : erreurs restantes
- Pierre-Feuille-Ciseaux (15 coups) : victoire / bonus selon nombre de wins
- Jeux inconnus : renvoie 0 points
- Vérifier que les points correspondent à la logique de chaque jeu
