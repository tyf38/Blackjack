import random

# Valeurs des cartes
# 2 à 9 = valeurs normales
# 10, Valet, Dame, Roi = 10 (bûches)
# As = 11 (peut devenir 1 si nécessaire)

def créer_paquet():
    """Crée un paquet de 52 cartes"""
    return [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4


def tirer_carte(paquet):
    """Tire une carte au hasard et la retire du paquet"""
    carte = random.choice(paquet)
    paquet.remove(carte)
    return carte


def calcul_score(main):
    """Calcule le score de la main. Si le score dépasse 21 et qu'il y a un As (11), il devient un 1 automatiquement"""
    score = sum(main)

    # ajustement de l'As
    while score > 21 and 11 in main:
        index_as = main.index(11)
        main[index_as] = 1
        score = sum(main)

    return score


def afficher_main(nom, main, cacher_carte=False):
    """Affiche les cartes du joueur et cache une carte du croupier avec cacher_carte=True"""
    if cacher_carte:
        print(f"{nom} : [{main[0]}, ?]")
    else:
        print(f"{nom} : {main}, Score : {calcul_score(main)}\n")


def tour_joueur(paquet, main_joueur):
    """Gère le tour du joueur"""
    while True:
        score = calcul_score(main_joueur)

        afficher_main("Tes cartes", main_joueur)

        if score == 21:
            print("Blackjack !")
            break

        if score > 21:
            print("Tu dépasses 21. Tu as perdu.")
            break

        choix = input("Veux-tu une carte ou rester ? (c/r): ").lower()

        if choix == "c":
            nouvelle_carte = tirer_carte(paquet)
            main_joueur.append(nouvelle_carte)
            print(f"Tu tires : {nouvelle_carte}")

        elif choix == "r":
            print("Tu choisis de rester.")
            break

        else:
            print("Choix invalide. Tape 'c' ou 'r'.")


def tour_croupier(paquet, main_croupier):
    """Le croupier tire jusqu'à avoir au moins 17"""
    print("\nTour du croupier")

    while calcul_score(main_croupier) < 17:
        nouvelle_carte = tirer_carte(paquet)
        main_croupier.append(nouvelle_carte)
        print(f"Le croupier tire : {nouvelle_carte}")

    afficher_main("Croupier", main_croupier)


def determiner_gagnant(joueurs, main_croupier):
    """Compare les scores et annonce le résultat"""
    score_croupier = calcul_score(main_croupier)

    print("\nRésultat final\n")
    afficher_main("Croupier", main_croupier)

    for i, main_joueur in enumerate(joueurs):
        score_joueur = calcul_score(main_joueur)

        afficher_main(f"Joueur {i+1}", main_joueur)

        if score_joueur > 21:
            print(f"Joueur {i+1} a perdu.\n")

        elif score_croupier > 21:
            print(f"Joueur {i+1} a gagné ! (le croupier dépasse 21)\n")

        elif score_joueur > score_croupier:
            print(f"Joueur {i+1} a gagné !\n")

        elif score_joueur < score_croupier:
            print(f"Joueur {i+1} a perdu.\n")

        else:
            print(f"Joueur {i+1} : Égalité !\n")


def jouer_blackjack():
    """Lance une partie complète"""
    print("Bienvenue !\n")

    paquet = créer_paquet()

    # partie multijoueur
    while True:
        nb_joueurs = int(input("Combien de joueurs ? "))

        if nb_joueurs > 0:
            break
        else:
            print("Le nombre de joueurs doit être supérieur à 0.")
    
    joueurs = []

    for i in range(nb_joueurs):
        joueurs.append([tirer_carte(paquet), tirer_carte(paquet)])

    main_croupier = [tirer_carte(paquet), tirer_carte(paquet)]

    # affichage de départ
    for i, main_joueur in enumerate(joueurs):
        afficher_main(f"Joueur {i+1}", main_joueur)

    afficher_main("Croupier", main_croupier, cacher_carte=True)

    # tour des joueurs
    for i in range(nb_joueurs):
        print(f"\nTour du Joueur {i+1}")
        tour_joueur(paquet, joueurs[i])

    # tour du croupier
    if all(calcul_score(main_joueur) <= 21 for main_joueur in joueurs):
        tour_croupier(paquet, main_croupier)

    # résultat final
    determiner_gagnant(joueurs, main_croupier)


# pour lancer le jeu
jouer_blackjack()