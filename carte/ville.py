import numpy as np

from carte.distance import distance_km


class Ville:
    def __init__(self, points=None):
        points = points if points is not None else []
        self.destinations = np.array([(p[0], p[1]) for p in points], dtype=float)
        self.noms = [p[2] if len(p) > 2 else None for p in points]

    def nom(self, i):
        """Nom de la destination i (None si non renseigné)"""
        return self.noms[i]

    def distance(self, i, j):
        """Distance géodésique (km) entre deux destinations"""
        return distance_km(self.destinations[i], self.destinations[j])

    def plus_proche(self, i, exclus=None):
        """Retourne l'indice de la destination la plus proche de i, hors exclus"""
        exclus = set(exclus) if exclus is not None else set()
        distances = []
        for j in range(len(self.destinations)):
            if j not in exclus:
                d = self.distance(i, j)
                distances.append((d, j))

        distances.sort(key=lambda x: x[0])
        return distances[0][1] if distances else None

    def trajet_voisins(self, depart=""):
        n = len(self.destinations)
        try:
            depart_index = self.noms.index(depart) if depart else 0
        except ValueError:
            raise ValueError(f"Départ '{depart}' non trouvé parmi les destinations")
        visites = [depart_index]
        actuel = depart_index

        for _ in range(n - 1):
            next_ville = self.plus_proche(actuel, exclus=visites)
            if next_ville is not None:
                visites.append(next_ville)
                actuel = next_ville

        visites.append(depart_index)  # retour au point de départ (boucle fermée)
        points = self.rebuild_points(visites)

        return points

    def rebuild_points(self, visites):
        points = []
        for i in visites:
            points.append((self.destinations[i][0], self.destinations[i][1], self.noms[i]))
        return points
    
            

