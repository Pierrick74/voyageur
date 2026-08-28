# Voyageur de commerce

Résolution approchée du problème du voyageur de commerce (TSP) sur un jeu de 70 villes,
avec génération d'une carte HTML interactive du trajet.

Les distances sont géodésiques (calculées par `geopy` sur les coordonnées lat/lon),
pas euclidiennes.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

Le script lit `70villes.csv`, construit un trajet par chacune des quatre méthodes,
affiche la distance totale et le temps de calcul de chacune, puis exporte le trajet
de la colonie de fourmis dans `carte.html` (à ouvrir dans un navigateur).

Sortie typique :

```
Distance totale (voisins) : 730.29 km en 0.15 s
Distance totale (optimisée) : 629.71 km en 1.20 s
Distance totale (glouton) : 714.80 km en 0.30 s
Distance totale (fourmis) : ... km en ... s
Carte générée → carte.html
```

Les trois premières distances sont stables (algorithmes déterministes) ; celle de la
colonie de fourmis varie d'une exécution à l'autre, et son temps de calcul dépend
directement du nombre d'itérations passé à `colonie.run()`.

## Algorithmes

Les quatre méthodes produisent un circuit fermé (retour à la ville de départ).

### Plus proche voisin — `tsp/ville.py`

`Ville.trajet_voisins(depart)` part d'une ville et rejoint à chaque étape la ville
non visitée la plus proche. Simple et rapide, mais glouton au sens naïf : les dernières
villes non visitées forcent souvent de longs sauts en fin de parcours.

### 2-opt — `tsp/deux_opt.py`

`optimiser_trajet(villes)` améliore un trajet existant. Pour chaque paire
d'arêtes `(a,b)` et `(c,d)`, si `d(a,c) + d(b,d) < d(a,b) + d(c,d)`, le segment entre
les deux est inversé — ce qui « décroise » le trajet. On répète jusqu'à ce qu'aucune
inversion n'améliore plus le total.

C'est une post-optimisation : elle prend le trajet du plus proche voisin en entrée.
Sur ce jeu de données, elle fait gagner ~100 km (−14 %).

### Insertion gloutonne — `tsp/glouton.py`

`trajet_glouton(ville, depart)` part d'un circuit dégénéré `[depart, depart]` et insère
les villes une à une, chacune à la position du circuit qui minimise la distance totale
résultante. Plus coûteux que le plus proche voisin, mais meilleur résultat (714 km contre
730 km) — un trajet construit par insertion se croise moins.

### Colonie de fourmis (ACO) — `tsp/ant.py`, `tsp/colonie.py`, `tsp/probleme.py`

Métaheuristique : au lieu de construire un trajet une fois, on en fait construire des
milliers par des agents qui s'échangent de l'information via une matrice de phéromones.

- **`Probleme`** (`tsp/probleme.py`) porte les données partagées : la matrice des
  distances (`Probleme.depuis_ville(ville)` la calcule depuis un objet `Ville`) et la
  matrice des phéromones. `set_pheromones(i, j, longueur)` dépose sur un arc,
  `evaporate()` fait décroître toutes les traces d'un pourcentage (`evaporation`), sans
  jamais passer sous `borne_min` — un arc n'est donc jamais définitivement oublié.
- **`Fourmi`** (`tsp/ant.py`) est une machine à états (`RIEN` → `RECHERCHE_CHEMIN` →
  `RETOUR`) avancée frame par frame. En `RECHERCHE_CHEMIN` elle choisit sa prochaine
  ville par tirage à la roulette pondéré par les phéromones (`_ville_proche`) ; une fois
  toutes les villes visitées, elle repasse en `RETOUR` et redépose des phéromones sur
  chaque arc qu'elle remonte. Arrivée au nid, elle lève `FourmiAEnregistrer` pour rendre
  son résultat à la colonie.
- **`Colonie`** (`tsp/colonie.py`) fait avancer toutes les fourmis d'une frame par
  itération de `run(n)`, retient le meilleur tour vu (`meilleur_chemin`,
  `meilleure_longueur`), remplace chaque fourmi qui a bouclé par une neuve, et déclenche
  l'évaporation périodiquement — comptée en **tours bouclés**, pas en frames : un tour
  dure des centaines de frames, évaporer à la frame effacerait les traces avant qu'elles
  ne guident quoi que ce soit.

Le déplacement est simulé en « temps » : une fourmi met autant de frames à traverser un
arc que sa longueur en km. Les arcs courts sont donc parcourus plus vite, ce qui renforce
naturellement les bons chemins — c'est le mécanisme d'origine de l'ACO.

`meilleur_chemin` est une liste d'indices de villes ; `main.py` la referme sur son
premier élément puis la repasse en points via `Ville.rebuild_points()`.

Le 2-opt n'est pour l'instant appliqué qu'au trajet du plus proche voisin ; l'appliquer
aussi au circuit glouton et au tour des fourmis serait la suite logique.

## Structure

```
main.py             point d'entrée : lit le CSV, lance les 4 algos, écrit carte.html
data.py             lire_villes() — parse le CSV en points (lat, lon, nom)
carte.py            rendu folium : create_map, add_markers, draw_route
70villes.csv        70 coordonnées (latitude, longitude)
tsp/
  ville.py          classe Ville : distances, plus proche voisin, trajet_voisins
  distance.py       distance_km (géodésique), summary_distance_km (total d'un trajet)
  deux_opt.py       optimiser_trajet() — 2-opt
  glouton.py        trajet_glouton() — insertion gloutonne
  probleme.py       classe Probleme : matrices distances + phéromones, dépôt, évaporation
  ant.py            classe Fourmi : machine à états, choix pondéré, dépôt au retour
  colonie.py        classe Colonie : boucle de simulation, meilleur tour, évaporation
```

L'algorithmique (`tsp/`) est séparée du rendu (`carte.py`) : rien dans `tsp/` n'importe
folium, et `carte.py` ne connaît que des tuples `(lat, lon, nom)`.

Le format de point utilisé partout est le tuple `(latitude, longitude, nom)`. Les villes
n'ont pas de nom réel dans le CSV : elles sont numérotées `Ville 1` … `Ville 70` à la lecture.
L'ACO, elle, travaille uniquement sur des indices de villes et une matrice de distances —
elle ignore tout des coordonnées.

Les 70 villes tiennent dans un carré d'environ 1° de côté autour de (45.49, 5.49) — la
région Isère / Ain. C'est ce que `create_map()` cadre par défaut.
