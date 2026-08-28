import random
from enum import Enum


class FourmiAEnregistrer(Exception):
    """La fourmi a bouclé son tour : la colonie doit enregistrer son résultat."""

    def __init__(self, fourmi):
        super().__init__("fourmi de retour au nid")
        self.fourmi = fourmi


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
        self.villes_a_visiter = list(range(data.nb_villes))  # toutes les villes encore à visiter
        self.longueur_visitee = 0  # compteur de longueur du chemin parcouru
        self.etat = Etat.RIEN  # au nid, elle partira à la première frame

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

        # la longueur est comptée arc par arc à l'arrivée, pas frame par frame :
        # sinon on l'ajouterait deux fois, et arrondie à l'unité
        self._pos_arc_courant += 1
        if self._pos_arc_courant >= self._taille_arc_courant:
            self._trouver_prochaine_destination()

    def _trouver_prochaine_destination(self):
        """Détermination du prochain nœud à atteindre."""
        if self.etat is Etat.RIEN:
            # la fourmi est au nid : elle entame un nouveau parcours depuis la ville 0
            self.villes_visitees.append(0)
            if 0 in self.villes_a_visiter:
                self.villes_a_visiter.remove(0)

            dest = self._ville_proche(0)
            self.etat = Etat.RECHERCHE_CHEMIN
            self._origine_courante = 0
            self._destination_courante = dest
            self._pos_arc_courant = 0
            self._taille_arc_courant = self._data.distances[0][dest]
            return

        if self.etat is Etat.RECHERCHE_CHEMIN:
            # on a atteint _destination_courante
            distances = self._data.distances
            arrivee = self._destination_courante

            self.longueur_visitee += distances[self._origine_courante][arrivee]
            self.villes_visitees.append(arrivee)
            if arrivee in self.villes_a_visiter:
                self.villes_a_visiter.remove(arrivee)

            if not self.villes_a_visiter:
                # plus rien à visiter, le chemin est complet : on revient vers le nid
                self.longueur_visitee += distances[arrivee][0]

                self.etat = Etat.RETOUR
                # en RETOUR, ces deux champs indexent villes_visitees, pas les villes
                self._origine_courante = len(self.villes_visitees) - 1
                self._destination_courante = len(self.villes_visitees) - 2
                self._taille_arc_courant = distances[
                    self.villes_visitees[self._origine_courante]
                ][self.villes_visitees[self._destination_courante]]
                self._pos_arc_courant = self._taille_arc_courant
                return

            dest = self._ville_proche(arrivee)
            self._origine_courante = arrivee
            self._destination_courante = dest
            self._taille_arc_courant = distances[arrivee][dest]
            self._pos_arc_courant = 0
            return

        if self.etat is Etat.RETOUR:
            distances = self._data.distances
            origine = self.villes_visitees[self._origine_courante]
            destination = self.villes_visitees[self._destination_courante]

            # on dépose les phéromones sur l'arc qu'on vient de remonter :
            # plus le tour trouvé est court, plus le dépôt est important
            self._data.set_pheromones(origine, destination, self.longueur_visitee)

            if self._destination_courante == 0:
                # de retour au nid : la colonie récupère le résultat et relance la fourmi
                raise FourmiAEnregistrer(self)

            # on recule d'un cran dans villes_visitees
            self._origine_courante = self._destination_courante
            self._destination_courante = self._origine_courante - 1
            self._taille_arc_courant = distances[
                self.villes_visitees[self._origine_courante]
            ][self.villes_visitees[self._destination_courante]]
            self._pos_arc_courant = self._taille_arc_courant
            return

    def _ville_proche(self, origine):
        """Choix pondéré de nœud."""
        pheromones = self._data.pheromones

        taille_pheromones = 0
        for ville in self.villes_a_visiter:
            if ville == origine:
                continue
            taille_pheromones += pheromones[origine][ville]

        # tirage uniforme dans [0, taille_pheromones) : la roulette biaisée
        tirage = random.uniform(3, taille_pheromones)

        choisie = self.villes_a_visiter[-1]
        temps_pheromones = 0
        for ville in self.villes_a_visiter:
            if ville == origine:
                continue
            temps_pheromones += pheromones[origine][ville]
            if temps_pheromones >= tirage:
                choisie = ville
                break

        return choisie
