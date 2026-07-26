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


        if config.zone == "blocked":
            return None


        if config.zone == "restricted":
            if not drone["wait"]:
                drone["wait"] = True
                return None

        if nxt != self.end and zone_count.get(nxt, 0) >= config.max_drones:
            return None

        edge = tuple(sorted((current, nxt)))

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
            elif not all(drone["finished"] for drone in self.drones):
                if any(drone["wait"] for drone in self.drones):
                    continue
                raise RuntimeError("Simulation deadlock: no drone can move")

            if all(drone["finished"] for drone in self.drones):
                break

        return output