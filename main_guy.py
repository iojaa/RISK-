import matplotlib.pyplot as plt
import game
import combat
import carte2

class RiskGUI:
    def __init__(self):
        print("\n" + "="*40)
        print(" CONFIGURATION DE LA PARTIE DE RISK ")
        print("="*40)
        
        # 1. Saisie sécurisée du nombre de joueurs au lancement
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
        
        # Distribution initiale pour attribuer les territoires de départ
        self.partie.distribuer_cartes()
        
        # On vide la main des joueurs après la distribution (on commence à 0 carte)
        self.partie.cartes = []
        import objets
        self.partie.cartes = objets.créer_cartes()
        import random
        random.shuffle(self.partie.cartes)
        
        for j in self.partie.joueurs:
            j.cartes = []

        # Suivi des règles et bonus
        self.partie.tour_actuel = 1
        self.a_conquis_ce_tour = False  
        self.bonus_echange_actuel = 4   

        # Synchronisation forcée initiale des listes de territoires
        self.synchroniser_territoires_joueurs()

        # 4. Configuration des états du moteur de jeu
        self.joueur_actif_idx = 0
        self.phase = "RENFORCEMENT"
        self.armees_a_placer = 0
        self.territoire_attaquant = None  

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

    def synchroniser_territoires_joueurs(self):
        """Garantit que les listes majuscules et minuscules contiennent exactement la même chose pour tout le monde."""
        for j in self.partie.joueurs:
            # Si une modification a eu lieu dans Territoires, on l'applique à territoires
            j.territoires = j.Territoires

    def verifier_victoire(self):
        """Vérifie si le joueur actif possède la totalité des 42 territoires du jeu."""
        joueur = self.get_joueur_actif()
        
        # Sécurité : on prend le maximum des deux listes pour éviter tout bug de synchronisation
        nb_territoires = max(len(joueur.Territoires), len(joueur.territoires))
        
        if nb_territoires >= 42:
            print("\n" + "#"*50)
            print(f"🎉 🎉 VICTOIRE ÉCLATANTE DE {joueur.nom.upper()} ! 🎉 🎉")
            print(f"Il/Elle a conquis le monde entier en {self.partie.tour_actuel} tours !")
            print("#"*50 + "\n")
            
            self.phase = "VICTOIRE"
            titre_FIN = f"🏆 VICTOIRE DE {joueur.nom.upper()} ! CONQUÊTE TOTALE ! 🏆"
            carte2.mettre_a_jour_carte(self.partie, self.nodes_draw, self.labels_draw, self.titre_obj, titre_FIN)
            self.fig.canvas.draw_idle()
            return True
        return False

    def commencer_phase_renforcement(self):
        if self.phase == "VICTOIRE":
            return
            
        self.phase = "RENFORCEMENT"
        self.territoire_attaquant = None
        joueur = self.get_joueur_actif()
        
        # Recalcul précis basé sur la synchronisation
        self.synchroniser_territoires_joueurs()
        self.armees_a_placer = max(3, len(joueur.Territoires) // 3)
        print(f"\n[TOUR GLOBAL {self.partie.tour_actuel}] C'est au tour de {joueur.nom}.")
        print(f"👉 Armées reçues par territoires : +{self.armees_a_placer}")
        
        # Analyse automatique des cartes pour l'échange
        if len(joueur.cartes) >= 3:
            print(f"🃏 {joueur.nom}, vous possédez {len(joueur.cartes)} cartes : {joueur.cartes}")
            combo_valide = self.verifier_et_echanger_cartes(joueur)
            if combo_valide:
                self.armees_a_placer += self.bonus_echange_actuel
                print(f"🎉 COMBINAISON VALIDE ! Bonus de +{self.bonus_echange_actuel} armées ! (Total à placer : {self.armees_a_placer})")
                self.bonus_echange_actuel += 2
            else:
                print("ℹ️ Vos cartes ne forment pas de combinaison valide. Pas de bonus.")

        print(f"📍 Cliquez sur vos territoires pour placer vos {self.armees_a_placer} armées.")

    def verifier_et_echanger_cartes(self, joueur):
        from collections import Counter
        types = [c.arme for c in joueur.cartes]
        compte = Counter(types)
        cartes_a_retirer = []
        
        for arme, qte in compte.items():
            if qte >= 3:
                cartes_a_retirer = [c for c in joueur.cartes if c.arme == arme][:3]
                break
                
        if not cartes_a_retirer and len(compte) >= 3:
            for arme in compte.keys():
                for c in joueur.cartes:
                    if c.arme == arme and c not in cartes_a_retirer:
                        cartes_a_retirer.append(c)
                        break
                if len(cartes_a_retirer) == 3:
                    break

        if len(cartes_a_retirer) == 3:
            print(f"🔄 Échange des cartes suivantes : {cartes_a_retirer}")
            for c in cartes_a_retirer:
                joueur.cartes.remove(c)
                self.partie.cartes.append(c) 
            return True
        return False

    def gerer_clic(self, event):
        # Bloquer complètement les actions si le jeu est fini
        if self.phase == "VICTOIRE":
            return

        if event.xdata is None or event.ydata is None:
            return

        # Détection du territoire cliqué
        territoire_clique = None
        distance_proximite = 0.5
        for nom, position in carte2.pos.items():
            dist = ((event.xdata - position[0])**2 + (event.ydata - position[1])**2)**0.5
            if dist < distance_proximite:
                territoire_clique = self.partie.territoires_dict[nom]
                break

        if not_territoire := (not territoire_clique):
            return

        joueur = self.get_joueur_actif()

        # CLIC DROIT : Passer d'étape
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
                    if self.partie.tour_actuel == 1:
                        self.phase = "MANŒUVRE"
                        print("[PHASE] Tour 1 : Attaques désactivées ! Passage à la MANŒUVRE.")
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
                        print(f"[ATTAQUE] Attaquant : {territoire_clique.nom}. Cliquez sur un voisin ennemi.")
                    else:
                        print("[ERREUR] Il vous faut au moins 2 armées pour attaquer.")
                else:
                    print("[ERREUR] Vous devez choisir un de vos territoires.")
            else:
                t_att = self.territoire_attaquant
                t_def = territoire_clique

                if t_appartient_au_joueur(t_def, joueur):
                    print("[ERREUR] Impossible d'attaquer votre propre territoire !")
                    self.territoire_attaquant = None
                    self.rafraichir_affichage()
                    return

                if not combat.sont_voisins(t_att.nom, t_def.nom):
                    print(f"[ERREUR] {t_def.nom} n'est pas adjacent à {t_att.nom} !")
                    return

                print(f"\n[COMBAT] {t_att.nom} attaque {t_def.nom} !")
                
                ancien_proprio = t_def.propriétaire

                try:
                    combat.combat(t_att, t_def, verbeux=True)
                except Exception as e:
                    print(f"[ERREUR COMBAT] {e}")

                # RE-SYNCHRONISATION ET TEST DE VICTOIRE IMMÉDIAT
                self.synchroniser_territoires_joueurs()
                
                if t_def.propriétaire == joueur and ancien_proprio != joueur:
                    self.a_conquis_ce_tour = True
                    # Vérification si le joueur a gagné la partie en prenant ce territoire
                    if self.verifier_victoire():
                        return

                self.territoire_attaquant = None
                
                if not joueur_peut_encore_attaquer(joueur):
                    print(f"[INFO] Plus aucune armée disponible pour attaquer. Passage à la MANŒUVRE.")
                    self.phase = "MANŒUVRE"

        elif self.phase == "MANŒUVRE":
            if self.territoire_attaquant is None:
                if t_appartient_au_joueur(territoire_clique, joueur):
                    if territoire_clique.nombre_armées > 1:
                        self.territoire_attaquant = territoire_clique
                        print(f"[MANŒUVRE] Source : {territoire_clique.nom}. Cliquez sur un voisin allié.")
                    else:
                        print("[ERREUR] Il faut au moins 2 armées pour pouvoir en déplacer.")
                else:
                    print("[ERREUR] Ce territoire ne vous appartient pas.")
            else:
                if territoire_clique == self.territoire_attaquant:
                    self.territoire_attaquant = None
                    print("[MANŒUVRE] Sélection annulée.")
                    self.rafraichir_affichage()
                    return

                if t_appartient_au_joueur(territoire_clique, joueur):
                    if combat.sont_voisins(self.territoire_attaquant.nom, territoire_clique.nom):
                        if self.territoire_attaquant.nombre_armées > 1:
                            self.territoire_attaquant.nombre_armées -= 1
                            territoire_clique.nombre_armées += 1
                            print(f"[MANŒUVRE] 1 armée transférée vers {territoire_clique.nom}.")
                        else:
                            print("[ERREUR] Vous devez laisser au moins 1 armée sur le territoire source.")
                            self.territoire_attaquant = None
                    else:
                        print("[ERREUR] Les territoires ne sont pas adjacents.")
                        self.territoire_attaquant = None
                else:
                    print("[ERREUR] La destination doit vous appartenir.")
                    self.territoire_attaquant = None

        self.rafraichir_affichage()

    def passer_au_joueur_suivant(self):
        if self.phase == "VICTOIRE":
            return
            
        joueur_sortant = self.get_joueur_actif()

        if self.a_conquis_ce_tour and len(self.partie.cartes) > 0:
            nouvelle_carte = self.partie.cartes.pop(0)  
            joueur_sortant.cartes.append(nouvelle_carte)
            print(f"\n🎁 {joueur_sortant.nom} a conquis un territoire ! Il pioche : {nouvelle_carte}")
        
        self.a_conquis_ce_tour = False  

        self.joueur_actif_idx = (self.joueur_actif_idx + 1) % len(self.partie.joueurs)
        if self.joueur_actif_idx == 0:
            self.partie.tour_actuel += 1
            
        self.commencer_phase_renforcement()

    def rafraichir_affichage(self):
        joueur = self.get_joueur_actif()
        
        if self.phase == "VICTOIRE":
            return # On ne touche plus à rien si c'est gagné
            
        nb_cartes = len(joueur.cartes)
        info_cartes = f" | 🃏 {nb_cartes} carte(s)"

        if self.phase == "RENFORCEMENT":
            titre = f"Tour de {joueur.nom.upper()} | RENFORCEMENT ({self.armees_a_placer} restantes){info_cartes}"
        elif self.phase == "ATTAQUE":
            titre = f"Tour de {joueur.nom.upper()} | ATTAQUE (Clic droit pour finir){info_cartes}"
            if self.territoire_attaquant:
                titre += f" | Attaque depuis : {self.territoire_attaquant.nom}"
        elif self.phase == "MANŒUVRE":
            titre = f"Tour de {joueur.nom.upper()} | MANŒUVRE (Clic droit pour finir son tour){info_cartes}"
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