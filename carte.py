import folium

# Carte centrée sur Paris (lat, lon) + zoom
carte = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Un marqueur cliquable
folium.Marker(
    location=[48.8584, 2.2945],
    popup="Tour Eiffel",
    tooltip="Clique-moi",
    icon=folium.Icon(color="red", icon="info-sign"),  # prefix glyphicon par défaut
).add_to(carte)

# Exporte une carte HTML interactive
carte.save("carte.html")
print("Carte générée → carte.html")