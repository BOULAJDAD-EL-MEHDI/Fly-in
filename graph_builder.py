from connection_parser import ConnectionConfig
from end_hub_parser import EndHubConfig
from hub_parser import HubConfig
from start_hub_parser import StartHubConfig


class GraphBuilder:
    def __init__(self, configs: list):
        self.configs = configs
        self.graph : dict = {}
        self.start = None
        self.end = None

    def build_graph(self):
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

    def add_node(self, name, config=None):
        if name not in self.graph:
            self.graph[name] = {
                "config": config,
                "neighbors": []
            }

    def add_connection(self, config):
        node1, node2 = config.connection

        self.add_node(node1)
        self.add_node(node2)

        self.graph[node1]["neighbors"].append(node2)
        self.graph[node2]["neighbors"].append(node1)