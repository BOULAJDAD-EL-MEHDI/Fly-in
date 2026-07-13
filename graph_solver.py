from collections import deque


class GraphSolver:

    def __init__(self, graph):
        self.graph = graph

    def shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            return {"path": [], "distance": None}

        queue = deque([start])
        previous = {start: None}

        while queue:
            current = queue.popleft()
            if current == end:
                break

            for neighbor in self.graph[current]["neighbors"]:
                if neighbor in previous:
                    continue
                previous[neighbor] = current
                queue.append(neighbor)

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous.get(current)

        path.reverse()
        if path and path[0] == start:
            return {"path": path, "distance": len(path) - 1}

        return {"path": [], "distance": None}
