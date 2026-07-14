from colors import color_text


class SimulationEngine:
    def __init__(self, graph, nb_drones, start, end, paths):
        self.graph = graph
        self.nb_drones = nb_drones
        self.start = start
        self.end = end

        self.drones = []
        for i in range(nb_drones):
            self.drones.append({
                "id": i + 1,
                "path": paths[i],
                "index": 0,
                "wait": False,
                "finished": False,
            })

    def move_drone(self, drone, zone_count, connection_count):
        if drone["finished"]:
            return None

        path = drone["path"]

        if drone["index"] == len(path) - 1:
            drone["finished"] = True
            return None

        current = path[drone["index"]]
        nxt = path[drone["index"] + 1]

        config = self.graph[nxt]["config"]

        # Blocked zone
        if config.zone == "blocked":
            return None

        # Restricted zone -> wait one turn
        if config.zone == "restricted" and not drone["wait"]:
            drone["wait"] = True
            return None

        drone["wait"] = False

        # Zone capacity
        if zone_count.get(nxt, 0) >= config.max_drones:
            return None

        edge = tuple(sorted((current, nxt)))

        # Connection capacity
        if connection_count.get(edge, 0) >= 1:
            return None

        zone_count[current] -= 1
        zone_count[nxt] = zone_count.get(nxt, 0) + 1
        connection_count[edge] = connection_count.get(edge, 0) + 1

        drone["index"] += 1

        if nxt == self.end:
            drone["finished"] = True

        config = self.graph[nxt]["config"]
        return f"D{drone['id']}-{color_text(nxt, config.color)}"

    def simulate(self):
        output = []

        zone_count = {self.start: self.nb_drones}

        while True:
            moves = []
            connection_count = {}

            for drone in self.drones:
                move = self.move_drone(drone, zone_count, connection_count)

                if move:
                    moves.append(move)

            if moves:
                output.append(" ".join(moves))

            if all(drone["finished"] for drone in self.drones):
                break

        return output