import unittest

from src.scraper.graphs.graph import Graph
from src.scraper.graphs.vertices.actor import Actor
from src.scraper.graphs.vertices.movie import Movie

"""
Tests the functionality of the Graph class
"""
class GraphTest(unittest.TestCase):
    # create a graph to test all operations on
    def setUp(self):
        self.movie = Movie("Movie", 100000, 1980, 'https://Testing')
        self.actor = Actor("Actor", 24, 'https://MoreTesting')
        self.graph = Graph()
        self.graph.add_vertex(self.movie)
        self.graph.add_vertex(self.actor)
        for i in range(10):
            self.graph.add_vertex(Actor(str(i), i, 'https://' + str(i)))
        for i in range(10):
            self.graph.add_vertex(Movie(str(i), i, i * 100, 'https://' + str(i)))
        for i in range(10):
            self.graph.add_edge(self.movie, Actor(str(i), i, 'https://' + str(i)), 0)
            self.graph.add_edge(self.actor, Movie(str(i), i, i * 100, 'https://' + str(i)), 0)
            self.graph.add_edge(Actor(str(i), i, 'https://' + str(i)), Movie(str(i), i, i * 100, 'https://' + str(i)), 0)

    def test_add_vertex(self):
        self.assertEqual(True, self.graph.is_vertex(self.movie))
        self.assertEqual(True, self.graph.is_vertex(self.actor))
        self.assertEqual(True, self.graph.is_vertex(Actor(str(4), 4, 'https://' + str(4))))
        self.assertEqual(False, self.graph.is_vertex(Actor("hi", 32, 'https:?')))

    def test_add_edge(self):
        for i in range(10):
            self.assertEqual(True, self.graph.is_edge(self.movie, Actor(str(i), i, 'https://' + str(i))))
            self.assertEqual(True, self.graph.is_edge(self.actor, Movie(str(i), i, i * 100, 'https://' + str(i))))
            self.assertEqual(True, self.graph.is_edge(Actor(str(i), i, 'https://' + str(i)),
                                                      Movie(str(i), i, i * 100, 'https://' + str(i))))
        self.assertEqual(False, self.graph.is_edge(self.movie, self.actor))

    def test_get_all_with(self):
        def f(x):
            return isinstance(x, Actor)
        actors = [Actor(str(i), i, 'https://' + str(i)) for i in range(10)]
        actors.append(self.actor)
        self.assertEqual(set(actors), set(self.graph.get_all_with(f)))

    def test_get_neighbors(self):
        self.assertEqual(set([Movie(str(i), i, i * 100, 'https://' + str(i)) for i in range(10)]),
                         self.graph.get_neighbors(self.actor))
        self.assertEqual(set([Actor(str(i), i, 'https://' + str(i)) for i in range(10)]),
                         self.graph.get_neighbors(self.movie))

    def test_get_weight(self):
        self.assertEqual(0, self.graph.get_weight(self.movie, Actor(str(1), 1, 'https://' + str(1))))

    def test_delete_vertex(self):
        self.graph.delete_vertex(self.movie)
        neighbor = Actor(str(1), 1, 'https://' + str(1))
        self.assertEqual(False, self.graph.is_vertex(self.movie))
        self.assertEqual(False, self.graph.is_edge(neighbor, self.movie))
        self.graph.add_vertex(self.movie)
        for i in range(10):
            self.graph.add_edge(self.movie, Actor(str(i), i, 'https://' + str(i)), 0)



if __name__ == '__main__':
    unittest.main()