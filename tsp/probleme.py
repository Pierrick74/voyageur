class Probleme:
    """Données du problème + connaissance collective de la colonie."""

    def __init__(self, distances, borne_min=0.1, borne_max=10.0, evaporation=5.0):
        self.distances = distances
        self.nb_villes = len(distances)

        self.borne_min = borne_min  # plancher : un arc n'est jamais totalement oublié
        self.borne_max = borne_max  # plafond : évite qu'un arc écrase tous les autres
        self.evaporation = evaporation  # pourcentage évaporé à chaque tour

        self.longueur_optimale = 0  # meilleure longueur connue, sert d'échelle au dépôt

        # au départ tous les arcs sont également attractifs
        self.pheromones = [[borne_max] * self.nb_villes for _ in range(self.nb_villes)]

    @classmethod
    def depuis_ville(cls, ville, **kwargs):
        """Construit la matrice des distances (km) à partir d'un objet Ville."""
        n = len(ville.destinations)
        distances = [[ville.distance(i, j) for j in range(n)] for i in range(n)]
        return cls(distances, **kwargs)

    def set_pheromones(self, i, j, longueur):
        """Dépose sur l'arc (i, j) : plus le tour est court, plus le dépôt est fort."""

        valeur = self.pheromones[i][j] + 100
        self.pheromones[i][j] = valeur
        self.pheromones[j][i] = valeur

    def evaporate(self):
        """Diminue le taux de phéromones sur chacun des arcs, sans passer sous borne_min."""
        facteur = (100 - self.evaporation) / 100
        for i in range(self.nb_villes):
            for j in range(i):
                valeur = max(self.pheromones[i][j] * facteur, self.borne_min)
                self.pheromones[i][j] = valeur
                self.pheromones[j][i] = valeur
