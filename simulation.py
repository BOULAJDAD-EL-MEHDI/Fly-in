import sys

from connection_parser import ConnectionConfig
from end_hub_parser import EndHubConfig
from graph_builder import GraphBuilder
from graph_solver import GraphSolver
from hub_parser import HubConfig
from nb_drones_parser import NbDronesConfig
from parser_engine import ParserEngine
from start_hub_parser import StartHubConfig


class Simulation:
    """Run a simple turn-by-turn drone simulation."""

    def __init__(self, config_path: str) -> None:
        self.configs = ParserEngine(config_path).config
        self.graph, self.start_node, self.end_node = GraphBuilder(self.configs).build_graph()
        self.zone_info = self._build_zone_info()
        self.connections = self._build_connections()
        self.number_of_drones = self._get_number_of_drones()
        self.drones = self._create_drones()
        self.reserved_connections = {}
        self.turn_number = 0

    def run(self) -> None:
        path = self._build_route()
        if not path:
            return

        for drone in self.drones:
            drone["route"] = list(path)

        while not self._all_drones_finished():
            self.turn_number += 1
            moves = self._play_turn()
            self._apply_moves(moves)
            self._print_turn(moves)

    def _build_zone_info(self) -> dict:
        zone_info = {}
        for config in self.configs:
            if isinstance(config, (StartHubConfig, EndHubConfig, HubConfig)):
                zone_type = getattr(config, "zone", None) or "normal"
                zone_info[config.name] = {
                    "max_drones": config.max_drones,
                    "zone_type": zone_type,
                }
        return zone_info

    def _build_connections(self) -> dict:
        connections = {}
        for config in self.configs:
            if isinstance(config, ConnectionConfig):
                first, second = config.connection
                connections[self._connection_key(first, second)] = config.link_capacity
        return connections

    def _get_number_of_drones(self) -> int:
        for config in self.configs:
            if isinstance(config, NbDronesConfig):
                return config.nb_drones
        return 0

    def _create_drones(self) -> list:
        drones = []
        for index in range(self.number_of_drones):
            drones.append(
                {
                    "id": index + 1,
                    "position": self.start_node,
                    "route": [],
                    "waiting": 0,
                    "target_zone": None,
                    "finished": False,
                }
            )
        return drones

    def _build_route(self) -> list:
        solver = GraphSolver(self.graph)
        result = solver.shortest_path(self.start_node, self.end_node)
        return result["path"] if result["path"] else []

    def _all_drones_finished(self) -> bool:
        for drone in self.drones:
            if not drone["finished"]:
                return False
        return True

    def _play_turn(self) -> list:
        zone_counts = self._count_zone_occupancy()
        connection_usage = dict(self.reserved_connections)
        moves = []

        for drone in self.drones:
            if drone["finished"]:
                continue

            current_zone = drone["position"]
            if drone["waiting"] > 0:
                drone["waiting"] -= 1
                if drone["waiting"] > 0:
                    continue

                target_zone = drone["target_zone"]
                if self._can_move(current_zone, target_zone, zone_counts, connection_usage):
                    moves.append((drone, target_zone))
                    zone_counts[current_zone] -= 1
                    zone_counts[target_zone] += 1
                    connection_key = self._connection_key(current_zone, target_zone)
                    connection_usage[connection_key] = connection_usage.get(connection_key, 0) + 1
                    self.reserved_connections[connection_key] = max(0, self.reserved_connections.get(connection_key, 0) - 1)
                else:
                    drone["waiting"] = 1
                continue

            next_zone = self._next_zone(drone)
            if next_zone is None:
                drone["finished"] = True
                continue

            if self._is_restricted_zone(next_zone):
                connection_key = self._connection_key(current_zone, next_zone)
                if self._can_reserve_connection(connection_key, connection_usage):
                    drone["waiting"] = 1
                    drone["target_zone"] = next_zone
                    self.reserved_connections[connection_key] = self.reserved_connections.get(connection_key, 0) + 1
                    connection_usage[connection_key] = connection_usage.get(connection_key, 0) + 1
                continue

            if self._can_move(current_zone, next_zone, zone_counts, connection_usage):
                moves.append((drone, next_zone))
                zone_counts[current_zone] -= 1
                zone_counts[next_zone] += 1
                connection_key = self._connection_key(current_zone, next_zone)
                connection_usage[connection_key] = connection_usage.get(connection_key, 0) + 1

        return moves

    def _apply_moves(self, moves: list) -> None:
        for drone, next_zone in moves:
            drone["position"] = next_zone
            if drone["route"]:
                drone["route"] = drone["route"][1:]
            if len(drone["route"]) <= 1:
                drone["finished"] = True

    def _print_turn(self, moves: list) -> None:
        if not moves:
            return

        parts = []
        for drone, next_zone in moves:
            parts.append(f"D{drone['id']}-{next_zone}")
        print(" ".join(parts))

    def _count_zone_occupancy(self) -> dict:
        counts = {name: 0 for name in self.zone_info}
        for drone in self.drones:
            if not drone["finished"]:
                counts[drone["position"]] += 1
        return counts

    def _next_zone(self, drone: dict) -> str | None:
        if not drone["route"] or len(drone["route"]) == 1:
            return None
        return drone["route"][1]

    def _is_restricted_zone(self, zone_name: str) -> bool:
        return self.zone_info.get(zone_name, {}).get("zone_type", "normal") == "restricted"

    def _can_reserve_connection(self, connection_key: str, connection_usage: dict) -> bool:
        if connection_key not in self.connections:
            return False
        return connection_usage.get(connection_key, 0) + 1 <= self.connections[connection_key]

    def _can_move(self, current_zone: str, next_zone: str, zone_counts: dict, connection_usage: dict) -> bool:
        if next_zone not in self.graph.get(current_zone, {}).get("neighbors", []):
            return False
        if self.zone_info.get(next_zone, {}).get("zone_type", "normal") == "blocked":
            return False
        if zone_counts.get(next_zone, 0) + 1 > self.zone_info[next_zone]["max_drones"]:
            return False

        connection_key = self._connection_key(current_zone, next_zone)
        if connection_key in self.connections:
            used = connection_usage.get(connection_key, 0) + self.reserved_connections.get(connection_key, 0)
            if used + 1 > self.connections[connection_key]:
                return False

        return True

    def _connection_key(self, first: str, second: str) -> str:
        return f"{first}-{second}"


if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    Simulation(config_file).run()
