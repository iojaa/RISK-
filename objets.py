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


print(lances_de_dés(5))  # Exemple de lancer de 5 dés

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

print(créer_cartes())