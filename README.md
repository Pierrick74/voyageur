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

Le script lit `70villes.csv`, construit un trajet par chacune des trois méthodes,
affiche la distance totale de chacune, puis exporte le trajet optimisé dans `carte.html`
(à ouvrir dans un navigateur).

Sortie typique :

```
Distance totale (voisins) : 730.29 km
Distance totale (optimisée) : 629.71 km
Distance totale (glouton) : 714.80 km
Carte générée → carte.html
```

## Algorithmes

Les trois méthodes produisent un circuit fermé (retour à la ville de départ).

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

Le 2-opt n'est pour l'instant appliqué qu'au trajet du plus proche voisin ; l'appliquer
aussi au circuit glouton serait la suite logique.

## Structure

```
main.py             point d'entrée : lit le CSV, lance les 3 algos, écrit carte.html
data.py             lire_villes() — parse le CSV en points (lat, lon, nom)
carte.py            rendu folium : create_map, add_markers, draw_route
70villes.csv        70 coordonnées (latitude, longitude)
tsp/
  ville.py          classe Ville : distances, plus proche voisin, trajet_voisins
  distance.py       distance_km (géodésique), summary_distance_km (total d'un trajet)
  deux_opt.py       optimiser_trajet() — 2-opt
  glouton.py        trajet_glouton() — insertion gloutonne
```

L'algorithmique (`tsp/`) est séparée du rendu (`carte.py`) : rien dans `tsp/` n'importe
folium, et `carte.py` ne connaît que des tuples `(lat, lon, nom)`.

Le format de point utilisé partout est le tuple `(latitude, longitude, nom)`. Les villes
n'ont pas de nom réel dans le CSV : elles sont numérotées `Ville 1` … `Ville 70` à la lecture.

Les 70 villes tiennent dans un carré d'environ 1° de côté autour de (45.49, 5.49) — la
région Isère / Ain. C'est ce que `create_map()` cadre par défaut.
