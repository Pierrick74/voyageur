from geopy.distance import geodesic


def distance_km(point_a, point_b):
    """Distance géodésique en km entre deux points (lat, lon, ...).

    Seules les deux premières valeurs (lat, lon) sont utilisées,
    ce qui permet de passer directement des points (lat, lon, nom).
    """
    a = (point_a[0], point_a[1])
    b = (point_b[0], point_b[1])
    return geodesic(a, b).km
