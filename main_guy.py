import matplotlib.pyplot as plt
import game
import combat
import carte2

class RiskGUI:
    def __init__(self):
        print("\n" + "="*40)
        print(" CONFIGURATION DE LA PARTIE DE RISK ")
        print("="*40)
        
        # Saisie sécurisée du nombre de joueurs dans la console
        while True:
            try:
                nb_joueurs = int(input("Entrez le nombre de joueurs (2 à 6) : "))
                if 2 <= nb_joueurs <= 6:
                    break
                print("[ERREUR] Le nombre de joueurs doit être entre 2 et 6.")
            except ValueError:
                print("[ERREUR] Veuillez entrer un nombre entier valide.")

        # Saisie des noms de chaque joueur
        noms_joueurs = []
        for i in range(nb_joueurs):
            nom = input(f"Entrez le nom du joueur {i+1} : ").strip()
            # Si le nom est vide, on donne un nom automatique
            if not nom:
                nom = f"Joueur_{i+1}"
            noms_joueurs.append(nom)

        print("\n[INFO] Configuration terminée ! Lancement de la carte...")
        print("="*40 + "\n")

        # 1. Initialisation de la logique de jeu (game.py) avec les vrais noms saisis
        self.partie = game.Partie(noms_joueurs)
        self.partie.territoires_dict = {t.nom: t for t in self.partie.territoires}
        
        # Distribution automatique initiale
        self.partie.distribuer_cartes()
        
        # Synchronisation forcée des attributs majuscules/minuscules de tes objets
        for j in self.partie.joueurs:
            j.territoires = j.Territoires

        # 2. Configuration des états du moteur de jeu
        self.joueur_actif_idx = 0
        self.phase = "RENFORCEMENT"
        self.armees_a_placer = 0
        self.territoire_attaquant = None

        # 3. Initialisation de la fenêtre graphique
        self.fig, self.ax, self.nodes_draw, self.labels_draw, self.titre_obj = carte2.initialiser_carte_interactive(self.partie)
        
        # Liaison de l'événement clic de souris
        self.fig.canvas.mpl_connect('button_press_event', self.gerer_clic)

        # Lancement du premier tour
        self.commencer_phase_renforcement()
        self.rafraichir_affichage()
        plt.show()



    def get_joueur_actif(self):
        return self.partie.joueurs[self.joueur_actif_idx]

    def commencer_phase_renforcement(self):
        self.phase = "RENFORCEMENT"
        self.territoire_attaquant = None
        joueur = self.get_joueur_actif()
        # Calcul officiel : nombre de territoires divisé par 3 (minimum 3 armées)
        self.armees_a_placer = max(3, len(joueur.Territoires) // 3)
        print(f"\n[TOUR] C'est au tour de {joueur.nom}. {self.armees_a_placer} armées à placer.")

    def gerer_clic(self, event):
        if event.xdata is None or event.ydata is None:
            return

        # Détection du territoire le plus proche du clic de souris
        territoire_clique = None
        distance_proximite = 0.5
        for nom, position in carte2.pos.items():
            dist = ((event.xdata - position[0])**2 + (event.ydata - position[1])**2)**0.5
            if dist < distance_proximite:
                territoire_clique = self.partie.territoires_dict[nom]
                break

        if not territoire_clique:
            return

        joueur = self.get_joueur_actif()

        # CLIC DROIT : Annuler la sélection en cours ou finir son tour d'attaque
        if event.button == 3:
            if self.territoire_attaquant:
                self.territoire_attaquant = None
                print("[INFO] Sélection attaquante annulée.")
            elif self.phase == "ATTAQUE":
                print(f"[INFO] {joueur.nom} décide de terminer sa phase d'attaque.")
                self.passer_au_joueur_suivant()
            self.rafraichir_affichage()
            return

        # CLIC GAUCHE : Déroulement des actions du jeu
        if self.phase == "RENFORCEMENT":
            # Vérification de propriété
            if t_appartient_au_joueur(territoire_clique, joueur):
                territoire_clique.nombre_armées += 1
                self.armees_a_placer -= 1
                print(f"[RENFORT] +1 armée sur {territoire_clique.nom} (Reste : {self.armees_a_placer})")
                
                if self.armees_a_placer == 0:
                    self.phase = "ATTAQUE"
                    print("[PHASE] Renforcements terminés. Place à la phase d'ATTAQUE !")
            else:
                print("[ERREUR] Ce territoire ne vous appartient pas !")

        elif self.phase == "ATTAQUE":
            if self.territoire_attaquant is None:
                # Étape 1 : Sélection du territoire d'où part l'attaque
                if t_appartient_au_joueur(territoire_clique, joueur):
                    if territorio_peut_attaquer(territoire_clique):
                        self.territoire_attaquant = territoire_clique
                        print(f"[ATTAQUE] Territoire attaquant choisi : {territoire_clique.nom}. Cliquez sur une cible ennemie voisine.")
                    else:
                        print("[ERREUR] Il vous faut au moins 2 armées pour pouvoir lancer une attaque.")
                else:
                    print("[ERREUR] Vous devez choisir un de vos territoires.")
            else:
                # Étape 2 : Sélection de la cible ennemie
                t_att = self.territoire_attaquant
                t_def = territoire_clique

                if t_appartient_au_joueur(t_def, joueur):
                    print("[ERREUR] Vous ne pouvez pas attaquer votre propre territoire ! Sélection réinitialisée.")
                    self.territoire_attaquant = None
                    self.rafraichir_affichage()
                    return

                if not combat.sont_voisins(t_att.nom, t_def.nom):
                    print(f"[ERREUR] {t_def.nom} n'est pas un voisin direct de {t_att.nom} !")
                    return

                # Résolution du combat (Appel à ton module combat.py)
                print(f"\n[COMBAT] {t_att.nom} attaque {t_def.nom} !")
                
                # Double sécurité pour la casse majuscule/minuscule de tes objets
                for j in self.partie.joueurs:
                    j.territoires = j.Territoires

                # Résolution automatique
                try:
                    
                    bilan = combat.combat(t_att, t_def, verbeux=True)
                    
                    # Répercuter les changements de listes après combat
                    for j in self.partie.joueurs:
                        j.Territoires = j.territoires
                except Exception as e:
                    print(f"[ERREUR COMBAT] {e}")

                self.territoire_attaquant = None
                
                # Vérifier si le joueur possède encore des territoires capables de se battre
                if not joueur_peut_encore_attaquer(joueur):
                    print(f"[INFO] {joueur.nom} n'a plus de territoires capables d'attaquer.")
                    self.passer_au_joueur_suivant()

        self.rafraichir_affichage()

    def passer_au_joueur_suivant(self):
        self.joueur_actif_idx = (self.joueur_actif_idx + 1) % len(self.partie.joueurs)
        self.commencer_phase_renforcement()

    def rafraichir_affichage(self):
        joueur = self.get_joueur_actif()
        
        # Création du titre dynamique en haut de la carte2
        if self.phase == "RENFORCEMENT":
            titre = f"Tour de {joueur.nom.upper()} | Phase : RENFORCEMENT ({self.armees_a_placer} restantes)"
        else:
            titre = f"Tour de {joueur.nom.upper()} | Phase : ATTAQUE (Clic droit pour finir le tour)"
            if self.territoire_attaquant:
                titre += f" | Attaque depuis : {self.territoire_attaquant.nom}"

        # Application graphique (carte2.py)
        carte2.mettre_a_jour_carte(self.partie, self.nodes_draw, self.labels_draw, self.titre_obj, titre)
        
        # Gestion des contours (Mise en surbrillance rouge du territoire sélectionné)
        self.mettre_en_surbrillance_selection()
        
        self.fig.canvas.draw_idle()

    def mettre_en_surbrillance_selection(self):
        # Réinitialisation de toutes les bordures en noir fin
        self.nodes_draw.set_edgecolors(['black'] * len(self.partie.territoires))
        self.nodes_draw.set_linewidths([1.5] * len(self.partie.territoires))
        
        if self.territoire_attaquant:
            G_nodes = list(self.partie.territoires_dict.keys())
            if self.territoire_attaquant.nom in G_nodes:
                idx = G_nodes.index(self.territoire_attaquant.nom)
                edge_colors = list(self.nodes_draw.get_edgecolors())
                line_widths = list(self.nodes_draw.get_linewidths())
                edge_colors[idx] = 'red' # Bordure rouge pour l'attaquant sélectionné
                line_widths[idx] = 4.0
                self.nodes_draw.set_edgecolors(edge_colors)
                self.nodes_draw.set_linewidths(line_widths)

# --- FONCTIONS REQUISES POUR HARMONISER TES OBJETS ---



def t_appartient_au_joueur(territoire, joueur):
    if t_has_no_owner(territoire): return False
    nom_proprio = territoire.propriétaire.nom if hasattr(territoire.propriétaire, 'nom') else territoire.propriétaire
    return nom_proprio == joueur.nom

def t_has_no_owner(t):
    return t.propriétaire is None

def territorio_peut_attaquer(t):
    return t.nombre_armées >= 2

def joueur_peut_encore_attaquer(joueur):
    return any(t.nombre_armées >= 2 for t in joueur.Territoires)

if __name__ == "__main__":
    print("=== LANCEMENT DU RISK INTERACTIVE INTERFACE ===")
    RiskGUI()