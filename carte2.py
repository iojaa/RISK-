import networkx as nx
import matplotlib.pyplot as plt
import game

# On réutilise exactement tes positions d'origine
pos = {
    "Alaska": (0.5, 9), "Northwest Terr.": (2.5, 9.2), "Greenland": (5.8, 9.5),
    "Alberta": (2, 8.2), "Ontario": (3.7, 8), "Quebec": (5, 8.2),
    "Western US": (2.4, 7), "Eastern US": (3.7, 6.7), "Central America": (2.7, 5),
    "Venezuela": (3.5, 4), "Peru": (3.8, 2.5), "Brazil": (5.2, 2.8), "Argentina": (4, 0.5),
    "Iceland": (7.5, 8.5), "Scandinavia": (9.5, 9), "Ukraine": (11.5, 8.2),
    "Great Britain": (7.5, 7.3), "Northern Europe": (9.5, 7.5), "Western Europe": (8, 6), "Southern Europe": (9.8, 6.2),
    "North Africa": (8.8, 4), "Egypt": (10.5, 4), "East Africa": (11.5, 3),
    "Congo": (10, 2), "South Africa": (10.5, 0.8), "Madagascar": (12.5, 0.5),
    "Siberia": (14, 9.5), "Yakutsk": (16, 9.8), "Kamchatka": (17.5, 9.5),
    "Ural": (13.2, 8), "Irkutsk": (15.5, 8.2), "Mongolia": (16, 7), "Japan": (18, 6.8),
    "Afghanistan": (12.5, 6.5), "China": (15, 6), "Middle East": (11.2, 5.2), "India": (14, 4.5), "Siam": (15.5, 4.5),
    "Indonesia": (16, 2), "New Guinea": (18, 2.5), "Western Australia": (17, 0.5), "Eastern Australia": (18.5, 0.5)
}

# Couleurs par défaut des joueurs pour l'interface graphique
COULEURS_JOUEURS = {
    "Alice": "#FF7F7F", # Rouge clair
    "Bob": "#7FBFFF", # Bleu clair
    "Charlie": "#7FFF7F", # Vert clair
    "Neutre": "#FFFFFF" # Blanc si aucun propriétaire
}

