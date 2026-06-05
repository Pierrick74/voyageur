from geopy.distance import geodesic


def distance_km(point_a, point_b):
    """Distance géodésique en km entre deux points (lat, lon, ...).

    Seules les deux premières valeurs (lat, lon) sont utilisées,
    ce qui permet de passer directement des points (lat, lon, nom).
    """
    a = (point_a[0], point_a[1])
    b = (point_b[0], point_b[1])
    return geodesic(a, b).km

def summary_distance_km(villes):
    """Distance totale d'un trajet fermé (liste de points)."""
    total = 0.0
    n = len(villes)
    for i in range(n - 1):
        total += distance_km(villes[i], villes[i + 1])
    return total