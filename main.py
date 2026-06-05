from carte import add_markers, create_map, draw_route
from carte.distance import distance_km
from carte.op2 import optimisation
from carte.ville import Ville
from data import POINTS

# Carte centrée sur la France
carte = create_map()

add_markers(carte, POINTS)

ville = Ville(POINTS)
points = ville.trajet_voisins(depart="Mairie")

for i in range(len(points)):
    print(points[i][2])

print("\nOptimisation :")


pointsOptimised = optimisation(ville).optimiser_trajet(points)

for i in range(len(pointsOptimised)):
    print(pointsOptimised[i][2])

for i in range(len(pointsOptimised) - 1):
    draw_route(carte, [pointsOptimised[i], pointsOptimised[i+1]])



# Exporte une carte HTML interactive
carte.save("carte.html")
print("Carte générée → carte.html")
