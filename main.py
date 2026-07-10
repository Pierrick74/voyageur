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


def afficher(titre, trajet):
    print(f"Distance totale ({titre}) : {summary_distance_km(trajet):.2f} km")


# Lecture des villes depuis le fichier CSV
points = lire_villes("7villes.csv")
ville = Ville(points)

trajetVoisins = ville.trajet_voisins(depart="Ville 1")
afficher("voisins", trajetVoisins)

trajetOptimise = optimiser_trajet(trajetVoisins)
afficher("optimisée", trajetOptimise)

#trajetGlouton = trajet_glouton(ville, depart="Ville 1")
#afficher("glouton", trajetGlouton)

# Colonie de fourmis : le tour glouton sert de cible à atteindre
probleme = Probleme.depuis_ville(ville)

colonie = Colonie(probleme, nb_fourmis=100)
# get current time

# 

colonie.run(1000000)

boucle = colonie.meilleur_chemin + [colonie.meilleur_chemin[0]]
trajetFourmis = ville.rebuild_points(boucle)
afficher("fourmis", trajetFourmis)

# Carte HTML interactive du meilleur trajet
carte = create_map()
add_markers(carte, points)
draw_route(carte, trajetFourmis)
carte.save("carte.html")
print("Carte générée → carte.html")
