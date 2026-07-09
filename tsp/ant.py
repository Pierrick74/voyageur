from enum import Enum


class Etat(Enum):
    """État de la fourmi, en route, en retour .."""

    RECHERCHE_CHEMIN = "recherche_chemin"
    RETOUR = "retour"
    RIEN = "rien"


class Fourmi:
    def __init__(self, data):
        # on donne à chaque fourmi les données du problème et la connaissance collective
        self._data = data

        self.villes_visitees = []  # toutes les villes visitées par la fourmi
        self.villes_a_visiter = []  # toutes les villes encore à visiter
        self.longueur_visitee = 0  # compteur de longueur du chemin parcouru
        self.etat = Etat.RECHERCHE_CHEMIN

        # données de parcours locales
        self._taille_arc_courant = 0.0  # longueur de l'arc actuellement parcouru
        self._pos_arc_courant = 0.0  # position sur l'arc actuellement parcouru
        self._origine_courante = 0  # première extrémité de l'arc actuellement parcouru
        self._destination_courante = 0  # seconde extrémité de l'arc actuellement parcouru

    def frame(self):
        """Faire évoluer la fourmi à chaque itération."""
        if self.etat is Etat.RIEN:
            self._trouver_prochaine_destination()
            return

        # seule une fourmi en recherche compte la longueur parcourue ;
        # les deux états avancent ensuite sur l'arc (fallthrough du switch C++)
        if self.etat is Etat.RECHERCHE_CHEMIN:
            self.longueur_visitee += 1

        self._pos_arc_courant += 1
        if self._pos_arc_courant >= self._taille_arc_courant:
            self._trouver_prochaine_destination()

    def _trouver_prochaine_destination(self):
        """Détermination du prochain nœud à atteindre."""
        raise NotImplementedError

    def _ville_proche(self, origine):
        """Choix pondéré de nœud."""
        raise NotImplementedError
