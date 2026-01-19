import random
import time
import json
import os
from datetime import datetime

# ================== COULEURS ANSI ==================
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
REVERSE = "\033[7m"


def creer_profil():
    """
    Crée un nouveau profil joueur et le sauvegarde en JSON.

    Demande à l'utilisateur un nom de joueur, initialise les données
    du profil et enregistre le fichier dans data/profils/.

    Retour :
        dict : profil joueur créé
    """
    try:
        print(f"\n{CYAN}{BOLD}👤 CRÉER UN NOUVEAU PROFIL{RESET}")
        nom = input(f"{MAGENTA}Entrez le nom du joueur : {RESET}").strip()

        if nom == "":
            print(f"{RED}❌ Le nom ne peut pas être vide.{RESET}")
            return None

        # Création du dossier s'il n'existe pas
        os.makedirs("data/profils", exist_ok=True)

        chemin_fichier = f"data/profils/{nom}.json"

        if os.path.exists(chemin_fichier):
            print(f"{YELLOW}⚠️ Un profil avec ce nom existe déjà.{RESET}")
            return None

        profil = {
            "name": nom,
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "parties": [],
            "total_score": 0,
            "succes": [],
        }

        with open(chemin_fichier, "w", encoding="utf-8") as fichier:
            json.dump(profil, fichier, indent=4, ensure_ascii=False)

        print(f"{GREEN}✅ Profil '{nom}' créé avec succès.{RESET}")
        print(f"{CYAN}🔄️ Chargement du profil en cours...{RESET}")
        time.sleep(2)
        print("\033c", end="")  # clear terminal

        return profil

    except Exception as e:
        print(f"{RED}⚠️ Erreur lors de la création du profil :{RESET}", e)
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
            print(f"{RED}⚠️ Aucun profil existant.{RESET}")
            return None

        fichiers = [f for f in os.listdir(dossier_profils) if f.endswith(".json")]

        if not fichiers:
            print(f"{RED}⚠️ Aucun profil trouvé.{RESET}")
            return None

        # 🔹 Affichage avec couleurs
        print(f"\n{CYAN}{BOLD}👤 Profils disponibles :{RESET}")
        for index, fichier in enumerate(fichiers, start=1):
            print(f"{YELLOW}{index}. {fichier.replace('.json', '')}{RESET}")

        choix = input(f"{MAGENTA}Choisissez un profil (numéro) : {RESET}").strip()

        if not choix.isdigit():
            print(f"{RED}❌ Veuillez entrer un numéro valide.{RESET}")
            return None

        choix = int(choix)

        if choix < 1 or choix > len(fichiers):
            print(f"{RED}❌ Choix hors limites.{RESET}")
            return None

        chemin_fichier = os.path.join(dossier_profils, fichiers[choix - 1])

        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            profil = json.load(fichier)

        print(f"{GREEN}✅ Profil '{profil['name']}' chargé avec succès.{RESET}")
        print(f"{CYAN}🔄️ Chargement en cours...{RESET}")
        time.sleep(2)  # réduction du temps pour une UX plus fluide
        print("\033c", end="")  # clear terminal
        return profil

    except json.JSONDecodeError:
        print(f"{RED}❌ Erreur : fichier de profil corrompu.{RESET}")
        return None

    except Exception as e:
        print(f"{RED}⚠️ Erreur lors du chargement du profil :{RESET}", e)
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
        print(f"\n{CYAN}{BOLD}🎯 DEVINE LE NOMBRE{RESET}")
        print(f"{YELLOW}1. Facile (1 - 50){RESET}")
        print(f"{YELLOW}2. Moyen (1 - 100){RESET}")
        print(f"{YELLOW}3. Difficile (1 - 500){RESET}")

        difficulty = input(f"{CYAN}Choisissez la difficulté : {RESET}")

        if difficulty == "1":
            max_nb = 50
            max_try = 10
            selected_difficulty = "easy"
        elif difficulty == "2":
            max_nb = 100
            max_try = 7
            selected_difficulty = "average"
        elif difficulty == "3":
            max_nb = 500
            max_try = 5
            selected_difficulty = "hard"
        else:
            print(f"{RED}❌ Choix invalide.{RESET}")
            return 0

        secret = random.randint(1, max_nb)
        left_try = max_try

        while left_try > 0:
            # 🔹 Clear à chaque essai
            print("\033c", end="")

            print(f"{CYAN}{BOLD}🎯 DEVINE LE NOMBRE{RESET}")
            print(f"{YELLOW}Nombre d'essais restants : {left_try}{RESET}")

            try:
                proposal = int(
                    input(f"{MAGENTA}Entrez un nombre (1 à {max_nb}) : {RESET}")
                )
            except ValueError:
                print(f"{RED}❌ Veuillez entrer un nombre valide.{RESET}")
                time.sleep(1)
                continue

            if proposal < 1 or proposal > max_nb:
                print(f"{RED}❌ Nombre hors limites.{RESET}")
                time.sleep(1)
                continue

            left_try -= 1

            if proposal < secret:
                print(f"{BLUE}📉 Trop petit.{RESET}")
                time.sleep(1)
            elif proposal > secret:
                print(f"{BLUE}📈 Trop grand.{RESET}")
                time.sleep(1)
            else:
                performance = {"difficulty": selected_difficulty, "left_try": left_try}

                score = calculer_points("Devine le nombre", performance)
                print(f"{GREEN}🎉 Bravo ! Nombre trouvé. +{score} points{RESET}")

                profil["total_score"] = profil.get("total_score", 0) + score
                profil.setdefault("parties", []).append(
                    {
                        "game": "Devine le nombre",
                        "score": score,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                    }
                )

                return score

        print(f"{RED}💀 Perdu ! Le nombre était {secret}.{RESET}")
        return 0

    except Exception as e:
        print(f"{RED}⚠️ Erreur dans le jeu Devine le nombre :{RESET}", e)
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
    try:
        print(f"\n{CYAN}{BOLD}🧠 CALCUL MENTAL — 30 secondes{RESET}")
        time_limit = 30
        correct_answers = 0
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            remaining = int(time_limit - elapsed)
            if remaining <= 0:
                print(f"\n{RED}⏱️ Temps écoulé !{RESET}")
                break

            # 🔹 Clear à chaque tour
            print("\033c", end="")
            print(
                f"{CYAN}{BOLD}🧠 CALCUL MENTAL — Temps restant : {YELLOW}{remaining} s{RESET}{CYAN}{BOLD}{RESET}"
            )

            # Génération du calcul
            op = random.choice(["+", "-", "*"])
            if op == "+":
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                solution = a + b
            elif op == "-":
                a = random.randint(1, 100)
                b = random.randint(1, a)
                solution = a - b
            else:  # "*"
                a = random.randint(1, 12)
                b = random.randint(1, 12)
                solution = a * b

            try:
                answer = input(f"{MAGENTA}Calcule : {a} {op} {b} = {RESET}").strip()
                # vérifier si le temps est écoulé après la saisie
                if time.time() - start_time > time_limit:
                    print(f"\n{RED}⏱️ Temps écoulé pendant la réponse.{RESET}")
                    break

                reponse_int = int(answer)
                if reponse_int == solution:
                    print(f"{GREEN}✅ Correct !{RESET}")
                    correct_answers += 1
                else:
                    print(f"{RED}❌ Incorrect. Réponse : {solution}{RESET}")

                time.sleep(1)  # petite pause pour voir le résultat avant le clear

            except ValueError:
                print(f"{RED}❌ Entrée invalide. Veuillez entrer un nombre.{RESET}")
                time.sleep(1)
                if time.time() - start_time > time_limit:
                    print(f"\n{RED}⏱️ Temps écoulé !{RESET}")
                    break
                continue

        # Calcul des points
        points = calculer_points("Calcul mental", {"correct_answers": correct_answers})
        print(
            f"\n{GREEN}🎯 Résultat : {correct_answers} bonnes réponses — +{points} points{RESET}"
        )

        # mise à jour du profil
        profil["total_score"] = profil.get("total_score", 0) + points
        profil.setdefault("parties", []).append(
            {
                "game": "Calcul mental",
                "score": points,
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        )

        return points

    except Exception as e:
        print(f"{RED}⚠️ Erreur dans le jeu Calcul mental :{RESET}", e)
        return 0


def charger_mots():
    """
    Charge un mot aléatoire depuis data/word.json en gérant les thèmes.

    Retour :
        str : un mot (fallback aléatoire si erreur)
    """
    path = "data/word.json"
    fallback = [
        "ordinateur",
        "python",
        "developpeur",
        "framework",
        "algorithm",
        "memoire",
        "reseau",
        "securite",
        "interface",
        "fonction",
    ]

    try:
        if not os.path.exists(path):
            print(
                f"{RED}⚠️ Fichier {path} introuvable. Renvoi d'un mot par défaut.{RESET}"
            )
            return random.choice(fallback)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict) or not data:
            print(
                f"{RED}⚠️ Contenu de {path} invalide (attendu dict non vide). Renvoi d'un mot par défaut.{RESET}"
            )
            return random.choice(fallback)

        # Construire dictionnaire thème -> liste de mots nettoyés
        clean_data = {}
        for theme, lst in data.items():
            if isinstance(lst, list):
                mots = [w.strip() for w in lst if isinstance(w, str) and w.strip()]
                if mots:
                    clean_data[theme] = mots

        if not clean_data:
            print(
                f"{RED}⚠️ Aucun mot valide trouvé dans les thèmes. Renvoi d'un mot par défaut.{RESET}"
            )
            return random.choice(fallback)

        themes = sorted(clean_data.keys())

        # 🔹 Clear avant le menu
        print("\033c", end="")

        # Affichage menu thèmes
        print(f"{CYAN}{BOLD}🔤 Thèmes disponibles :{RESET}")
        for i, t in enumerate(themes, start=1):
            print(f"{YELLOW}{i}. {t} ({len(clean_data.get(t, []))} mots){RESET}")
        print(f"{YELLOW}0. Aléatoire parmi tous les thèmes{RESET}")

        choice = input(
            f"{CYAN}Choisissez un thème (numéro ou nom, 0 pour aléatoire) : {RESET}"
        ).strip()

        # Cas aléatoire / aucun choix
        if choice == "" or choice == "0":
            all_words = [w for lst in clean_data.values() for w in lst]
            return random.choice(all_words) if all_words else random.choice(fallback)

        # Si choix numérique -> index
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(themes):
                selected = themes[idx]
                mots = clean_data.get(selected, [])
                return random.choice(mots) if mots else random.choice(fallback)
            else:
                print(f"{RED}❌ Choix hors limites, mot aléatoire sélectionné.{RESET}")
                all_words = [w for lst in clean_data.values() for w in lst]
                return (
                    random.choice(all_words) if all_words else random.choice(fallback)
                )

        # Sinon, tentative de correspondance sur nom de thème (insensible à la casse)
        lowered_map = {t.lower(): t for t in themes}
        if choice.lower() in lowered_map:
            selected = lowered_map[choice.lower()]
            mots = clean_data.get(selected, [])
            return random.choice(mots) if mots else random.choice(fallback)

        # Choix invalide
        print(f"{RED}❌ Choix invalide, mot aléatoire sélectionné.{RESET}")
        all_words = [w for lst in clean_data.values() for w in lst]
        return random.choice(all_words) if all_words else random.choice(fallback)

    except json.JSONDecodeError:
        print(f"{RED}❌ Erreur JSON dans {path}. Renvoi d'un mot par défaut.{RESET}")
        return random.choice(fallback)
    except Exception as e:
        print(f"{RED}⚠️ Erreur lors du chargement des mots :{RESET}", e)
        return random.choice(fallback)


