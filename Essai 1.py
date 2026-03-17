# JEU DU BLACKJACK (sans l'interface et les tours joueur/croupier et le reste)

import random

# paquet de cartes
cartes = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 4

def tirer_carte(paquet):
    carte = random.choice(paquet)
    paquet.remove(carte)  # on retire la carte du paquet
    return carte

def calcul_score(main):
    score = sum(main)
    # gérer l'as (11 devient 1 si on dépasse 21)
    while score > 21 and 11 in main:
        main[main.index(11)] = 1
        score = sum(main)
    return score

# mains des joueurs
joueur = []
croupier = []

# distribution de départ
joueur.append(tirer_carte(cartes))
joueur.append(tirer_carte(cartes))

croupier.append(tirer_carte(cartes))
croupier.append(tirer_carte(cartes))

# tour du joueur
while True:
    print("Tes cartes :", joueur, "Score :", calcul_score(joueur))
    print("Carte visible du croupier :", croupier[0])

    if calcul_score(joueur) > 21:
        print("Tu as dépassé 21, tu perds.")
        break

    choix = input("Carte ou rester ? (c/r) : ")

    if choix == "c":
        joueur.append(tirer_carte(cartes))
    else:
        break


# tour du croupier
while calcul_score(croupier) < 17:
    croupier.append(tirer_carte(cartes))

print("\nCartes du croupier :", croupier, "Score :", calcul_score(croupier))


# résultat final
score_joueur = calcul_score(joueur)
score_croupier = calcul_score(croupier)

if score_joueur > 21:
    print("Tu as perdu.")
elif score_croupier > 21 or score_joueur > score_croupier:
    print("Tu as gagné.")
elif score_joueur == score_croupier:
    print("Égalité.")
else:
    print("Le croupier gagne.")


# essai
import random

# paquet de 52 cartes
# 2 à 9 = valeurs normales
# 10, Valet, Dame, Roi = 10 (bûches)
# As = 11 (peut devenir 1)
cartes = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 4

def tirer_carte(paquet):
    """Tire une carte au hasard"""
    carte = random.choice(paquet)
    paquet.remove(carte)  # on retire la carte du paquet
    return carte

def calcul_score(main):
    """Calcule le score de la main et ajuste l'As si nécessaire"""
    score = sum(main)
    while score > 21 and 11 in main:
        main[main.index(11)] = 1
        score = sum(main)
    return score

# distribution de départ
joueur = [tirer_carte(cartes), tirer_carte(cartes)]
croupier = [tirer_carte(cartes), tirer_carte(cartes)]

# tour du joueur
while True:
    print("\nTes cartes :", joueur, "Score :", calcul_score(joueur))
    print("Carte visible du croupier :", croupier[0])

    score_j = calcul_score(joueur)
    if score_j == 21:
        print("Blackjack !")
        break
    elif score_j > 21:
        print("Tu as dépassé 21, tu perds.")
        break

    choix = input("Carte ou rester ? (c/r): ").lower()
    if choix == "c":
        joueur.append(tirer_carte(cartes))
    elif choix == "r":
        print("Tu as choisi de rester.")
    else:
        print("Choix invalide, tape 'c' pour carte ou 'r' pour rester.")

# tour du croupier
if calcul_score(joueur) <= 21:  # seulement si le joueur n'a pas brûlé
    while calcul_score(croupier) < 17:
        croupier.append(tirer_carte(cartes))

# affichage final
print("\nCartes joueur :", joueur, "Score :", calcul_score(joueur))
print("Cartes croupier :", croupier, "Score :", calcul_score(croupier))

# détermination du gagnant
score_joueur = calcul_score(joueur)
score_croupier = calcul_score(croupier)

if score_joueur > 21:
    print("Tu as perdu.")
elif score_croupier > 21:
    print("Le croupier dépasse 21. Tu gagnes.")
elif score_joueur > score_croupier:
    print("Tu gagnes.")
elif score_joueur < score_croupier:
    print("Le croupier gagne.")
else:
    print("Égalité.")