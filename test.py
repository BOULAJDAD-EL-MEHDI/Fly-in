class Graph:
#-----------init-------------#
    def __init__(self, directed = False):
        self.directed = directed
        self.adj_list = dict()

#-----------repr-------------#
    def __repr__(self):
        gragh_str = ""
        for node, neighbors in self.adj_list:
            gragh_str += f"{node} -> {neighbors}\n"
        return gragh_str

#-----------add node-------------#
    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = set()
        else:
            raise ValueError ("Node exists already !")

#-----------remove node-------------#
    def remove_node(self, node):
        if node not in self.adj_list:
            raise ValueError ("Node does not exist !")
        for neighbors in self.adj_list.values():
            neighbors.discard(node)
        del self.adj_list[node]

#-----------add edge-------------#
    def add_edge(self, from_node, to_node, weight):
        if from_node not in self.adj_list:
            self.add_node(from_node)
        if to_node not in self.adj_list:
            self.add_node(to_node)
        if weight is None:
            self.adj_list[from_node].add(to_node)
            if not self.directed:
                self.adj_list[to_node].add(from_node)
        else:
            self.adj_list[from_node].add(from_node, weight)
            if not self.directed:
                self.adj_list[to_node].add(from_node, weight)

#-----------remove-------------#
    def remove(self, from_node, to_node):
        if from_node in self.adj_list:
            if self.adj_list[from_node]:
                self.adj_list[from_node].remove(to_node)
            else:
                raise ValueError ("Edge does not exist !")
            if not self.directed:
                if from_node in self.adj_list[to_node]:
                    self.adj_list[to_node].remove(from_node)
        else:
            raise ValueError ("Edge does not exists")

#-----------get nighbors-------------#
    def get_nighbors(self, node):
        return self.adj_list.get(node, set())

#-----------has node-------------#
    def has_node(self, node):
        return node in self.adj_list

#-----------has edge-------------#
    def has_edge(self, from_node, to_node):
        if from_node in self.adj_list:
            return to_node in self.adj_list[from_node]
        return False

#-----------get nodes-------------#
    def get_nodos(self):
        return list(self.adj_list.keys())

#-----------get edges-------------#
    def get_edges(self):
        edges = []
        for from_node, neighbors in self.adj_list.items():
            for to_node in neighbors:
                edges.append(from_node, to_node)
            
#-----------BFS-------------#
    def bfs(self, start):
        pass

#-----------DFS-------------#
    def dfs(self, start):
        pass