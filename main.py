from time import perf_counter

from carte import add_markers, create_map, draw_route
from data import lire_villes
from tsp import (
    Colonie,
    Probleme,
    Ville,
    optimiser_trajet,
    summary_distance_km,
    trajet_glouton,
)


def mesurer(titre, calcul):
    """Exécute `calcul`, affiche la distance du trajet obtenu et le temps mis."""
    debut = perf_counter()
    trajet = calcul()
    duree = perf_counter() - debut
    print(f"Distance totale ({titre}) : {summary_distance_km(trajet):.2f} km en {duree:.2f} s")
    return trajet


# Lecture des villes depuis le fichier CSV
points = lire_villes("70villes.csv")
ville = Ville(points)

trajetVoisins = mesurer("voisins", lambda: ville.trajet_voisins(depart="Ville 1"))

trajetOptimise = mesurer("optimisée", lambda: optimiser_trajet(trajetVoisins))

trajetGlouton = mesurer("glouton", lambda: trajet_glouton(ville, depart="Ville 1"))


# Colonie de fourmis : le tour glouton sert de cible à atteindre
def calculer_fourmis():
    probleme = Probleme.depuis_ville(ville)
    colonie = Colonie(probleme, nb_fourmis=100)
    colonie.run(1000000)
    boucle = colonie.meilleur_chemin + [colonie.meilleur_chemin[0]]
    return ville.rebuild_points(boucle)


trajetFourmis = mesurer("fourmis", calculer_fourmis)

# Carte HTML interactive du meilleur trajet
carte = create_map()
add_markers(carte, points)
draw_route(carte, trajetFourmis)
carte.save("carte.html")
print("Carte générée → carte.html")
