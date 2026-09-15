from connection_parser import ConnectionConfig
from end_hub_parser import EndHubConfig
from hub_parser import HubConfig
from start_hub_parser import StartHubConfig


class GraphBuilder:
    """Build an adjacency graph from parsed configuration objects."""

    def __init__(self, configs: list):
        """Initialize the builder with parsed configuration entries.

        Args:
            configs: Parsed configuration objects to convert into a graph.
        """
        self.configs = configs
        self.graph : dict = {}
        self.start = None
        self.end = None

    def build_graph(self):
        """Create the graph representation from all configuration objects.

        Returns:
            A tuple containing the graph, the start node, and the end node.
        """
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
        """Add a node to the graph if it does not already exist.

        Args:
            name: Name of the hub to add.
            config: Optional configuration object associated with the node.
        """
        if name not in self.graph:
            self.graph[name] = {
                "config": config,
                "neighbors": [],
                "link_capacity": {}
            }

    def add_connection(self, config):
        """Connect two nodes in the graph using a connection configuration.

        Args:
            config: Connection configuration describing the link between two nodes.
        """
        node1, node2 = config.connection

        self.add_node(node1)
        self.add_node(node2)

        self.graph[node1]["neighbors"].append(node2)
        self.graph[node2]["neighbors"].append(node1)
        self.graph[node1]["link_capacity"][node2] = config.link_capacity
        self.graph[node2]["link_capacity"][node1] = config.link_capacity