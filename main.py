from carte import add_markers, create_map, draw_route
from data import POINTS

# Carte centrée sur la France
carte = create_map()

add_markers(carte, POINTS)
draw_route(carte, POINTS)

# Exporte une carte HTML interactive
carte.save("carte.html")
print("Carte générée → carte.html")
