# RISK - Adaptation Numérique du Jeu de Société

Ce projet est une adaptation numérique en Python du célèbre jeu de stratégie au tour par tour RISK. Développé dans le cadre de la Licence 1 SPI à l'Université d'Angers, il combine une modélisation orientée objet de la logique de jeu, une structure de données topologique basée sur la théorie des graphes et une interface utilisateur interactive synchronisée en temps réel.

## Fonctionnalités
- Modélisation Complète : Gestion des 42 territoires mondiaux répartis sur 6 continents, respectant les frontières officielles.
- Système de Combat Authentique : Simulation stochastique des lancers de dés (jusqu'à 3 dés pour l'attaquant, 2 pour le défenseur) avec tri décroissant et résolution automatique des pertes et conquêtes.
- Interface Graphique Interactive : Cartographie dynamique générée via matplotlib et networkx avec mise en surbrillance rouge du territoire sélectionné pour l'attaque.
- Automate à États : Gestion stricte des phases de jeu (Renforcement initial, Renforcement par tour, Attaque) et détection automatique de la condition de victoire (contrôle absolu des 42 territoires).

---

## Architecture du Code

Le projet est découpé en modules spécialisés pour garantir une séparation claire entre la logique métier et l'interface utilisateur :

1. objets.py : Contient les briques fondamentales en Programmation Orientée Objet (Dés, Carte, Territoire, Joueur, Continent).
2. game.py : Orchestre la structure globale de la partie (Partie), la distribution des cartes initiales et la répartition des armées.
3. combat.py : Contient la matrice d'adjacence des frontières mondiales (Graphe non orienté) et l'algorithme de résolution des affrontements par comparaison de vecteurs de dés.
4. carte2.py : Gère l'affichage graphique, le positionnement des nœuds géographiques, l'application des couleurs des joueurs et le placage des labels numériques.
5. main_guy.py : Le point d'entrée de l'application. Il capture les événements de clics de souris (architecture événementielle), calcule les distances euclidiennes pour identifier le territoire ciblé, et pilote l'automate de jeu.

---

## Installation et Lancement

### Prérequis
Assurez-vous d'avoir Python 3.8+ installé, ainsi que les bibliothèques requises :
```bash
pip install matplotlib networkx pillow
