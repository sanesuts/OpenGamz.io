# Projet 1PRJ1 – Centre de Jeux Multijoueurs

---

## 1️⃣ Description générale du projet

Le projet consiste à développer un centre de jeux multijoueurs en Python (console) permettant aux utilisateurs de créer et gérer des profils joueurs, jouer à plusieurs mini-jeux, cumuler des points, débloquer des succès et consulter des classements.

Le programme fonctionne entièrement en ligne de commande, avec un menu interactif, une sauvegarde persistante des données (JSON) et une gestion complète des erreurs.

---

## 2️⃣ Entrées utilisateur nécessaires

- Menu principal
    - Choix du menu (numéro entre 1 et 7)
- Gestion des profils
  - Nom du joueur
  - Sélection d’un profil existant
- Jeux
  - Devine le nombre
    - Choix de la difficulté (1, 2 ou 3)
    - Proposition de nombres
  - Calcul mental
    - Réponses numériques aux calculs
    - Réponses sous contrainte de temps (30 secondes)
  - Pendu
    - Choix du thème
    - Lettres proposées (1 caractère)
- Autres
  - Confirmation pour quitter
  - Navigation dans les classements et succès

-> Toutes les entrées utilisateur doivent être validées (type, plage de valeurs, non vide).

---

## 3️⃣ Traitements et algorithmes à implémenter

### **🎮 Logique des jeux**

- Génération aléatoire de nombres (random)
- Comparaison des réponses utilisateur
- Calcul des scores selon :
  - Difficulté
  - Nombre d’essais
  - Temps de réponse
- Gestion du chronomètre (time)

### **🏆 Système de points**

- Attribution de points dynamiques
- Mise à jour du score total du joueur

### **🎯 Succès**

- Vérification automatique après chaque partie :
  - Première victoire
  - Nombre de parties jouées
  - Score parfait
  - Performance exceptionnelle

### **📊 Classements**

- Classement global Top 10
- Classement par jeu
- Historique des 20 dernières parties

### **💾 Données**

- Chargement automatique des profils au démarrage
- Sauvegarde après chaque modification importante

---

## 4️⃣ Format de stockage des données

### **📁 Fichiers utilisés (JSON)**

**Profil joueur (1 fichier par joueur)**

```json
{
  "nom": "Marie",
  "date_creation": "2026-01-14",
  "parties": [
    {
      "jeu": "Pendu",
      "score": 150,
      "date": "2026-01-14"
    }
  ],
  "score_total": 450,
  "succes": ["Première victoire"]
}
```

**Classements globaux**

- `classements.json`
- Contient les scores cumulés et historiques récents

📌 Le format JSON est choisi pour sa lisibilité, sa simplicité et sa compatibilité Python.

---

## 5️⃣ Cas d’erreurs possibles et gestion

| Erreur possible              | Gestion prévue                     |
| ---------------------------- | ---------------------------------- |
| Entrée non numérique         | Message d’erreur + nouvelle saisie |
| Profil inexistant            | Message clair + retour menu        |
| Fichier JSON absent          | Création automatique               |
| Fichier JSON corrompu        | Message d’erreur + reset sécurisé  |
| Lettre invalide au pendu     | Message explicatif                 |
| Temps écoulé (calcul mental) | Partie terminée                    |
| Choix de menu invalide       | Nouvelle demande                   |
| Double succès                | Ignoré automatiquement             |


👉 Utilisation systématique de try / except

👉 Messages d’erreur clairs et compréhensibles

---

## 6️⃣ Fonctions principales prévues

- `creer_profil()`
- `charger_profil()`
- `jouer_devinette()`
- `jouer_calcul()`
- `jouer_pendu()`
- `calculer_points()`
- `verifier_succes()`
- `sauvegarder_donnees()`
- `charger_donnees()`

📌 Toutes les fonctions seront documentées (docstrings) et réutilisables.

---

## 7️⃣ Expérience utilisateur

- Menus clairs et numérotés
- Messages explicatifs à chaque étape
- Feedback immédiat après chaque action
- Affichage ASCII pour le pendu
- Navigation fluide sans crash

---

## 8️⃣ Outils et contraintes respectées

- Python 3.8+
- Modules standard uniquement
- Interface console
- Minimum 8 fonctions
- Git avec commits réguliers
- Respect PEP8

---