import folium


def create_map(location=(45.49, 5.49), zoom_start=9):
    """Crée une carte folium centrée par défaut sur la zone couverte par 70villes.csv."""
    return folium.Map(location=list(location), zoom_start=zoom_start)


def add_markers(carte, points):
    """Affiche un marqueur cliquable pour chaque point (lat, lon, nom)."""
    for lat, lon, nom in points:
        folium.Marker(
            location=[lat, lon],
            popup=nom,
            icon=folium.Icon(color="red", icon="info-sign"),  # prefix glyphicon par défaut
        ).add_to(carte)


def draw_route(carte, points):
    """Trace une ligne reliant les points (lat, lon, nom)."""
    trace = [(lat, lon) for lat, lon, _ in points]
    folium.PolyLine(locations=trace, color="blue", weight=2.5, opacity=0.8).add_to(carte)

