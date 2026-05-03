import tkinter as tk
from tkinter import messagebox
import random

# =========================
# ===== APPLICATION =====
# =========================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("500x400")
        self.current_frame = None
        self.show_menu()

    def clear(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_menu(self):
        self.clear()
        self.current_frame = Menu(self)
    
    def show_classique(self):
        self.clear()
        self.current_frame = BlackjackClassique(self)

    def show_1v1(self):
        self.clear()
        self.current_frame = Blackjack1v1(self)


# =========================
# ===== MENU =====
# =========================

class Menu(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.pack(fill="both", expand=True)

        tk.Label(self, text="BLACKJACK", font=("Arial", 20, "bold")).pack(pady=20)

        tk.Button(self, text="Mode Classique", width=25,
                  command=app.show_classique).pack(pady=10)

        tk.Button(self, text="Mode 1v1", width=25,
                  command=app.show_1v1).pack(pady=10)


# =========================
# ===== MODE CLASSIQUE =====
# =========================

def create_deck():
    values = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    deck = [(str(v), v) for v in values for _ in range(4)]
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    score = sum(card[1] for card in hand)
    aces = sum(1 for card in hand if card[1] == 11)
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score


class BlackjackClassique(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.pack(fill="both", expand=True)
        self.app = app

        self.player_label = tk.Label(self, font=("Arial", 14))
        self.player_label.pack()

        self.dealer_label = tk.Label(self, font=("Arial", 14))
        self.dealer_label.pack()

        self.result_label = tk.Label(self, font=("Arial", 16))
        self.result_label.pack(pady=10)

        self.button_hitt=tk.Button(self, text="Tirer", command=self.hit, state='active')
        self.button_hitt.pack(padx=20)
        
        self.button_stayy=tk.Button(self, text="Rester", command=self.stand, state='active')
        self.button_stayy.pack(padx=20)

        self.btn_restartT = tk.Button(self, text="Nouvelle partie", command=self.nouvelle_partie)
        self.btn_restartT.pack(pady=20)
        
        tk.Button(self, text="Retour menu", command=self.app.show_menu).pack()

        self.new_game()

    def new_game(self):
        self.deck = create_deck()
        self.player = [self.deck.pop(), self.deck.pop()]
        self.dealer = [self.deck.pop(), self.deck.pop()]
        self.result_label.config(text="")
        self.update_display(True)

    def update_display(self, hide=True):
        p = " | ".join(c[0] for c in self.player)
        d = self.dealer[0][0] + " ?" if hide else " | ".join(c[0] for c in self.dealer)

        self.player_label.config(text=f"Ta main : {p} |({calculate_score(self.player)})")
        self.dealer_label.config(text=f"Croupier : {d} ")

    def hit(self):
        self.player.append(self.deck.pop())
        if calculate_score(self.player) > 21:
            self.end(f"Tu as perdu, le croupier avait {calculate_score(self.dealer)}")
            self.button_hitt.config(state='disabled')
            self.button_stayy.config(state='disabled')
        self.update_display(True)

    def stand(self):
        while calculate_score(self.dealer) < 17:
            self.dealer.append(self.deck.pop())

        self.update_display(False)

        p = calculate_score(self.player)
        d = calculate_score(self.dealer)

        if d > 21 or p > d:
            self.end(f"Tu gagnes, le croupier avait {calculate_score(self.dealer)}")
            self.button_hitt.config(state='disabled')
            self.button_stayy.config(state='disabled')
        elif p < d:
            self.end(f"Tu perds, le croupier avait {calculate_score(self.dealer)}")
            self.button_hitt.config(state='disabled')
            self.button_stayy.config(state='disabled')
        else:
            self.end(f"Egalite, le croupier avait {calculate_score(self.dealer)}")
            self.button_hitt.config(state='disabled')
            self.button_stayy.config(state='disabled')

    def end(self, msg):
        self.result_label.config(text=msg)

    def nouvelle_partie(self):
        self.new_game()
        self.update()
        self.button_hitt.config(state='active')
        self.button_stayy.config(state='active')


# =========================
# ===== MODE 1v1 =====
# =========================

def creer_paquet():
    return [2,3,4,5,6,7,8,9,10,10,10,10,11]*4

def tirer_carte(paquet):
    c = random.choice(paquet)
    paquet.remove(c)
    return c

def calcul_score(main):
    score = sum(main)
    while score > 21 and 11 in main:
        main[main.index(11)] = 1
        score = sum(main)
    return score


class Blackjack1v1(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.pack(fill="both", expand=True)
        self.app = app

        self.reset()

        self.label_tour = tk.Label(self, font=("Arial", 16, "bold"))
        self.label_tour.pack(pady=10)

        self.label_main = tk.Label(self, font=("Arial", 14))
        self.label_main.pack()

        self.label_info = tk.Label(self, font=("Arial", 14))
        self.label_info.pack(pady=20)

        self.btn_show = tk.Button(self, text="Voir mes cartes", command=self.show)
        self.btn_show.pack()

        self.btn_hit = tk.Button(self, text="Tirer", command=self.hit, state="disabled")
        self.btn_hit.pack()

        self.btn_stand = tk.Button(self, text="Rester", command=self.stand, state="disabled")
        self.btn_stand.pack()

        self.btn_restart = tk.Button(self, text="Nouvelle partie", command=self.nouvelle_partie)
        self.btn_restart.pack(pady=20)
        
        tk.Button(self, text="Retour menu", command=self.app.show_menu).pack()

        self.update()

    def reset(self):
        self.deck = creer_paquet()
        self.players = [
            [tirer_carte(self.deck), tirer_carte(self.deck)],
            [tirer_carte(self.deck), tirer_carte(self.deck)]
        ]
        self.current = 0
        self.phase = "hide"
        self.over = False
        self.stayed = [False, False]

    def update(self):
        if self.phase == "hide":
            self.label_tour.config(text=f"Joueur {self.current+1}")
            self.label_main.config(text="Cartes cachées")
        else:
            hand = self.players[self.current]
            self.label_main.config(text=f"{hand} | Score: {calcul_score(hand)}")

    def show(self):
        self.phase = "play"
        self.btn_hit.config(state="normal")
        self.btn_stand.config(state="normal")
        self.btn_show.config(state="disabled")
        self.update()

    def hit(self):
        hand = self.players[self.current]
        hand.append(tirer_carte(self.deck))

        if calcul_score(hand) > 21:
            self.end()
            return

        self.update()

    def stand(self):
        self.stayed[self.current] = True

        if all(self.stayed):
            self.end()
            return

        self.current = 1 - self.current
        self.phase = "hide"
        self.btn_hit.config(state="disabled")
        self.btn_stand.config(state="disabled")
        self.btn_show.config(state="normal")
        self.update()

    def end(self):
        s1 = calcul_score(self.players[0])
        s2 = calcul_score(self.players[1])

        if s1 > 21:
            res = "Joueur 2 gagne"
            self.btn_hit.config(state='disabled')
            self.btn_stand.config(state='disabled')
        elif s2 > 21:
            res = "Joueur 1 gagne"
            self.btn_hit.config(state='disabled')
            self.btn_stand.config(state='disabled')
        elif s1 > s2:
            res = "Joueur 1 gagne"
            self.btn_hit.config(state='disabled')
            self.btn_stand.config(state='disabled')
        elif s2 > s1:
            res = "Joueur 2 gagne"
            self.btn_hit.config(state='disabled')
            self.btn_stand.config(state='disabled')
        else:
            res = "Egalite"
            self.btn_hit.config(state='disabled')
            self.btn_stand.config(state='disabled')

        self.label_tour.config(text="Fin")
        self.label_main.config(text=f"J1:{self.players[0]}({s1}) | J2:{self.players[1]}({s2})")
        self.label_info.config(text=res)
    
    def nouvelle_partie(self):
        self.reset()
        self.update()
        self.btn_show.config(state="normal")
        self.update





# =========================
# ===== LANCEMENT =====
# =========================

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()