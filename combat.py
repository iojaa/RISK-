"""
combat.py — Logique de combat RISK
S'appuie sur objets.py sans le modifier.
"""

import objets  # lances_de_dés, Territoire, Joueur


# ---------------------------------------------------------------------------
# FRONTIÈRES — graphe d'adjacence des 42 Territoires
# ---------------------------------------------------------------------------

FRONTIERES: dict[str, list[str]] = {
    "Alaska":             ["Northwest Terr.", "Alberta", "Kamchatka"],
    "Northwest Terr.":    ["Alaska", "Alberta", "Ontario", "Greenland"],
    "Greenland":          ["Northwest Terr.", "Ontario", "Quebec", "Iceland"],
    "Alberta":            ["Alaska", "Northwest Terr.", "Ontario", "Western US"],
    "Ontario":            ["Northwest Terr.", "Alberta", "Quebec", "Western US", "Eastern US", "Greenland"],
    "Quebec":             ["Ontario", "Eastern US", "Greenland"],
    "Western US":         ["Alberta", "Ontario", "Eastern US", "Central America"],
    "Eastern US":         ["Ontario", "Quebec", "Western US", "Central America"],
    "Central America":    ["Western US", "Eastern US", "Venezuela"],
    "Venezuela":          ["Central America", "Brazil", "Peru"],
    "Peru":               ["Venezuela", "Brazil", "Argentina"],
    "Brazil":             ["Venezuela", "Peru", "Argentina", "North Africa"],
    "Argentina":          ["Peru", "Brazil"],
    "Iceland":            ["Greenland", "Great Britain", "Scandinavia"],
    "Scandinavia":        ["Iceland", "Great Britain", "Northern Europe", "Ukraine"],
    "Ukraine":            ["Scandinavia", "Northern Europe", "Southern Europe", "Ural", "Afghanistan", "Middle East"],
    "Great Britain":      ["Iceland", "Scandinavia", "Western Europe", "Northern Europe"],
    "Northern Europe":    ["Great Britain", "Scandinavia", "Western Europe", "Southern Europe", "Ukraine"],
    "Western Europe":     ["Great Britain", "Northern Europe", "Southern Europe", "North Africa"],
    "Southern Europe":    ["Western Europe", "Northern Europe", "Ukraine", "North Africa", "Egypt", "Middle East"],
    "North Africa":       ["Brazil", "Western Europe", "Southern Europe", "Egypt", "East Africa", "Congo"],
    "Egypt":              ["North Africa", "Southern Europe", "East Africa", "Middle East"],
    "East Africa":        ["North Africa", "Egypt", "Congo", "South Africa", "Madagascar"],
    "Congo":              ["North Africa", "East Africa", "South Africa"],
    "South Africa":       ["Congo", "East Africa", "Madagascar"],
    "Madagascar":         ["East Africa", "South Africa"],
    "Ural":               ["Ukraine", "Siberia", "Afghanistan"],
    "Siberia":            ["Ural", "Yakutsk", "Irkutsk", "Mongolia"],
    "Yakutsk":            ["Siberia", "Kamchatka", "Irkutsk"],
    "Kamchatka":          ["Alaska", "Yakutsk", "Irkutsk", "Mongolia", "Japan"],
    "Irkutsk":            ["Siberia", "Yakutsk", "Kamchatka", "Mongolia"],
    "Mongolia":           ["Siberia", "Kamchatka", "Irkutsk", "Japan", "China"],
    "Japan":              ["Kamchatka", "Mongolia"],
    "Afghanistan":        ["Ukraine", "Ural", "China", "Middle East", "India"],
    "China":              ["Afghanistan", "Mongolia", "India", "Siam"],
    "Middle East":        ["Ukraine", "Southern Europe", "Egypt", "Afghanistan", "India"],
    "India":              ["Afghanistan", "China", "Middle East", "Siam"],
    "Siam":               ["China", "India", "Indonesia"],
    "Indonesia":          ["Siam", "New Guinea", "Western Australia"],
    "New Guinea":         ["Indonesia", "Western Australia", "Eastern Australia"],
    "Western Australia":  ["Indonesia", "New Guinea", "Eastern Australia"],
    "Eastern Australia":  ["New Guinea", "Western Australia"],
}


def sont_voisins(nom1: str, nom2: str) -> bool:
    """Retourne True si les deux Territoires partagent une frontière."""
    return nom2 in FRONTIERES.get(nom1, [])


# ---------------------------------------------------------------------------
# RÉSOLUTION D'UN ROUND
# ---------------------------------------------------------------------------

def _résoudre_round(dés_att: list[int], dés_def: list[int]) -> tuple[int, int]:
    """
    Compare les dés paire par paire (déjà triés décroissant).
    Règle : en cas d'égalité, le défenseur gagne.
    Retourne (pertes_attaquant, pertes_défenseur).
    """
    pertes_att, pertes_def = 0, 0
    for da, dd in zip(dés_att, dés_def):
        if da > dd:
            pertes_def += 1
        else:
            pertes_att += 1
    return pertes_att, pertes_def


# ---------------------------------------------------------------------------
# COMBAT PRINCIPAL
# ---------------------------------------------------------------------------

