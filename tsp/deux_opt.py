from tsp.distance import distance_km


def optimiser_trajet(villes):
    """Améliore un trajet fermé par 2-opt : inverse un segment tant que
    cela raccourcit le total (décroise le trajet)."""
    villes = list(villes)
    n = len(villes)
    if n < 4:
        return villes

    isOptimized = True
    while isOptimized:
        isOptimized = False

        for i in range(1, n - 1):
            for j in range(i + 1, n - 1):
                a, b = villes[i - 1], villes[i]
                c, d = villes[j], villes[j + 1]

                avant = distance_km(a, b) + distance_km(c, d)
                apres = distance_km(a, c) + distance_km(b, d)
                if apres < avant:
                    villes[i:j + 1] = list(reversed(villes[i:j + 1]))
                    isOptimized = True
                    break

    return villes
