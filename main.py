from carte import add_markers, create_map, draw_route
from carte.distance import distance_km, summary_distance_km
from carte.op2 import optimisation
from carte.ville import Ville
from data import POINTS, lire_villes
from carte.glouton import glouton

# Lecture des villes depuis le fichier CSV
points = lire_villes("70villes.csv")

# Carte centrée sur la France
carte = create_map()

add_markers(carte, points)

ville = Ville(points)
points = ville.trajet_voisins(depart="Ville 1")
summary_distance = summary_distance_km(points)
print(f"Distance totale (voisins) : {summary_distance:.2f} km\n")

for i in range(len(points)):
    print(points[i][2])

print("\nOptimisation :")


pointsOptimised = optimisation(ville).optimiser_trajet(points)

summary_distance = summary_distance_km(pointsOptimised)
print(f"Distance totale (optimisée) : {summary_distance:.2f} km\n")

for i in range(len(pointsOptimised)):
    print(pointsOptimised[i][2])


ville = Ville(points)
glouton = glouton(ville).trajet_glouton(depart="Ville 1")
summary_distance = summary_distance_km(glouton)
print(f"Distance totale (glouton) : {summary_distance:.2f} km\n")

for i in range(len(glouton)):
    print(glouton[i][2])
    

for i in range(len(pointsOptimised) - 1):
    draw_route(carte, [pointsOptimised[i], pointsOptimised[i+1]])



# Exporte une carte HTML interactive
carte.save("carte.html")
print("Carte générée → carte.html")
