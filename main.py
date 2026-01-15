import random
import time
import json
import os
from datetime import datetime


def creer_profil():
    """
    Crée un nouveau profil joueur et le sauvegarde en JSON.

    Demande à l'utilisateur un nom de joueur, initialise les données
    du profil et enregistre le fichier dans data/profils/.

    Retour :
        dict : profil joueur créé
    """
    try:
        nom = input("Entrez le nom du joueur : ").strip()

        if nom == "":
            print("❌ Le nom ne peut pas être vide.")
            return None

        # Création du dossier s'il n'existe pas
        os.makedirs("data/profils", exist_ok=True)

        chemin_fichier = f"data/profils/{nom}.json"

        if os.path.exists(chemin_fichier):
            print("⚠️ Un profil avec ce nom existe déjà.")
            return None

        profil = {
            "name": nom,
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "parties": [],
            "total_score": 0,
            "succes": []
        }

        with open(chemin_fichier, "w", encoding="utf-8") as fichier:
            json.dump(profil, fichier, indent=4, ensure_ascii=False)

        print(f"✅ Profil '{nom}' créé avec succès.")
        return profil

    except Exception as e:
        print("⚠️ Erreur lors de la création du profil :", e)
        return None



def charger_profil():
    """
    Charge un profil joueur existant depuis les fichiers de sauvegarde.

    Affiche la liste des profils disponibles et permet à l'utilisateur
    d'en sélectionner un.

    Retour :
        dict : profil joueur chargé
    """
    try:
        dossier_profils = "data/profils"

        if not os.path.exists(dossier_profils):
            print("⚠️ Aucun profil existant.")
            return None

        fichiers = [
            f for f in os.listdir(dossier_profils)
            if f.endswith(".json")
        ]

        if not fichiers:
            print("⚠️ Aucun profil trouvé.")
            return None

        print("\n👤 Profils disponibles :")
        for index, fichier in enumerate(fichiers, start=1):
            print(f"{index}. {fichier.replace('.json', '')}")

        choix = input("Choisissez un profil (numéro) : ")

        if not choix.isdigit():
            print("❌ Veuillez entrer un numéro valide.")
            return None

        choix = int(choix)

        if choix < 1 or choix > len(fichiers):
            print("❌ Choix hors limites.")
            return None

        chemin_fichier = os.path.join(dossier_profils, fichiers[choix - 1])

        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            profil = json.load(fichier)

        print(f"✅ Profil '{profil['name']}' chargé avec succès.")
        return profil

    except json.JSONDecodeError:
        print("❌ Erreur : fichier de profil corrompu.")
        return None

    except Exception as e:
        print("⚠️ Erreur lors du chargement du profil :", e)
        return None



def jouer_devinette(profil):
    """
    Lance le jeu 'Devine le nombre'.

    L'utilisateur doit deviner un nombre aléatoire selon
    la difficulté choisie. Le score dépend du nombre d'essais restants.

    Paramètres :
        profil (dict) : profil du joueur actuel

    Retour :
        int : score gagné
    """
    try:
        print("\n🎯 DEVINE LE NOMBRE")
        print("1. Facile (1 - 50)")
        print("2. Moyen (1 - 100)")
        print("3. Difficile (1 - 500)")

        difficulty = input("Choisissez la difficulté : ")

        if difficulty == "1":
            max_nb = 50
            max_try = 10
            base_score = 50
            selected_difficulty = "easy"
        elif difficulty == "2":
            max_nb = 100
            max_try = 7
            base_score = 100
            selected_difficulty = "average"
        elif difficulty == "3":
            max_nb = 500
            max_try = 5
            base_score = 200
            selected_difficulty = "hard"
        else:
            print("❌ Choix invalide.")
            return 0

        secret = random.randint(1, max_nb)
        left_try = max_try

        while left_try > 0:
            try:
                proposal = int(
                    input(f"Entrez un nombre (1 à {max_nb}) : ")
                )
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
                continue

            if proposal < 1 or proposal > max_nb:
                print("❌ Nombre hors limites.")
                continue

            left_try -= 1

            if proposal < secret:
                print("📉 Trop petit.")
            elif proposal > secret:
                print("📈 Trop grand.")
            else:

                performance = {
                    "difficulty": selected_difficulty,
                    "left_try": left_try
                }
                
                score = calculer_points("Devine le nombre", performance)
                print(f"🎉 Bravo ! Nombre trouvé. +{score} points")

                profil["total_score"] += score
                profil["parties"].append({
                    "game": "Devine le nombre",
                    "score": score,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })

                return score

        print(f"💀 Perdu ! Le nombre était {secret}.")
        return 0

    except Exception as e:
        print("⚠️ Erreur dans le jeu Devine le nombre :", e)
        return 0



def jouer_calcul(profil):
    """
    Lance le jeu de calcul mental.

    Génère des calculs aléatoires, lance un chronomètre de 30 secondes
    et calcule le score selon les bonnes réponses.

    Paramètres :
        profil (dict) : profil du joueur actuel

    Retour :
        int : score gagné
    """
    pass


def jouer_pendu(profil):
    """
    Lance le jeu du pendu.

    Sélectionne un mot aléatoire, affiche le pendu en ASCII,
    gère les lettres proposées et calcule le score final.

    Paramètres :
        profil (dict) : profil du joueur actuel

    Retour :
        int : score gagné
    """
    pass


