class GraphSolver:
    def __init__(self, graph):
        self.graph = graph

    def shortest_path(self, start, end):
        distances = {}
        previous = {}
        visited = set()

        for node in self.graph:
            distances[node] = float("inf")

        distances[start] = 0

        while True:
            current = None

            for node in self.graph:
                if node in visited:
                    continue

                if current is None or distances[node] < distances[current]:
                    current = node

            if current is None or distances[current] == float("inf"):
                break

            if current == end:
                break

            visited.add(current)

            for neighbor in self.graph[current]["neighbors"]:
                config = self.graph[neighbor]["config"]

                if config.zone == "blocked":
                    continue

                cost = 1

                if config.zone == "restricted":
                    cost = 2
                elif config.zone == "priority":
                    cost = 0.9

                new_distance = distances[current] + cost

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current

        if end not in previous and start != end:
            return []

        path = [end]

        while path[-1] != start:
            path.append(previous[path[-1]])

        path.reverse()
        return path