from carte import add_markers, create_map, draw_route
from data import lire_villes
from tsp import Ville, optimiser_trajet, summary_distance_km, trajet_glouton


def afficher(titre, trajet):
    print(f"Distance totale ({titre}) : {summary_distance_km(trajet):.2f} km\n")
    for point in trajet:
        print(point[2])
    print()


# Lecture des villes depuis le fichier CSV
points = lire_villes("70villes.csv")
ville = Ville(points)

trajetVoisins = ville.trajet_voisins(depart="Ville 1")
afficher("voisins", trajetVoisins)

trajetOptimise = optimiser_trajet(trajetVoisins)
afficher("optimisée", trajetOptimise)

trajetGlouton = trajet_glouton(ville, depart="Ville 1")
afficher("glouton", trajetGlouton)

# Carte HTML interactive du meilleur trajet
carte = create_map()
add_markers(carte, points)
draw_route(carte, trajetOptimise)
carte.save("carte.html")
print("Carte générée → carte.html")