def jouer_pendu(profil):
    """
    Lance le jeu du pendu.

    Sélectionne un mot aléatoire (via charger_mots), affiche le pendu en ASCII,
    gère les lettres proposées et calcule le score final.

    Paramètres :
        profil (dict) : profil du joueur actuel

    Retour :
        int : score gagné
    """
    try:
        mot_choisi = charger_mots()  # retourne un seul mot (string)
        if not mot_choisi:
            print(f"{RED}⚠️ Aucune liste de mots disponible.{RESET}")
            return 0

        secret_word = mot_choisi.lower()
        secret_letters = set([c for c in secret_word if c.isalpha()])
        letters_found = set()
        proposed_letters = set()

        max_errors = 6
        errors = 0

        ascii_pendu = [
            """


            =========
            """,
            """

            |
            |
            |
            |
            =========
            """,
            """
            +---+
            |
            |
            |
            |
            =========
            """,
            """
            +---+
            |   O
            |
            |
            |
            =========
            """,
            """
            +---+
            |   O
            |   |
            |
            |
            =========
            """,
            """
            +---+
            |   O
            |  /|\\
            |
            |
            =========
            """,
            """
            +---+
            |   O
            |  /|\\
            |  / \\
            |
            =========
            """,
        ]

        print(f"\n{CYAN}{BOLD}🪤 PENDU — Trouvez le mot !{RESET}")

        while errors < max_errors and not secret_letters.issubset(letters_found):
            # 🔹 Clear du terminal à chaque tour
            print("\033c", end="")

            hidden_word = " ".join(
                [
                    c if (not c.isalpha()) or (c in letters_found) else "_"
                    for c in secret_word
                ]
            )
            print(f"{MAGENTA}{ascii_pendu[min(errors, len(ascii_pendu) - 1)]}{RESET}")
            print(f"\nMot : {YELLOW}{hidden_word}{RESET}")
            print(
                f"Lettres proposées : {', '.join(sorted(proposed_letters))}"
                if proposed_letters
                else f"Lettres proposées : {YELLOW}(aucune){RESET}"
            )
            print(f"Erreurs : {RED}{errors}{RESET} / {max_errors}")

            proposal = (
                input(f"{CYAN}Proposez une lettre (ou le mot entier): {RESET}")
                .strip()
                .lower()
            )
            if not proposal:
                print(f"{RED}❌ Entrée vide.{RESET}")
                continue

            if len(proposal) > 1:
                if proposal == secret_word:
                    letters_found.update(secret_letters)
                    print(
                        f"{GREEN}🎉 Bravo ! Vous avez trouvé le mot '{secret_word}'.{RESET}"
                    )
                    break
                else:
                    errors += 1
                    print(
                        f"{RED}❌ Mauvaise réponse. Tentative mot incorrecte. ({errors}/{max_errors}){RESET}"
                    )
                    continue

            letter = proposal[0]
            if not letter.isalpha():
                print(f"{RED}❌ Veuillez entrer une lettre valide.{RESET}")
                continue

            if letter in proposed_letters:
                print(f"{YELLOW}⚠️ Lettre déjà proposée.{RESET}")
                continue

            proposed_letters.add(letter)

            if letter in secret_letters:
                letters_found.add(letter)
                print(f"{GREEN}✅ Lettre correcte !{RESET}")
            else:
                errors += 1
                print(f"{RED}❌ Lettre incorrecte. ({errors}/{max_errors}){RESET}")

        # 🔹 Résultat final
        print("\033c", end="")  # clear avant d’afficher le mot final

        if secret_letters.issubset(letters_found):
            remaining_errors = max_errors - errors
            points = calculer_points("Pendu", {"remaining_errors": remaining_errors})
            print(
                f"{GREEN}🏆 Mot trouvé : {secret_word} — +{points} points (erreurs restantes : {remaining_errors}){RESET}"
            )

            profil["total_score"] = profil.get("total_score", 0) + points
            profil.setdefault("parties", []).append(
                {
                    "game": "Pendu",
                    "score": points,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                }
            )

            return points
        else:
            print(f"{MAGENTA}{ascii_pendu[min(errors, len(ascii_pendu)-1)]}{RESET}")
            print(f"\n{RED}💀 Perdu ! Le mot était : {secret_word}{RESET}")
            profil.setdefault("parties", []).append(
                {
                    "game": "Pendu",
                    "score": 0,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                }
            )
            return 0

    except Exception as e:
        print(f"{RED}⚠️ Erreur dans le jeu Pendu :{RESET}", e)
        return 0


