import objets
import carte
import combat




territoires = ["Alaska", "Northwest Terr.", "Greenland", "Alberta", "Ontario", "Quebec", "Western US", "Eastern US", "Central America",
                    "Venezuela", "Peru", "Brazil", "Argentina",
                    "Iceland", "Scandinavia", "Ukraine", "Great Britain", "Northern Europe", "Western Europe", "Southern Europe",
                    "North Africa", "Egypt", "East Africa", "Congo", "South Africa", "Madagascar",
                    "Siberia", "Yakutsk", "Kamchatka", "Ural", "Irkutsk", "Mongolia", "Japan",
                    "Afghanistan", "China", "Middle East", "India", "Siam","Eastern Australia", "Western Australia", "New Guinea", "Indonesia"]

class Partie:
    def __init__(self, joueurs):
        self.joueurs = [objets.Joueur(nom) for nom in joueurs]
        self.nb_joueurs = len(self.joueurs)
        self.territoires = [objets.Territoire(nom) for nom in territoires]
        self.cartes = objets.créer_cartes()  # Crée les cartes au début de la partie



    def distribuer_cartes(self):
        import random
        dict_territoires = {territoire.nom: territoire for territoire in self.territoires}  # Crée un dictionnaire pour accéder rapidement aux territoires par nom
        random.shuffle(self.cartes)  # Mélange les cartes
        for i, carte in enumerate(self.cartes):
            joueur = self.joueurs[i % len(self.joueurs)]  # Distribue les cartes de manière cyclique
            joueur.cartes.append(carte)
            if carte.territoires in dict_territoires:  # Vérifie si le territoire de la carte existe
                territoire = dict_territoires[carte.territoires]
                joueur.Territoires.append(territoire)  # Associe les territoires des cartes aux joueurs
                territoire.propriétaire = joueur  # Associe les territoires des cartes aux joueurs
                territoire.nombre_armées += 1  # Place une armée sur le territoire au début de la partie


    def distribuer_armées(self):
        for joueur in self.joueurs:
            # 1. Calcul du nombre d'armées à distribuer
            nombre_armées = max(3, len(joueur.Territoires) // 3)
            print(f"\n=== Tour de {joueur.nom} : Phase de renforcement ===")
            print(f"{joueur.nom} reçoit {nombre_armées} armées à distribuer.")
            
            # 2. Boucle de distribution des armées reçues
            while nombre_armées > 0:
                print(f"\nIl vous reste {nombre_armées} armées à placer.")
                print("Vos territoires disponibles :")
                
                # Affiche la liste des territoires du joueur pour l'aider à choisir
                for i, terr in enumerate(joueur.Territoires):
                    print(f" {i} - {terr.nom} (Armées actuelles : {terr.nombre_armées})")
                
                # 3. Saisie sécurisée du choix du territoire
                try:
                    choix = int(input(f"{joueur.nom}, entrez le NUMÉRO du territoire à renforcer : "))
                    
                    if 0 <= choix < len(joueur.Territoires):
                        territoire_choisi = joueur.Territoires[choix]
                        
                        # Saisie du nombre d'armées à déposer sur ce territoire
                        qte = int(input(f"Combien d'armées voulez-vous placer sur {territoire_choisi.nom} ? (Max {nombre_armées}) : "))
                        
                        if 1 <= qte <= nombre_armées:
                            # On applique le renforcement
                            territoire_choisi.nombre_armées += qte
                            nombre_armées -= qte
                            print(f"Succès ! {qte} armée(s) ajoutée(s) sur {territoire_choisi.nom}.")
                        else:
                            print(f"Erreur : Vous devez choisir une quantité entre 1 et {nombre_armées}.")
                    else:
                        print("Erreur : Ce numéro ne fait pas partie de vos territoires.")
                        
                except ValueError:
                    print("Erreur : Veuillez entrer un nombre entier valide.")

            

# P=Partie(["Alice", "Bob", "Charlie"])
# P.distribuer_cartes()
# print(P.joueurs[2].Territoires)  # Affiche les territoires de chaque joueur
# print(P.joueurs[0].cartes)  # Affiche les cartes de chaque joueur
# print(P.joueurs)  # Affiche les noms des joueurs
# P.distribuer_armées()
# print(P.joueurs[2].Territoires) 