def calculer_points(game, performance):
    """
    Calcule le nombre de points gagnés selon le jeu et la performance.

    Centralise la logique de calcul des scores pour éviter
    la duplication de code.

    Paramètres :
        game (str) : nom du jeu
        performance (dict) : données de performance du joueur

    Retour :
        int : nombre de points calculés
    """

    points = 0

    try:
        if game == "Devine le nombre":
            difficulty = performance.get("difficulty")

            match difficulty:
                case "easy":
                    points = 50
                case "average":
                    points = 100
                case "hard":
                    points = 200

            left_try = performance.get("left_try", 0)
            points += left_try * 10

        elif game == "Calcul mental":
            correct_answers = performance.get("correct_answers", 0)
            points = correct_answers * 10

        elif game == "Pendu":
            remaining_errors = performance.get("remaining_errors", 0)
            points = remaining_errors * 25

        else:
            points = 0

        return points

    except Exception as e:
        print("⚠️ Erreur lors du calcul des points :", e)
        return 0


def verifier_succes(profil):
    """
    Vérifie si des succès sont débloqués par le joueur.

    Analyse le profil (score, nombre de parties, performances)
    et ajoute les succès non encore obtenus.

    Paramètres :
        profil (dict) : profil du joueur

    Retour :
        None
    """
    pass


def afficher_classements():
    """
    Affiche les classements du centre de jeux.

    Montre le top 10 global, les classements par jeu
    et l'historique des parties.

    Paramètres :
        Aucun

    Retour :
        None
    """
    rankings_path = "data/classements.json"

    try:
        if not os.path.exists(rankings_path):
            print("📭 Aucun classement disponible.")
            return

        with open(rankings_path, "r", encoding="utf-8") as file:
            try:
                rankings = json.load(file)
            except json.JSONDecodeError:
                print("⚠️ Fichier de classement corrompu.")
                return

        players = rankings.get("players", {})

        if not players:
            print("📭 Aucun joueur enregistré dans le classement.")
            return

        # Tri des joueurs par score décroissant
        sorting_ranking = sorted(
            players.items(),
            key=lambda item: item[1],
            reverse=True
        )

        print("\n🏆 CLASSEMENT GLOBAL 🏆")
        print("-" * 30)
        for rank, (name, score) in enumerate(sorting_ranking, start=1):
            print(f"{rank}. {name} — {score} points")

        print("-" * 30)
    except Exception as e:
        print("⚠️ Erreur lors de l'affichage du classement :", e)



def sauvegarder_donnees(profil):
    """
    Sauvegarde les données du profil joueur et met à jour les classements.

    Écrit les données dans des fichiers JSON pour assurer
    la persistance des informations.

    Paramètres :
        profil (dict) : profil du joueur

    Retour :
        None
    """
    try:
        if profil is None:
            return

        os.makedirs("data/profils", exist_ok=True)

        profil_path = f"data/profils/{profil['name']}.json"
        with open(profil_path, "w", encoding="utf-8") as file:
            json.dump(profil, file, indent=4, ensure_ascii=False)

        rankings_path = "data/classements.json"

        if os.path.exists(rankings_path):
            with open(rankings_path, "r", encoding="utf-8") as file:
                try:
                    rankings = json.load(file)
                except json.JSONDecodeError:
                    rankings = {"players": {}}
        else:
            rankings = {"players": {}}


        rankings["players"][profil["name"]] = profil["total_score"]

        with open(rankings_path, "w", encoding="utf-8") as file:
            json.dump(rankings, file, indent=4, ensure_ascii=False)

        print("💾 Données sauvegardées avec succès.")


    except Exception as e:
        print("⚠️ Erreur lors de la sauvegarde des données :", e)


def main():
    """
    Fonction principale du programme.

    Affiche le menu principal du centre de jeux multijoueurs
    et redirige l'utilisateur vers les fonctionnalités choisies.
    """
    profil_actuel = None
    choix = ""

    while choix != "7":
        print("\n=== 🎮 CENTRE DE JEUX MULTIJOUEURS ===")
        print("1. Créer un profil")
        print("2. Charger un profil")
        print("3. Jouer")
        print("4. Classements")
        print("5. Succès")
        print("6. Règles")
        print("7. Quitter")

        choix = input("Votre choix : ")

        try:
            if choix == "1":
                profil_actuel = creer_profil()

            elif choix == "2":
                profil_actuel = charger_profil()

            elif choix == "3":
                if profil_actuel is None:
                    print("⚠️ Aucun profil chargé. Veuillez créer ou charger un profil.")
                else:
                    print("\n--- Choix du jeu ---")
                    print("1. Devine le nombre")
                    print("2. Calcul mental")
                    print("3. Pendu")

                    choix_jeu = input("Votre choix : ")

                    if choix_jeu == "1":
                        score = jouer_devinette(profil_actuel)
                    elif choix_jeu == "2":
                        score = jouer_calcul(profil_actuel)
                    elif choix_jeu == "3":
                        score = jouer_pendu(profil_actuel)
                    else:
                        print("❌ Choix de jeu invalide.")
                        continue

                    verifier_succes(profil_actuel)
                    sauvegarder_donnees(profil_actuel)

            elif choix == "4":
                afficher_classements()

            elif choix == "5":
                if profil_actuel is None:
                    print("⚠️ Aucun profil chargé.")
                else:
                    print("\n🏆 Succès débloqués :")
                    for succes in profil_actuel.get("succes", []):
                        print(f"- {succes}")

            elif choix == "6":
                print("\n📜 RÈGLES DU JEU")
                print("- Choisissez un jeu depuis le menu")
                print("- Gagnez des points selon vos performances")
                print("- Débloquez des succès automatiquement")

            elif choix == "7":
                print("👋 Merci d'avoir joué. À bientôt !")

            else:
                print("❌ Choix invalide. Veuillez entrer un nombre entre 1 et 7.")

        except Exception as e:
            print("⚠️ Une erreur est survenue :", e)



if __name__ == "__main__":
    main()
