class GraphBuilder:

    def __init__(self, configs: list):
        self.configs = configs
        self.graph = {}

    def build_graph(self):
        """Build the graph from the parsed configurations."""

        self._create_nodes()
        self._create_connections()

        return self.graph

    def _create_nodes(self):
        """Create every hub in the graph."""

        for config in self.configs:
            if config[0].startswith("hub"):
                self.add_node(config)

    def _create_connections(self):
        """Connect the hubs together."""

        for config in self.configs:
            if config[0].startswith("connection"):
                self.add_connection(config)

    def add_node(self, config):
        """Add a node to the graph."""

        position = config[1]

        if position in self.graph:
            return

        self.graph[position] = {
            "config": config,
            "neighbors": []
        }

    def add_connection(self, config):
        """Create a connection between two nodes."""

        start = config[1]
        end = config[2]

        self.graph[start]["neighbors"].append(end)
        self.graph[end]["neighbors"].append(start)

    def get_graph(self):
        return self.graph