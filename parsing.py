class Vertice:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

def add_edge(connection):
    name1, name2 = connection.split('-')
    obj1 = Vertice(name1)
    obj2 = Vertice(name2)
    obj1.neighbors.append(obj2)
    obj2.neighbors.append(obj1)

    for n in obj1.neighbors:
        print(n.name)
    for n in obj2.neighbors:
        print(n.name)
    


connection = 'start-juntion'
add_edge(connection)
