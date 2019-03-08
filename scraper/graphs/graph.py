
"""
A representation of a graph
"""
class Graph:
    """
    Sets up the graph
    """
    def __init__(self):
        self.adjList = dict()

    """
    Adds a vertex to the graph
    :param u: the vertex to add to the graph
    """
    def add_vertex(self, u):
        self.adjList[u] = dict()

    """
    Deletes a vertex from the graph
    :param u: the vertex to be deleted
    """
    def delete_vertex(self, u):
        for v in self.get_neighbors(u):
            del self.adjList[v][u]
        del self.adjList[u]

    """
    Given two vertices, one of them being in the graph, replaces the first one with the second one
    :param u: the vertex in the graph to be replaced
    :param v: the vertex not in the graph that is u's replacement
    """
    def update_vertex(self, u, v):
        self.add_vertex(v)
        for w in self.get_neighbors(u):
            self.add_edge(w, v, self.adjList[w][u])
        self.delete_vertex(u)

    """
    Adds the edge, (u,v), to the graph
    :param u: a vertex
    :param v: a vertex
    """
    def add_edge(self, u, v, w):
        self.adjList[u][v] = w
        self.adjList[v][u] = w

    """
    :param u: a vertex
    :param v: a vertex
    :return: the weight of edge (u,v)
    """
    def get_weight(self, u, v):
        return self.adjList[u][v]

    """
    :param u: a vertex
    :param v: a vertex
    :return: True iff (u,v) is an edge
    """
    def is_edge(self, u, v):
        return v in self.adjList[u].keys()

    """
    :return: True iff u is a vertex
    """
    def is_vertex(self, u):
        return u in self.adjList.keys()

    """
    :param u: a vertex
    :return: a list of the neighbors of u
    """
    def get_neighbors(self, u):
        return self.adjList[u].keys()

    """
    Gets all vertices that satisfy the boolean function prop
    :param prop: a boolean function on the vertices
    :return: a list of all vertices satisfying the property
    """
    def get_all_with(self, prop):
        return [x for x in self.adjList.keys() if prop(x)]
