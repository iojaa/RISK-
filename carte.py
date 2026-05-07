#import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt



def dessiner_carte_risk_complete():
    G = nx.Graph()

    # 1. POSITION DES TERRITOIRES (Coordonnées X, Y simplifiées)
    # Format: "Nom": (Longitude_imaginaire, Latitude_imaginaire)
    pos = {
        # Amérique du Nord (Jaune)
        "Alaska": (0.5, 9), "Northwest Terr.": (2.5, 9.2), "Greenland": (5.8, 9.5),
        "Alberta": (2, 8.2), "Ontario": (3.7, 8), "Quebec": (5, 8.2),
        "Western US": (2.4, 7), "Eastern US": (3.7, 6.7), "Central America": (2.7, 5),
        
        # Amérique du Sud (Rouge)
        "Venezuela": (3.5, 4), "Peru": (3.8, 2.5), "Brazil": (5.2, 2.8), "Argentina": (4, 0.5),
        
        # Europe (Bleu)
        "Iceland": (7.5, 8.5), "Scandinavia": (9.5, 9), "Ukraine": (11.5, 8.2),
        "Great Britain": (7.5, 7.3), "Northern Europe": (9.5, 7.5), "Western Europe": (8, 6), "Southern Europe": (9.8, 6.2),
        
        # Afrique (Brun/Orange) - On l'espace un peu
        "North Africa": (8.8, 4), "Egypt": (10.5, 4), "East Africa": (11.5, 3),
        "Congo": (10, 2), "South Africa": (10.5, 0.8), "Madagascar": (12.5, 0.5),
        
        # Asie (Vert) - On l'étale vers l'Est
        "Siberia": (14, 9.5), "Yakutsk": (16, 9.8), "Kamchatka": (17.5, 9.5),
        "Ural": (13.2, 8), "Irkutsk": (15.5, 8.2), "Mongolia": (16, 7), "Japan": (18, 6.8),
        "Afghanistan": (12.5, 6.5), "China": (15, 6), "Middle East": (11.2, 5.2), "India": (14, 4.5), "Siam": (15.5, 4.5),
        
        # Océanie (Violet)
        "Indonesia": (16, 2), "New Guinea": (18, 2.5), "Western Australia": (17, 0.5), "Eastern Australia": (18.5, 0.5)
    }

    # 2. DÉFINITION DES COULEURS PAR CONTINENT
    colors = []
    for node in pos:
        if node in ["Alaska", "Northwest Terr.", "Greenland", "Alberta", "Ontario", "Quebec", "Western US", "Eastern US", "Central America"]:
            colors.append("#F3D34A") # Jaune
        elif node in ["Venezuela", "Peru", "Brazil", "Argentina"]:
            colors.append("#D83A2D") # Rouge
        elif node in ["Iceland", "Scandinavia", "Ukraine", "Great Britain", "Northern Europe", "Western Europe", "Southern Europe"]:
            colors.append("#4A88F3") # Bleu
        elif node in ["North Africa", "Egypt", "East Africa", "Congo", "South Africa", "Madagascar"]:
            colors.append("#E3963E") # Orange
        elif node in ["Siberia", "Yakutsk", "Kamchatka", "Ural", "Irkutsk", "Mongolia", "Japan", "Afghanistan", "China", "Middle East", "India", "Siam"]:
            colors.append("#5AB25A") # Vert
        else:
            colors.append("#B35AF3") # Violet

    # 3. CONNEXIONS (Frontières RISK)
    frontieres = [
        # Amérique du Nord
        ("Alaska", "Northwest Terr."), ("Alaska", "Alberta"), ("Alaska", "Kamchatka"),
        ("Northwest Terr.", "Alberta"), ("Northwest Terr.", "Ontario"), ("Northwest Terr.", "Greenland"),
        ("Greenland", "Ontario"), ("Greenland", "Quebec"), ("Greenland", "Iceland"),
        ("Alberta", "Ontario"), ("Alberta", "Western US"),
        ("Ontario", "Quebec"), ("Ontario", "Western US"), ("Ontario", "Eastern US"),
        ("Quebec", "Eastern US"), ("Western US", "Eastern US"), ("Western US", "Central America"),
        ("Eastern US", "Central America"),
        # Amérique du Sud
        ("Central America", "Venezuela"), ("Venezuela", "Brazil"), ("Venezuela", "Peru"),
        ("Brazil", "Peru"), ("Brazil", "Argentina"), ("Brazil", "North Africa"), ("Peru", "Argentina"),
        # Europe
        ("Iceland", "Great Britain"), ("Iceland", "Scandinavia"),
        ("Great Britain", "Western Europe"), ("Great Britain", "Northern Europe"), ("Great Britain", "Scandinavia"),
        ("Scandinavia", "Northern Europe"), ("Scandinavia", "Ukraine"),
        ("Western Europe", "Northern Europe"), ("Western Europe", "Southern Europe"), ("Western Europe", "North Africa"),
        ("Northern Europe", "Southern Europe"), ("Northern Europe", "Ukraine"),
        ("Southern Europe", "Ukraine"), ("Southern Europe", "North Africa"), ("Southern Europe", "Egypt"), ("Southern Europe", "Middle East"),
        # Afrique
        ("North Africa", "Egypt"), ("North Africa", "East Africa"), ("North Africa", "Congo"),
        ("Egypt", "East Africa"), ("Egypt", "Middle East"),
        ("East Africa", "Congo"), ("East Africa", "South Africa"), ("East Africa", "Madagascar"),
        ("Congo", "South Africa"), ("South Africa", "Madagascar"),
        # Asie
        ("Ukraine", "Ural"), ("Ukraine", "Afghanistan"), ("Ukraine", "Middle East"),
        ("Ural", "Siberia"), ("Ural", "Afghanistan"),
        ("Siberia", "Yakutsk"), ("Siberia", "Irkutsk"), ("Siberia", "Mongolia"),
        ("Yakutsk", "Kamchatka"), ("Yakutsk", "Irkutsk"),
        ("Kamchatka", "Irkutsk"), ("Kamchatka", "Mongolia"), ("Kamchatka", "Japan"),
        ("Irkutsk", "Mongolia"), ("Mongolia", "Japan"), ("Mongolia", "China"),
        ("Afghanistan", "China"), ("Afghanistan", "Middle East"), ("Afghanistan", "India"),
        ("China", "India"), ("China", "Siam"), ("Middle East", "India"),
        ("India", "Siam"), ("Siam", "Indonesia"),
        # Océanie
        ("Indonesia", "New Guinea"), ("Indonesia", "Western Australia"),
        ("New Guinea", "Western Australia"), ("New Guinea", "Eastern Australia"),
        ("Western Australia", "Eastern Australia")
    ]
    
    G.add_edges_from(frontieres)
    
    # --- AJOUT DE L'IMAGE DE FOND ---
    # Option A : Charger une image locale (ex: 'risk_map.jpg')
    img = plt.imread('risk_map.webp')
    
   
    # Afficher l'image. 
    # 'extent' définit les limites [X_min, X_max, Y_min, Y_max] 
    # Il faut que ces chiffres correspondent à tes coordonnées 'pos'
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.imshow(img, extent=[-1, 20, -1, 11], aspect='auto', alpha=0.6)
    # --------------------------------

    # Arêtes
    nx.draw_networkx_edges(G, pos, width=2, edge_color='#666666', alpha=0.8)
    
    # Nœuds
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=colors, edgecolors='black', linewidths=1.5)
    
    # Noms
    iso_names = {
        "Alaska": "ALK", "Northwest Terr.": "NWT", "Greenland": "GRL", "Alberta": "ALB", "Ontario": "ONT", "Quebec": "QUE", "Western US": "WUS", "Eastern US": "EUS", "Central America": "CAM",
        "Venezuela": "VEN", "Peru": "PER", "Brazil": "BRA", "Argentina": "ARG",
        "Iceland": "ICE", "Scandinavia": "SCA", "Ukraine": "UKR", "Great Britain": "GBR", "Northern Europe": "NEU", "Western Europe": "WEU", "Southern Europe": "SEU",
        "North Africa": "NAF", "Egypt": "EGY", "East Africa": "EAF", "Congo": "CON", "South Africa": "SAF", "Madagascar": "MAD",
        "Siberia": "SIB", "Yakutsk": "YAK", "Kamchatka": "KAM", "Ural": "URA", "Irkutsk": "IRK", "Mongolia": "MON", "Japan": "JAP", "Afghanistan": "AFG", "China": "CHI", "Middle East": "MEA", "India": "IND", "Siam": "SIA",
        "Indonesia": "IDO", "New Guinea": "NGU", "Western Australia": "WAU", "Eastern Australia": "EAU"
    }
    
    # On déplace le texte (y - 0.3) pour le mettre SOUS le cercle
    pos_labels = {k: (v[0], v[1]-0.4) for k, v in pos.items()}
    nx.draw_networkx_labels(G, pos_labels, font_size=8, font_family='sans-serif')


    legend_text = (
        "CONTINENTS & BONUS\n\n"
        "● Amérique N. (4) : +5\n"
        "● Amérique S. (4) : +2\n"
        "● Europe (7) : +5\n"
        "● Afrique (6) : +3\n"
        "● Asie (12) : +7\n"
        "● Océanie (4) : +2"
    )
    plt.text(0.5, 0.5, legend_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    dessiner_carte_risk_complete()