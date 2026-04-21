class Graph:
    def __init__(self, directed: bool) -> None:
        self.directed = directed
        self.adj_list = dict()

    def __repr__(self) -> str:
        graph_str = ""
        for node, neighbors in self.adj_list.items():
            graph_str += f"{node} -> {neighbors}\n"
        return graph_str
    
    def add_node(self, node) -> None:
        if node not in self.adj_list:
            self.adj_list[node] = set()
        else:
            raise ValueError("Node is alrady exist !")
        
    def remove_node(self, node) -> None:
        if node not in self.adj_list:
            raise ValueError ("Node does not exist !")
        for naighbors in self.adj_list:
            naighbors.discard(node)
        del self.adj_list[node]

    def add_edge(self, from_node, to_node, Weghit) -> None:
        if from_node not in self.adj_list:
            self.add_node(from_node)
        if to_node not in self.adj_list:
            self.add_node(to_node)
        if Weghit is None:
            if self.directed:
                self.adj_list.ne