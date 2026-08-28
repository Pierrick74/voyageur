from tsp.distance import summary_distance_km


def trajet_glouton(ville, depart=""):
    """Construit un circuit fermé par insertion gloutonne : chaque ville est
    insérée à la position du circuit qui minimise la distance totale."""
    try:
        depart_index = ville.noms.index(depart) if depart else 0
    except ValueError:
        raise ValueError(f"Départ '{depart}' non trouvé parmi les destinations")

    restantes = ville.rebuild_points(range(len(ville.noms)))

    if len(restantes) <= 3:
        return restantes + [restantes[0]]

    circuit = [restantes.pop(depart_index)] * 2

    while restantes:
        _inserer_au_meilleur_endroit(circuit, restantes.pop(0))

    return circuit


def _inserer_au_meilleur_endroit(circuit, city):
    """Insère city à la position du circuit qui minimise la distance totale."""
    distances = {}

    for i in range(1, len(circuit)):
        temp_circuit = circuit[:i] + [city] + circuit[i:]
        distances[i] = summary_distance_km(temp_circuit)

    best_position = min(distances, key=distances.get)
    circuit.insert(best_position, city)
