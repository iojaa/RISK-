from pyclbr import Class

class Dés:
    def __init__(self, nombre_faces):
        self.nombre_faces = nombre_faces

    def lancer(self):
        import random
        return random.randint(1, self.nombre_faces)

def lances_de_dés(nombre_lances):
    dés = Dés(6)  # Un dé à 6 faces
    résultats = []
    for i in range(nombre_lances):
        résultats.append(dés.lancer())
    return résultats


# print(lances_de_dés(5))  # Exemple de lancer de 5 dés

class Carte:
    def __init__(self, territoires, arme):
        self.territoires = territoires
        self.arme = arme
    def __repr__(self):
        return f"( {self.territoires} | {self.arme})"

def créer_cartes():
    cartes = []
    territoires = ["Alaska", "Northwest Terr.", "Greenland", "Alberta", "Ontario", "Quebec", "Western US", "Eastern US", "Central America",
                    "Venezuela", "Peru", "Brazil", "Argentina",
                    "Iceland", "Scandinavia", "Ukraine", "Great Britain", "Northern Europe", "Western Europe", "Southern Europe",
                    "North Africa", "Egypt", "East Africa", "Congo", "South Africa", "Madagascar",
                    "Siberia", "Yakutsk", "Kamchatka", "Ural", "Irkutsk", "Mongolia", "Japan",
                    "Afghanistan", "China", "Middle East", "India", "Siam","Eastern Australia", "Western Australia", "New Guinea", "Indonesia"]
    armes = ["Fantassin", "Cavalier", "Canon"]
    for i in range (42):  # 42 territoires dans RISK
        if territoires[i] in ["Alaska", "North Africa", "Alberta", "Western US","Argentina","Egypt","Eastern Australia",
                              "Afghanistan", "India","Western US","Eastern Europe","Iceland","Japan","Madagascar","Irkutsk"]:
            carte=Carte(territoires[i], armes[0])  # Associe chaque territoire à une arme de manière cyclique
        elif territoires[i] in [ "Peru","Central America","China","Congo","Northern Europe","Southern Europe","Great Britain","Greenland",
                                "Indonesia","Kamchatka","Ontario","Ural","Yakutsk"]:
            carte=Carte(territoires[i], armes[1])
        else:
            carte=Carte(territoires[i], armes[2])
        cartes.append(carte)
    return cartes





class Territoire:
    def __init__(self, nom):
        self.nom = nom
        self.propriétaire = None
        self.nombre_armées = 0

    def __repr__(self):
        return f"{self.nom} (Propriétaire: {self.propriétaire}, Armées: {self.nombre_armées})"
    
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.territoires = []
        self.cartes = []

    def __repr__(self):
        return f"{self.nom} (Territoires: {len(self.territoires)}, Cartes: {len(self.cartes)})"
     
class Continent:
    def __init__(self, nom, territoires):
        self.nom = nom
        self.territoires = territoires

    def __repr__(self):
        return f"{self.nom} (Territoires: {len(self.territoires)})"
    
Europe = Continent("Europe", ["Iceland", "Scandinavia", "Ukraine", "Great Britain", "Northern Europe", "Western Europe", "Southern Europe"])
Africa = Continent("Africa", ["North Africa", "Egypt", "East Africa", "Congo", "South Africa", "Madagascar"])
Asia = Continent("Asia", ["Siberia", "Yakutsk", "Kamchatka", "Ural", "Irkutsk", "Mongolia", "Japan",
                    "Afghanistan", "China", "Middle East", "India", "Siam","Eastern Australia", "Western Australia", "New Guinea", "Indonesia"])
North_America = Continent("North America", ["Alaska", "Northwest Terr.", "Greenland", "Alberta", "Ontario", "Quebec", "Western US", "Eastern US", "Central America"])
South_America = Continent("South America", ["Venezuela", "Peru", "Brazil", "Argentina"])
Oceania = Continent("Oceania", ["Indonesia", "New Guinea", "Western Australia", "Eastern Australia"])
