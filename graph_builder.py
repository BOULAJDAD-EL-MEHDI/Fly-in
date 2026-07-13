from connection_parser import ConnectionConfig
from end_hub_parser import EndHubConfig
from hub_parser import HubConfig
from nb_drones_parser import NbDronesConfig
from start_hub_parser import StartHubConfig


class GraphBuilder:

    def __init__(self, configs: list):
        self.configs = configs
        self.graph = {}
        self.start = None
        self.end = None

    def build_graph(self):
        """Build the graph from the parsed configurations."""

        self.graph = {}
        self.start = None
        self.end = None

        for config in self.configs:
            if isinstance(config, StartHubConfig):
                self.start = config.name
                self.add_node(config.name, config)
            elif isinstance(config, EndHubConfig):
                self.end = config.name
                self.add_node(config.name, config)
            elif isinstance(config, HubConfig):
                self.add_node(config.name, config)
            elif isinstance(config, ConnectionConfig):
                self.add_connection(config)

        return self.graph, self.start, self.end

    def add_node(self, name: str, config=None):
        """Add a node to the graph."""

        if name in self.graph:
            return

        self.graph[name] = {
            "config": config,
            "neighbors": []
        }

    def add_connection(self, config):
        """Create a connection between two nodes."""

        start, end = config.connection
        self.add_node(start)
        self.add_node(end)
        self.graph[start]["neighbors"].append(end)
        self.graph[end]["neighbors"].append(start)

    def get_graph(self):
        return self.graph