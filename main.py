from carte import add_markers, create_map, draw_route
from carte.distance import distance_km
from data import POINTS

# Carte centrée sur la France
carte = create_map()

add_markers(carte, POINTS)
draw_route(carte, POINTS)

distance = distance_km(POINTS[0], POINTS[1])
print(f"Distance entre {POINTS[0][2]} et {POINTS[1][2]} : {distance:.2f} km")

# Exporte une carte HTML interactive
carte.save("carte.html")
print("Carte générée → carte.html")
