# 🎮 OpenGamz.io – Projet 1PRJ1

## 📚 Présentation du projet

Ce projet a été réalisé dans le cadre du module **1PRJ1 – Projet Python Fondamental** (Bachelor 1 – Unité 1, École IT, année 2025–2026).

Le **Centre de Jeux Multijoueurs** est une application Python en **ligne de commande** permettant de :
- Créer et gérer des profils joueurs
- Jouer à plusieurs mini-jeux
- Gagner des points
- Débloquer des succès
- Consulter des classements et statistiques

Le projet met en pratique les bases de **Python**, de **l’algorithmique**, de la **gestion de fichiers**, de la **gestion des erreurs**, ainsi que l’utilisation de **Git**.

---

## 🛠️ Technologies utilisées

- **Langage** : Python 3.8+
- **Interface** : Console / Terminal
- **Modules standards** :
    - `random`
    - `time`
    - `json`
    - `os`
    - `datetime`
- **Versioning** : Git / GitHub

---

## 🎯 Fonctionnalités principales

### 👤 Gestion des profils joueurs
- Création de profils
- Chargement de profils existants
- Sauvegarde automatique
- Suivi des scores et succès

### 🎮 Mini-jeux inclus
1. **Devine le nombre**
    - 3 niveaux de difficulté
    - Score basé sur les essais

2. **Calcul mental**
    - Opérations aléatoires
    - Chronomètre de 30 secondes
    - Score basé sur la rapidité et la justesse

3. **Pendu**
    - Mots aléatoires par thème
    - Affichage ASCII
    - Score basé sur les erreurs restantes

### 🏆 Système de points et succès
- Points attribués selon la performance
- Succès automatiques (première victoire, score parfait, etc.)
- Score total cumulatif

### 📊 Classements
- Top 10 global
- Classements par jeu
- Historique des parties

---

## 📂 Structure du projet
```
centre-jeux-multijoueur/
│
├── main.py # Programme principal
├── analysis.md # Analyse et conception du projet
├── README.md # Documentation du projet
│
├── data/
│ ├── profils/ # Profils joueurs (JSON)
│ └── classements.json # Classements globaux
│
└── assets/
└── pendu_ascii.txt # Dessins ASCII du pendu
```

---

## 💾 Format des données

### Exemple de profil joueur (JSON)

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

---

## ▶️ Installation et exécution

### 1️⃣ Prérequis

- Python 3.8 ou plus installé
- Git installé

### 2️⃣ Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/centre-jeux-multijoueur.git
cd centre-jeux-multijoueur
```

### 3️⃣ Lancer le programme

```bash
python main.py
```

---

## 🧪 Exemple d’utilisation

```markdown
=== CENTRE DE JEUX MULTIJOUEURS ===
1. Créer un profil
2. Charger un profil
3. Jouer
4. Classements
5. Succès
6. Règles
7. Quitter

> Choix : 3
> Jeu sélectionné : Pendu
> Mot trouvé ! +150 points
> Succès débloqué : Première victoire
```

---

## ⚠️ Gestion des erreurs

- Entrées utilisateur invalides
- Profils inexistants
- Fichiers absents ou corrompus
- Temps écoulé (calcul mental)
- Tentatives invalides (pendu)

👉 Toutes les erreurs sont gérées avec try/except et des messages clairs.

--- 

## 📌 Répartition du travail

- Conception & architecture : Mathis
- Développement jeux : Mathis
- Gestion des données & sauvegarde : Mathis
- Documentation & Git : Mathis

---

## 📅 Planning respecté

- Jour 1 : Analyse et conception
- Jour 2 : Développement des fonctions principales
- Jour 3 : Finalisation et gestion des erreurs
- Jour 4 : Documentation et présentation

---

## 👨‍🎓 Auteurs

Projet réalisé par :

Mathis
(Bachelor 1 – École IT)

---

## ✅ Objectifs pédagogiques atteints

- Développement d’un programme Python fonctionnel
- Structuration du code avec fonctions
- Gestion des entrées utilisateur
- Sauvegarde de données persistantes
- Documentation professionnelle
- Utilisation de Git avec commits réguliers