def jouer_rpsls(profil):
    """
    Lance le jeu Pierre-Feuille-Ciseaux étendu à 15 coups.

    Le score dépend uniquement du nombre de victoires.
    Les défaites et égalités ne rapportent aucun point.

    Paramètres :
        profil (dict) : profil du joueur actuel

    Retour :
        int : score gagné
    """
    try:
        print(f"\n{CYAN}{BOLD}🔥 PIERRE-FEUILLE-CISEAUX ULTIME (15 COUPS) 🔥{RESET}")

        MOVES = [
            "Pierre",
            "Pistolet",
            "Eclair",
            "Demon",
            "Dragon",
            "Eau",
            "Air",
            "Papier",
            "Eponge",
            "Loup",
            "Arbre",
            "Humain",
            "Serpent",
            "Ciseau",
            "Feu",
        ]

        TOTAL = len(MOVES)
        WIN_RANGE = TOTAL // 2  # 7
        rounds = 5
        wins = 0

        for round_num in range(1, rounds + 1):
            print(f"\n{YELLOW}--- Tour {round_num} ---{RESET}")
            print("Choisissez votre coup :")

            for i, move in enumerate(MOVES, start=1):
                print(f"{i}. {move}")

            choice = input("Votre choix (numéro) : ").strip()

            if not choice.isdigit():
                print(f"{RED}❌ Choix invalide.{RESET}")
                continue

            idx = int(choice) - 1
            if idx < 0 or idx >= TOTAL:
                print(f"{RED}❌ Choix invalide.{RESET}")
                continue

            player_move = MOVES[idx]
            computer_move = random.choice(MOVES)

            print(f"\n👤 Vous : {BOLD}{player_move}{RESET}")
            print(f"💻 Ordinateur : {BOLD}{computer_move}{RESET}")

            p = MOVES.index(player_move)
            c = MOVES.index(computer_move)
            distance = (p - c) % TOTAL

            if distance == 0:
                print(f"{YELLOW}⚖️ Égalité.{RESET}")
            elif 1 <= distance <= WIN_RANGE:
                print(f"{GREEN}🎉 Victoire !{RESET}")
                wins += 1
            else:
                print(f"{RED}💀 Défaite.{RESET}")

        # 📊 PERFORMANCE (même logique que jouer_devinette)
        performance = {"wins": wins, "rounds": rounds}

        score = calculer_points("Pierre-Feuille-Ciseaux (15)", performance)

        print(
            f"\n{CYAN}{BOLD}🏆 Résultat : {wins} victoire(s) — +{score} points{RESET}"
        )

        # 📦 Mise à jour du profil
        profil["total_score"] += score
        profil["parties"].append(
            {
                "game": "Pierre-Feuille-Ciseaux (15)",
                "score": score,
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        )

        return score

    except Exception as e:
        print(f"{RED}⚠️ Erreur lors de l'execution du jeu :{RESET}", e)
        return 0


def calculer_points(game, performance):
    """
    Points gagnés selon le jeu et la performance.

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

        elif game == "Pierre-Feuille-Ciseaux (15)":
            wins = performance.get("wins", 0)
            rounds = performance.get("rounds", 0)

            # Points de base : 10 points par victoire
            points = wins * 10

            # Bonus selon le nombre de victoires
            if wins >= 5:
                points += 30
            elif wins == 4:
                points += 20
            elif wins == 3:
                points += 10

        else:
            points = 0

        return points

    except Exception as e:
        print(f"{RED}⚠️ Erreur lors du calcul des points :{RESET}", e)
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
    try:
        if profil is None:
            return

        profil.setdefault("succes", [])
        succes_list = profil["succes"]

        parties = profil.get("parties", [])
        total_score = profil.get("total_score", 0)
        nb_parties = len(parties)

        counts = {}
        for p in parties:
            game = p.get("game", "Inconnu")
            counts[game] = counts.get(game, 0) + 1

        new = []

        # 🔹 Succès selon le nombre de parties
        thresholds_parties = [
            (1, "Premier jeu"),
            (5, "Joueur assidu (5 parties)"),
            (20, "Vétéran (20 parties)"),
            (50, "Marathonien (50 parties)"),
            (100, "Légende vivante (100 parties)"),
        ]
        for threshold, name in thresholds_parties:
            if nb_parties >= threshold and name not in succes_list:
                succes_list.append(name)
                new.append(name)

        # 🔹 Succès selon le score total
        threshold_score = [
            (100, "Scoreur (100 points)"),
            (500, "Champion (500 points)"),
            (1000, "Maître du jeu (1000 points)"),
            (5000, "Légende (5000 points)"),
        ]
        for threshold, name in threshold_score:
            if total_score >= threshold and name not in succes_list:
                succes_list.append(name)
                new.append(name)

        # 🔹 Succès par jeu spécifique
        target_games = [
            ("Devine le nombre", 5, "Spécialiste Devine le nombre (5 parties)"),
            ("Calcul mental", 5, "Calculateur (5 parties)"),
            ("Pendu", 5, "Pendu expert (5 parties)"),
            ("Pierre-Feuille-Ciseaux (15)", 5, "Maître du RPSLS (5 parties)"),
        ]
        for game, threshold, name in target_games:
            if counts.get(game, 0) >= threshold and name not in succes_list:
                succes_list.append(name)
                new.append(name)

        # Affichage des nouveaux succès
        if new:
            print(f"\n{CYAN}{BOLD}🏅 Nouveaux succès débloqués :{RESET}")
            for s in new:
                print(f"{GREEN}- {s}{RESET}")

    except Exception as e:
        print(f"{RED}⚠️ Erreur lors de la vérification des succès :{RESET}", e)


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
            print(f"{YELLOW}📭 Aucun classement disponible.{RESET}")
            return

        with open(rankings_path, "r", encoding="utf-8") as file:
            try:
                rankings = json.load(file)
            except json.JSONDecodeError:
                print(f"{RED}⚠️ Fichier de classement corrompu.{RESET}")
                return

        players = rankings.get("players", {})

        if not players:
            print(f"{YELLOW}📭 Aucun joueur enregistré dans le classement.{RESET}")
            return

        # Tri des joueurs par score décroissant
        sorting_ranking = sorted(
            players.items(), key=lambda item: item[1], reverse=True
        )

        print(f"\n{CYAN}{BOLD}🏆 CLASSEMENT GLOBAL 🏆{RESET}")
        print(f"{MAGENTA}" + "-" * 40 + f"{RESET}")

        for rank, (name, score) in enumerate(sorting_ranking, start=1):
            color = GREEN if rank == 1 else CYAN if rank <= 3 else RESET
            print(f"{color}{rank}. {name} — {score} points{RESET}")

        print(f"{MAGENTA}" + "-" * 40 + f"{RESET}")

    except Exception as e:
        print(f"{RED}⚠️ Erreur lors de l'affichage du classement :{RESET}", e)


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

        print(f"{CYAN}💾 Sauvegarde des données en cours...{RESET}")

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
                    print(
                        f"{YELLOW}⚠️ Classements corrompus, réinitialisation...{RESET}"
                    )
                    rankings = {"players": {}}
        else:
            rankings = {"players": {}}

        rankings["players"][profil["name"]] = profil["total_score"]

        with open(rankings_path, "w", encoding="utf-8") as file:
            json.dump(rankings, file, indent=4, ensure_ascii=False)

        print(f"{GREEN}✅ Données sauvegardées avec succès.{RESET}")
        print(f"{CYAN}🔄 Chargement en cours...{RESET}")
        time.sleep(2)
        print("\033c", end="")

    except Exception as e:
        print(f"{RED}⚠️ Erreur lors de la sauvegarde des données :{RESET}", e)


def main():
    """
    Fonction principale du programme.

    Affiche le menu principal du centre de jeux multijoueurs
    et redirige l'utilisateur vers les fonctionnalités choisies.
    """

    profil = None
    choice = ""

    while choice != "5":
        if not profil:
            print(f"{CYAN}{BOLD}👋 Bienvenue au Centre de Jeux Multijoueurs !{RESET}")
            print(f"{BLUE}1.{RESET} Créer un profil")
            print(f"{BLUE}2.{RESET} Charger un profil")
            print(f"{RED}5.{RESET} Quitter")

            choice = input(f"{YELLOW}Votre choix : {RESET}")

            try:
                match choice:
                    case "1":
                        profil = creer_profil()
                    case "2":
                        profil = charger_profil()
                    case "5":
                        print(f"{GREEN}👋 À bientôt !{RESET}")
                    case _:
                        print(f"{RED}❌ Choix invalide.{RESET}")

            except Exception as e:
                print(f"{RED}⚠️ Une erreur est survenue :{RESET}", e)

        else:
            print(f"\n{MAGENTA}{BOLD}=== 🎮 CENTRE DE JEUX MULTIJOUEURS ==={RESET}")
            print(f"{BLUE}1.{RESET} Jouer")
            print(f"{BLUE}2.{RESET} Classements")
            print(f"{BLUE}3.{RESET} Succès")
            print(f"{BLUE}4.{RESET} Règles")
            print(f"{RED}5.{RESET} Quitter")

            choice = input(f"{YELLOW}Votre choix : {RESET}")

            try:
                if choice not in {"1", "2", "3", "4", "5"}:
                    print(
                        f"{RED}❌ Choix invalide. Veuillez entrer un nombre entre 1 et 5.{RESET}"
                    )
                    continue
                else:
                    print("\033c", end="")

                match choice:
                    case "1":
                        print(f"{CYAN}🔄 Récupération des jeux...{RESET}")
                        time.sleep(2)
                        print("\033c", end="")

                        print(f"{BOLD}--- Choix du jeu ---{RESET}")
                        print(f"{BLUE}1.{RESET} Devine le nombre")
                        print(f"{BLUE}2.{RESET} Calcul mental")
                        print(f"{BLUE}3.{RESET} Pendu")
                        print(f"{BLUE}4.{RESET} Pierre-Feuille-Ciseaux (15 coups)")

                        game_choice = input(f"{YELLOW}Votre choix : {RESET}")

                        print(f"{CYAN}🔄 Chargement du jeu en cours...{RESET}")
                        time.sleep(2)
                        print("\033c", end="")

                        match game_choice:
                            case "1":
                                score = jouer_devinette(profil)
                            case "2":
                                score = jouer_calcul(profil)
                            case "3":
                                score = jouer_pendu(profil)
                            case "4":
                                score = jouer_rpsls(profil)
                            case _:
                                print(f"{RED}❌ Jeu invalide.{RESET}")
                                continue

                        verifier_succes(profil)
                        sauvegarder_donnees(profil)

                    case "2":
                        print(f"{CYAN}🔄 Chargement des classements...{RESET}")
                        time.sleep(2)
                        print("\033c", end="")
                        afficher_classements()

                    case "3":
                        print(f"{CYAN}🔄 Chargement des succès...{RESET}")
                        time.sleep(2)
                        print("\033c", end="")
                        print(f"\n{GREEN}{BOLD}🏆 Succès débloqués :{RESET}")
                        for succes in profil.get("succes", []):
                            print(f"{GREEN}- {succes}{RESET}")

                    case "4":
                        print(f"{CYAN}🔄 Chargement des règles...{RESET}")
                        time.sleep(2)
                        print("\033c", end="")
                        print(f"\n{BOLD}📜 RÈGLES DU JEU{RESET}")
                        print(f"{YELLOW}- Choisissez un jeu depuis le menu{RESET}")
                        print(
                            f"{YELLOW}- Gagnez des points selon vos performances{RESET}"
                        )
                        print(f"{YELLOW}- Débloquez des succès automatiquement{RESET}")

                    case "5":
                        print(f"{GREEN}{BOLD}👋 Merci d'avoir joué. À bientôt !{RESET}")

            except Exception as e:
                print(f"{RED}⚠️ Une erreur est survenue :{RESET}", e)


if __name__ == "__main__":
    main()
