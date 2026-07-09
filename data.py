import csv


def lire_villes(chemin="70villes.csv"):
    """Lit un fichier CSV (latitude, longitude) et renvoie une liste
    de points au format (latitude, longitude, nom)."""
    points = []
    with open(chemin, newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        for i, ligne in enumerate(lecteur, start=1):
            lat = float(ligne["latitude"])
            lon = float(ligne["longitude"])
            points.append((lat, lon, f"Ville {i}"))
    return points