def initialiser_carte_interactive(partie):
    """Initialise la fenêtre Matplotlib pour le jeu interactif."""
    G = nx.Graph()
    G.add_nodes_from(pos.keys())

    # Import des frontières depuis combat.py pour l'affichage des lignes
    import combat
    for t_nom, voisins in combat.FRONTIERES.items():
        for v_nom in voisins:
            G.add_edge(t_nom, v_nom)

    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Image de fond optionnelle
    try:
        img = plt.imread('risk_map.webp')
        ax.imshow(img, extent=[-1, 20, -1, 11], aspect='auto', alpha=0.4)
    except FileNotFoundError:
        ax.set_xlim(-1, 20)
        ax.set_ylim(-1, 11)

    # Dessin des lignes de frontières
    nx.draw_networkx_edges(G, pos, ax=ax, width=1.5, edge_color='#666666', alpha=0.6)
    
    # Dessin initial des ronds (noeuds)
    nodes_draw = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1200, node_color='white', edgecolors='black', linewidths=1.5)
    
    # Dessin des chiffres (labels du nombre d'armées au centre)
    labels_draw = nx.draw_networkx_labels(G, pos, ax=ax, labels={n: '0' for n in G.nodes()}, font_size=10, font_weight='bold')

    # Dessin des étiquettes de noms abrégés (placés légèrement plus bas)
    pos_labels = {k: (v[0], v[1]-0.45) for k, v in pos.items()}
    iso_names = {
        "Alaska": "ALK", "Northwest Terr.": "NWT", "Greenland": "GRL", "Alberta": "ALB", "Ontario": "ONT", "Quebec": "QUE", "Western US": "WUS", "Eastern US": "EUS", "Central America": "CAM",
        "Venezuela": "VEN", "Peru": "PER", "Brazil": "BRA", "Argentina": "ARG",
        "Iceland": "ICE", "Scandinavia": "SCA", "Ukraine": "UKR", "Great Britain": "GBR", "Northern Europe": "NEU", "Western Europe": "WEU", "Southern Europe": "SEU",
        "North Africa": "NAF", "Egypt": "EGY", "East Africa": "EAF", "Congo": "CON", "South Africa": "SAF", "Madagascar": "MAD",
        "Siberia": "SIB", "Yakutsk": "YAK", "Kamchatka": "KAM", "Ural": "URA", "Irkutsk": "IRK", "Mongolia": "MON", "Japan": "JAP", "Afghanistan": "AFG", "China": "CHI", "Middle East": "MEA", "India": "IND", "Siam": "SIA",
        "Indonesia": "IDO", "New Guinea": "NGU", "Western Australia": "WAU", "Eastern Australia": "EAU"
    }
    nx.draw_networkx_labels(G, pos_labels, ax=ax, labels=iso_names, font_size=7, font_family='sans-serif')

    legend_text = (
        "CONTRÔLES\n\n"
        "● Clic Gauche :\n Sélection / Action\n"
        "● Clic Droit :\n Annuler / Fin Tour\n\n"
        "COULEURS\n"
        "🔴 Joueur 1\n🔵 Joueur 2\n🟢 Joueur 3"
    )
    legende_obj = plt.text(1.02, 0.5, legend_text, transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    legende_obj._risk_legend = True  # Marqueur pour pouvoir retrouver cet objet dans mettre_a_jour_carte
    
    ax.axis('off')
    titre_obj = fig.suptitle("RISK", fontsize=14, fontweight='bold', y=0.95)
    
    return fig, ax, nodes_draw, labels_draw, titre_obj

def __init__(self):
        # --- NOUVEAU : Saisie dynamique des joueurs ---
        # 1. Demander le nombre de joueurs (entre 2 et 6 par exemple)
        nb_joueurs_choisi = plt.numinput(
            title="Configuration de la partie",
            prompt="Entrez le nombre de joueurs (2 à 6) :",
            default=3,
            minval=2,
            maxval=6
        )
        
        # Sécurité si l'utilisateur clique sur "Annuler"
        if nb_joueurs_choisi is None:
            print("[INFO] Lancement annulé. Utilisation de la configuration par défaut.")
            noms_joueurs = ["Alice", "Bob", "Charlie"]
        else:
            nb_joueurs_choisi = int(nb_joueurs_choisi)
            noms_joueurs = []
            
            # 2. Demander le nom de chaque joueur
            for i in range(nb_joueurs_choisi):
                nom = plt.textinput(
                    title=f"Joueur {i+1}",
                    prompt=f"Entrez le nom du joueur {i+1} :"
                )
                # Si le joueur fait "Annuler" ou laisse vide, on donne un nom par défaut
                if not nom or nom.strip() == "":
                    nom = f"Joueur_{i+1}"
                noms_joueurs.append(nom.strip())

        # 1. Initialisation de la logique de jeu avec les vrais noms saisis
        self.partie = game.Partie(noms_joueurs)
        self.partie.territoires_dict = {t.nom: t for t in self.partie.territoires}
def mettre_a_jour_carte(partie, nodes_draw, labels_draw, titre_obj, text_titre):
    """Met à jour graphiquement les couleurs des joueurs et les textes des armées."""
    # IMPORTANT : on itère dans l'ordre de `pos`, qui est l'ordre utilisé par NetworkX
    # pour dessiner les nœuds. Utiliser un ordre différent décalerait les couleurs.
    couleurs_noeuds = []
    
    # Palette de couleurs génériques pour gérer jusqu'à 6 joueurs
    palette = ["#FF7F7F", "#7FBFFF", "#7FFF7F", "#FFD700", "#FF8C00", "#DA70D6"]

    # Création d'un dictionnaire { "Nom_du_joueur": "Couleur" } dynamiquement
    couleurs_attribuees = {}
    for idx, joueur in enumerate(partie.joueurs):
        couleurs_attribuees[joueur.nom] = palette[idx % len(palette)]

    # On parcourt les territoires dans l'ordre de `pos` (ordre de dessin NetworkX)
    for nom_t in pos.keys():
        territoire = partie.territoires_dict.get(nom_t)
        if territoire is None:
            couleurs_noeuds.append("#FFFFFF")
            continue

        proprio_nom = territoire.propriétaire.nom if hasattr(territoire.propriétaire, 'nom') else territoire.propriétaire
        
        # Attribution de la couleur dynamique
        if proprio_nom in couleurs_attribuees:
            couleurs_noeuds.append(couleurs_attribuees[proprio_nom])
        else:
            couleurs_noeuds.append("#FFFFFF")  # Neutre / Blanc

        # Mise à jour du texte au centre du cercle
        if nom_t in labels_draw:
            labels_draw[nom_t].set_text(str(territoire.nombre_armées))

    # Application globale des couleurs (dans l'ordre de pos)
    nodes_draw.set_facecolors(couleurs_noeuds)
    titre_obj.set_text(text_titre)

    # Mise à jour de la légende avec les vrais noms et couleurs des joueurs
    # (on stocke la référence à l'objet texte légende dans nodes_draw.axes)
    ax = nodes_draw.axes
    for child in ax.get_children():
        if hasattr(child, '_risk_legend') and child._risk_legend:
            couleurs_emoji = ["R", "B", "Ve", "J", "O", "Vi"]
            lignes_joueurs = "\n".join(
                f"{couleurs_emoji[i % len(couleurs_emoji)]} {j.nom}"
                for i, j in enumerate(partie.joueurs)
            )
            child.set_text(
                "CONTRÔLES\n\n"
                "● Clic Gauche :\n Sélection / Action\n"
                "● Clic Droit :\n Annuler / Fin Tour\n\n"
                "COULEURS\n" + lignes_joueurs
            )
            break
def dessiner_carte_risk_complete():
    """Conserve ta fonction d'origine intacte si tu lances carte.py directement."""
    print("Affichage de la carte de démonstration...")