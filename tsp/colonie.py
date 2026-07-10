from tsp.ant import Fourmi, FourmiAEnregistrer


class Colonie:
    """Fait tourner un ensemble de fourmis sur un problème jusqu'à convergence."""

    def __init__(self, data, nb_fourmis=10):
        self.data = data
        self.fourmis = [Fourmi(data) for _ in range(nb_fourmis)]

        self.meilleure_longueur = float("inf")
        self.meilleur_chemin = []
        self.tours_boucles = 0

    def notifier_solution(self, longueur, villes_visitees):
        """Une fourmi a bouclé un tour : on retient le meilleur vu jusqu'ici."""
        if longueur < self.meilleure_longueur:
            self.meilleure_longueur = longueur
            self.meilleur_chemin = list(villes_visitees)

    def run(self, n):
        for _ in range(n):
            for indice, fourmi in enumerate(self.fourmis):
                try:
                    fourmi.frame()
                except FourmiAEnregistrer as e:
                    self.notifier_solution(e.fourmi.longueur_visitee, e.fourmi.villes_visitees)

                    if self.meilleure_longueur <= self.data.longueur_optimale:
                        return

                    # la fourmi a fini son tour, on la remplace par une neuve
                    self.fourmis[indice] = Fourmi(self.data)

                    # on évapore tous les 20 tours bouclés, et surtout pas toutes les
                    # 20 frames : un tour dure des centaines de frames, la moindre
                    # trace serait effacée avant d'avoir pu guider qui que ce soit
                    self.tours_boucles += 1
                    if self.tours_boucles % 320 == 0:
                        self.data.evaporate()
