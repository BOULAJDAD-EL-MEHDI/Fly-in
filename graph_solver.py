from heapq import heappop, heappush


class GraphSolver:

    def __init__(self, graph):
        self.graph = graph

    def shortest_path(self, start, end):
        queue = [(0, start)]
        distances = {node: float("inf") for node in self.graph}
        previous = {node: None for node in self.graph}

        distances[start] = 0

        while queue:
            current_distance, current = heappop(queue)

            if current == end:
                break

            if current_distance > distances[current]:
                continue

            for neighbor in self.graph[current]["neighbors"]:

                if self._is_restricted(neighbor):
                    continue

                weight = self._edge_cost(current, neighbor)

                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    heappush(queue, (new_distance, neighbor))

        return self._build_path(previous, start, end)

    def _build_path(self, previous, start, end):
        path = []

        current = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        if path and path[0] == start:
            return path

        return []

    def _edge_cost(self, node1, node2):
        return 1

    def _is_restricted(self, node):
        return False