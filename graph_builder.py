


class GraphBuilder:
    def __init__(self, config: list):
        self.config = config
        self.graph = {}

    def build_graph(self, config: list):
        for line in config:
            if line[0].startswith("hub"):
                self.add_node()

        for line in config:
            if line[0].startswith("connection"):
                self.add_connection()
            

    def add_node(self, node: str):
        if node[1] not in self.graph:
            self.graph[node[1]] = {
                "data": node[1:],
                "neighbors": []
            }

    def add_connection():
        pass

    def get_graph():
        pass

