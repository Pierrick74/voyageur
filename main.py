from carte import add_markers, create_map, draw_route
from carte.distance import distance_km
from carte.ville import Ville
from data import POINTS

# Carte centrée sur la France
carte = create_map()

add_markers(carte, POINTS)

ville = Ville(POINTS)
points = ville.trajet_voisins(depart="Mairie")

for i in range(len(points) - 1):
    draw_route(carte, [points[i], points[i+1]])

for i in range(len(points)):
    print(points[i][2])

# Exporte une carte HTML interactive
carte.save("carte.html")
print("Carte générée → carte.html")
