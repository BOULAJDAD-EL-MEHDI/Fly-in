from colors import color_text


class SimulationEngine:
    """Simulate drone movement across the graph according to hub rules."""

    def __init__(self, graph, nb_drones, start, end, paths):
        """Initialize the simulation with the graph and drone routes.

        Args:
            graph: Graph containing hub configuration and neighbors.
            nb_drones: Number of drones to simulate.
            start: Starting hub name.
            end: Destination hub name.
            paths: Planned paths for each drone.
        """
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
        """Attempt to move a single drone to its next zone.

        Args:
            drone: Dictionary describing the drone state.
            zone_count: Count of drones currently occupying each zone.
            connection_count: Count of drones already using each connection.

        Returns:
            A formatted move string if the drone advances, otherwise None.
        """
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

        if (connection_count.get(edge, 0)
                >= self.graph[current]["link_capacity"][nxt]):
            return None

        zone_count[current] -= 1
        zone_count[nxt] = zone_count.get(nxt, 0) + 1
        connection_count[edge] = connection_count.get(edge, 0) + 1

        drone["index"] += 1
        drone["wait"] = False

        if nxt == self.end:
            drone["finished"] = True

        config = self.graph[nxt]["config"]
        return f"D{drone['id']}-{color_text(nxt, config.color)}"

    def simulate(self):
        """Run the full drone simulation until all drones have finished.

        Returns:
            A list of turn-by-turn move strings.
        """
        output = []

        zone_count = {self.start: self.nb_drones}

        while True:
            moves = []
            connection_count = {}
            waiting = False

            for drone in self.drones:
                was_waiting = drone["wait"]
                move = self.move_drone(drone, zone_count, connection_count)
                if not was_waiting and drone["wait"]:
                    waiting = True

                if move:
                    moves.append(move)

            if moves:
                output.append(" ".join(moves))
            elif not all(drone["finished"] for drone in self.drones):
                if waiting:
                    output.append("")
                    continue
                raise RuntimeError("Simulation deadlock: no drone can move")

            if all(drone["finished"] for drone in self.drones):
                break

        return output