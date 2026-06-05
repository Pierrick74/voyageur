import folium

# Carte centrée sur Paris (lat, lon) + zoom
carte = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Liste des points : (latitude, longitude, nom)
points = [
    (48.8584, 2.2945, "Tour Eiffel"),
    (45.90787713169338, 6.102644924842454, "Les papetteries"),
]

# Un marqueur cliquable par point
for lat, lon, nom in points:
    folium.Marker(
        location=[lat, lon],
        popup=nom,
        icon=folium.Icon(color="red", icon="info-sign"),  # prefix glyphicon par défaut
    ).add_to(carte)

trace = [(lat, lon) for lat, lon, _ in points]
folium.PolyLine(locations=trace, color="blue", weight=2.5, opacity=0.8).add_to(carte)

# Exporte une carte HTML interactive
carte.save("carte.html")
print("Carte générée → carte.html")