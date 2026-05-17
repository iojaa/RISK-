import objets
import carte





territoires = ["Alaska", "Northwest Terr.", "Greenland", "Alberta", "Ontario", "Quebec", "Western US", "Eastern US", "Central America",
                    "Venezuela", "Peru", "Brazil", "Argentina",
                    "Iceland", "Scandinavia", "Ukraine", "Great Britain", "Northern Europe", "Western Europe", "Southern Europe",
                    "North Africa", "Egypt", "East Africa", "Congo", "South Africa", "Madagascar",
                    "Siberia", "Yakutsk", "Kamchatka", "Ural", "Irkutsk", "Mongolia", "Japan",
                    "Afghanistan", "China", "Middle East", "India", "Siam","Eastern Australia", "Western Australia", "New Guinea", "Indonesia"]

class Partie:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.territoire=objets.Territoire(territoires)
        self.cartes = objets.créer_cartes()  # Crée les cartes au début de la partie



    def distribuer_cartes(self):
        import random
        random.shuffle(self.cartes)  # Mélange les cartes
        for i, carte in enumerate(self.cartes):
            joueur = self.joueurs[i % len(self.joueurs)]  # Distribue les cartes de manière cyclique
            joueur.cartes.append(carte)
            joueur.territoires.append(carte.territoires)  # Associe les territoires des cartes aux joueurs

Alice=objets.Joueur("Alice")
Bob=objets.Joueur("Bob")    
Charlie=objets.Joueur("Charlie")
P=Partie([Alice, Bob, Charlie])
P.distribuer_cartes()
print(P.joueurs[0].territoires)  # Affiche les territoires de chaque joueur
print(P.joueurs[0].cartes)  # Affiche les cartes de chaque joueur
