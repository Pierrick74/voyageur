from carte.distance import summary_distance_km 

class glouton:
    def __init__(self, villes):
            self.villes = villes
            self.remaining_cities = villes.rebuild_points(range(len(villes.noms)))
            self.circuit = []


    def trajet_glouton(self, depart=""):

        try:
            depart_index = self.villes.noms.index(depart) if depart else 0
        except ValueError:
            raise ValueError(f"Départ '{depart}' non trouvé parmi les destinations")

        if len(self.remaining_cities) <= 3:
            self.circuit = self.remaining_cities
            self.circuit.append(self.circuit[0])
            return self.circuit
        
        depart = self.remaining_cities.pop(depart_index)
        self.circuit = [depart, depart]

        while self.remaining_cities:
            city = self.remaining_cities[0]
            self.add_city_in_opt_circuit(city)

        return self.circuit


    def add_city_in_opt_circuit(self, city):
        distances = {}

        for i in range(1, len(self.circuit)):
            temp_circuit = self.circuit[:i] + [city] + self.circuit[i:]
            distances[i] = summary_distance_km(temp_circuit)

        best_position = min(distances, key=distances.get)
        self.circuit.insert(best_position, city)
        self.remaining_cities.remove(city)


    def add_city_in_circuit(self, city):
        self.circuit.append(city)
        self.remaining_cities.remove(city)
        