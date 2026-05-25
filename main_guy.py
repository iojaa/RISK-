import matplotlib.pyplot as plt
import game
import combat
import carte2

class RiskGUI:
    def __init__(self):
        print("\n" + "="*40)
        print(" CONFIGURATION DE LA PARTIE DE RISK ")
        print("="*40)
        
        # 1. Saisie sécurisée du nombre de joueurs au lancement (avant plt.show)
        while True:
            try:
                nb_joueurs = int(input("Entrez le nombre de joueurs (2 à 6) : "))
                if 2 <= nb_joueurs <= 6:
                    break
                print("[ERREUR] Le nombre de joueurs doit être entre 2 et 6.")
            except ValueError:
                print("[ERREUR] Veuillez entrer un nombre entier valide.")

        # 2. Saisie des noms de chaque joueur
        noms_joueurs = []
        for i in range(nb_joueurs):
            nom = input(f"Entrez le nom du joueur {i+1} : ").strip()
            if not nom:
                nom = f"Joueur_{i+1}"
            noms_joueurs.append(nom)

        print("\n[INFO] Configuration terminée ! Lancement de la carte...")
        print("="*40 + "\n")

        # 3. Initialisation de la logique de jeu avec les vrais noms saisis
        self.partie = game.Partie(noms_joueurs)
        self.partie.territoires_dict = {t.nom: t for t in self.partie.territoires}
        
        # Distribution automatique initiale
        self.partie.distribuer_cartes()
        
        # Ajout du compteur de tour global
        self.partie.tour_actuel = 1

        # Synchronisation forcée des listes de territoires
        for j in self.partie.joueurs:
            j.territoires = j.Territoires

        # 4. Configuration des états du moteur de jeu
        self.joueur_actif_idx = 0
        self.phase = "RENFORCEMENT"
        self.armees_a_placer = 0
        self.territoire_attaquant = None # Sert aussi de territoire source en MANŒUVRE

        # 5. Initialisation de la fenêtre graphique
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
        self.armees_a_placer = max(3, len(joueur.Territoires) // 3)
        print(f"\n[TOUR GLOBAL {self.partie.tour_actuel}] C'est au tour de {joueur.nom}. {self.armees_a_placer} armées à placer.")

    def gerer_clic(self, event):
        if event.xdata is None or event.ydata is None:
            return

        # Détection du territoire le plus proche du clic
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

        # CLIC DROIT : Annuler l'action en cours ou passer à la phase suivante
        if event.button == 3:
            if self.territoire_attaquant:
                self.territoire_attaquant = None
                print("[INFO] Sélection annulée.")
            elif self.phase == "ATTAQUE":
                print(f"[INFO] {joueur.nom} termine ses attaques. Passage à la MANŒUVRE.")
                self.phase = "MANŒUVRE"
            elif self.phase == "MANŒUVRE":
                print(f"[INFO] {joueur.nom} termine sa manœuvre. Fin du tour.")
                self.passer_au_joueur_suivant()
            self.rafraichir_affichage()
            return

        # CLIC GAUCHE : Actions du jeu
        if self.phase == "RENFORCEMENT":
            if t_appartient_au_joueur(territoire_clique, joueur):
                territoire_clique.nombre_armées += 1
                self.armees_a_placer -= 1
                print(f"[RENFORT] +1 armée sur {territoire_clique.nom} (Reste : {self.armees_a_placer})")
                
                if self.armees_a_placer == 0:
                    # RÈGLE : Pas d'attaque au Tour 1
                    if self.partie.tour_actuel == 1:
                        self.phase = "MANŒUVRE"
                        print("[PHASE] Tour 1 : Attaques interdites ! Passage direct à la phase de MANŒUVRE (Clic droit pour finir).")
                    else:
                        self.phase = "ATTAQUE"
                        print("[PHASE] Renforcements terminés. Place à la phase d'ATTAQUE !")
            else:
                print("[ERREUR] Ce territoire ne vous appartient pas !")

        elif self.phase == "ATTAQUE":
            if self.territoire_attaquant is None:
                if t_appartient_au_joueur(territoire_clique, joueur):
                    if territorio_peut_attaquer(territoire_clique):
                        self.territoire_attaquant = territoire_clique
                        print(f"[ATTAQUE] Attaquant choisi : {territoire_clique.nom}. Cliquez sur une cible ennemie voisine.")
                    else:
                        print("[ERREUR] Il vous faut au moins 2 armées pour attaquer.")
                else:
                    print("[ERREUR] Vous devez choisir un de vos territoires.")
            else:
                t_att = self.territoire_attaquant
                t_def = territoire_clique

                if t_appartient_au_joueur(t_def, joueur):
                    print("[ERREUR] Vous ne pouvez pas attaquer votre propre territoire !")
                    self.territoire_attaquant = None
                    self.rafraichir_affichage()
                    return

                if not combat.sont_voisins(t_att.nom, t_def.nom):
                    print(f"[ERREUR] {t_def.nom} n'est pas un voisin de {t_att.nom} !")
                    return

                print(f"\n[COMBAT] {t_att.nom} attaque {t_def.nom} !")
                
                try:
                    combat.combat(t_att, t_def, verbeux=True)
                except Exception as e:
                    print(f"[ERREUR COMBAT] {e}")

                self.territoire_attaquant = None
                
                if not joueur_peut_encore_attaquer(joueur):
                    print(f"[INFO] {joueur.nom} n'a plus de territoires capables d'attaquer. Passage à la MANŒUVRE.")
                    self.phase = "MANŒUVRE"

        elif self.phase == "MANŒUVRE":
            # ÉTAPE 1 : Sélection du territoire de départ
            if self.territoire_attaquant is None:
                if t_appartient_au_joueur(territoire_clique, joueur):
                    if territoire_clique.nombre_armées > 1:
                        self.territoire_attaquant = territoire_clique
                        print(f"[MANŒUVRE] Source : {territoire_clique.nom}. Cliquez sur un voisin allié (Clic gauche = +1 armée déplacée, Clic droit = Valider/Fin du tour).")
                    else:
                        print("[ERREUR] Le territoire doit avoir au moins 2 armées pour en déplacer.")
                else:
                    print("[ERREUR] Ce territoire ne vous appartient pas.")
            
            # ÉTAPE 2 : Déplacement unitaire au clic gauche
            else:
                if territoire_clique == self.territoire_attaquant:
                    self.territoire_attaquant = None
                    print("[MANŒUVRE] Sélection source annulée.")
                    self.rafraichir_affichage()
                    return

                if t_appartient_au_joueur(territoire_clique, joueur):
                    if combat.sont_voisins(self.territoire_attaquant.nom, territoire_clique.nom):
                        if self.territoire_attaquant.nombre_armées > 1:
                            # Déplacement d'une armée
                            self.territoire_attaquant.nombre_armées -= 1
                            territoire_clique.nombre_armées += 1
                            print(f"[MANŒUVRE] 1 armée déplacée de {self.territoire_attaquant.nom} vers {territoire_clique.nom}.")
                            print(f" (Reste déplaçable sur la source : {self.territoire_attaquant.nombre_armées - 1})")
                        else:
                            print("[ERREUR] Plus d'armées déplaçables. Vous devez laisser au moins 1 armée sur la source.")
                            self.territoire_attaquant = None
                    else:
                        print("[ERREUR] Les territoires ne sont pas voisins.")
                        self.territoire_attaquant = None
                else:
                    print("[ERREUR] La destination doit vous appartenir.")
                    self.territoire_attaquant = None

        self.rafraichir_affichage()

    def passer_au_joueur_suivant(self):
        self.joueur_actif_idx = (self.joueur_actif_idx + 1) % len(self.partie.joueurs)
        if self.joueur_actif_idx == 0:
            self.partie.tour_actuel += 1
        self.commencer_phase_renforcement()

    def rafraichir_affichage(self):
        joueur = self.get_joueur_actif()
        
        if self.phase == "RENFORCEMENT":
            titre = f"Tour de {joueur.nom.upper()} | Phase : RENFORCEMENT ({self.armees_a_placer} restantes)"
        elif self.phase == "ATTAQUE":
            titre = f"Tour de {joueur.nom.upper()} | Phase : ATTAQUE (Clic droit pour finir)"
            if self.territoire_attaquant:
                titre += f" | Attaque depuis : {self.territoire_attaquant.nom}"
        elif self.phase == "MANŒUVRE":
            titre = f"Tour de {joueur.nom.upper()} | Phase : MANŒUVRE (Clic droit pour finir son tour)"
            if self.territoire_attaquant:
                titre += f" | Déplacement depuis : {self.territoire_attaquant.nom}"

        carte2.mettre_a_jour_carte(self.partie, self.nodes_draw, self.labels_draw, self.titre_obj, titre)
        self.mettre_en_surbrillance_selection()
        self.fig.canvas.draw_idle()

    def mettre_en_surbrillance_selection(self):
        self.nodes_draw.set_edgecolors(['black'] * len(self.partie.territoires))
        self.nodes_draw.set_linewidths([1.5] * len(self.partie.territoires))
        
        if self.territoire_attaquant:
            G_nodes = list(self.partie.territoires_dict.keys())
            if self.territoire_attaquant.nom in G_nodes:
                idx = G_nodes.index(self.territoire_attaquant.nom)
                edge_colors = list(self.nodes_draw.get_edgecolors())
                line_widths = list(self.nodes_draw.get_linewidths())
                edge_colors[idx] = 'red'
                line_widths[idx] = 4.0
                self.nodes_draw.set_edgecolors(edge_colors)
                self.nodes_draw.set_linewidths(line_widths)

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