def combat(territoire_att: objets.Territoire,
           territoire_def: objets.Territoire,
           nb_dés_att: int = None,
           nb_dés_def: int = None,
           verbeux: bool = True) -> dict:
    """
    Résout un combat RISK complet entre deux Territoires.

    Règles officielles :
    - Attaquant : 1 à 3 dés, mais doit garder au moins 1 armée sur place.
    - Défenseur : 1 à 2 dés.
    - Comparaison paire par paire du plus grand au plus petit.
    - Égalité → le défenseur gagne.
    - Combat en rounds jusqu'à conquête ou arrêt faute d'armées.
    - Si conquête : l'attaquant déplace autant d'armées que de dés joués au dernier round.

    Paramètres
    ----------
    territoire_att  : Territoire attaquant (>= 2 armées requises)
    territoire_def  : Territoire défenseur (>= 1 armée requise)
    nb_dés_att      : Dés forcés pour l'attaquant (None = maximum autorisé)
    nb_dés_def      : Dés forcés pour le défenseur (None = maximum autorisé)
    verbeux         : Affiche le déroulé round par round

    Retourne un dict :
    {
        "conquis":          bool,
        "pertes_attaquant": int,
        "pertes_défenseur": int,
        "rounds":           list[dict]   # détail de chaque round
    }
    """

    # --- Validations ---
    if territoire_att.propriétaire is territoire_def.propriétaire:
        raise ValueError("Un joueur ne peut pas attaquer son propre territoire.")
    if territoire_att.nombre_armées < 2:
        raise ValueError(f"{territoire_att.nom} doit avoir au moins 2 armées pour attaquer.")
    if territoire_def.nombre_armées < 1:
        raise ValueError(f"{territoire_def.nom} n'a plus d'armées.")
    if not sont_voisins(territoire_att.nom, territoire_def.nom):
        raise ValueError(f"{territoire_att.nom} et {territoire_def.nom} ne sont pas voisins.")

    nom_att = territoire_att.propriétaire.nom if territoire_att.propriétaire else "Attaquant"
    nom_def = territoire_def.propriétaire.nom if territoire_def.propriétaire else "Défenseur"

    résultat = {"conquis": False, "pertes_attaquant": 0, "pertes_défenseur": 0, "rounds": []}
    dernier_nb_dés_att = 1  # pour le déplacement final

    if verbeux:
        print("=" * 60)
        print(f"⚔️  {nom_att} [{territoire_att.nom} — {territoire_att.nombre_armées} arm.]"
              f"  →  {nom_def} [{territoire_def.nom} — {territoire_def.nombre_armées} arm.]")
        print("=" * 60)

    num_round = 0
    while territoire_att.nombre_armées >= 2 and territoire_def.nombre_armées >= 1:
        num_round += 1

        max_att = min(3, territoire_att.nombre_armées - 1)
        max_def = min(2, territoire_def.nombre_armées)

        dés_att = max(1, min(nb_dés_att or max_att, max_att))
        dés_def = max(1, min(nb_dés_def or max_def, max_def))
        dernier_nb_dés_att = dés_att

        lancers_att = objets.lances_de_dés(dés_att)
        lancers_def = objets.lances_de_dés(dés_def)

        lancers_att.sort(reverse=True)
        lancers_def.sort(reverse=True)

        pertes_att, pertes_def = _résoudre_round(lancers_att, lancers_def)

        territoire_att.nombre_armées -= pertes_att
        territoire_def.nombre_armées -= pertes_def
        résultat["pertes_attaquant"] += pertes_att
        résultat["pertes_défenseur"] += pertes_def

        résultat["rounds"].append({
            "round": num_round,
            "dés_att": lancers_att, "dés_def": lancers_def,
            "pertes_att": pertes_att, "pertes_def": pertes_def,
            "armées_att": territoire_att.nombre_armées,
            "armées_def": territoire_def.nombre_armées,
        })

        if verbeux:
            print(f"\n  Round {num_round}")
            print(f"    🎲 {nom_att} : {lancers_att}  →  -{pertes_att} armée(s)")
            print(f"    🛡️  {nom_def} : {lancers_def}  →  -{pertes_def} armée(s)")
            print(f"    Reste → Att : {territoire_att.nombre_armées}  |  Déf : {territoire_def.nombre_armées}")

    # --- Résolution finale ---
    if territoire_def.nombre_armées == 0:
        résultat["conquis"] = True

        # Transfert de propriété
        ancien_proprio = territoire_def.propriétaire
        if ancien_proprio and territoire_def in ancien_proprio.Territoires:
            ancien_proprio.Territoires.remove(territoire_def)
        territoire_def.propriétaire = territoire_att.propriétaire
        if territoire_att.propriétaire:
            territoire_att.propriétaire.Territoires.append(territoire_def)

        # Déplacement d'armées (au moins autant que de dés joués au dernier round)
        à_déplacer = min(dernier_nb_dés_att, territoire_att.nombre_armées - 1)
        territoire_att.nombre_armées -= à_déplacer
        territoire_def.nombre_armées = à_déplacer

        if verbeux:
            print(f"\n  ✅ {nom_att} conquiert {territoire_def.nom} !")
            print(f"     {à_déplacer} armée(s) avancent sur le territoire.")
    else:
        if verbeux:
            print(f"\n  🛡️  {nom_def} résiste. L'attaque est stoppée.")

    if verbeux:
        print(f"\n  Bilan — Pertes att : {résultat['pertes_attaquant']}"
              f"  |  Pertes déf : {résultat['pertes_défenseur']}"
              f"  |  Conquis : {résultat['conquis']}")
        print("=" * 60)

    return résultat
