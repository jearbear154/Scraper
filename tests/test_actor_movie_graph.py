import unittest
from src.scraper.graphs.actor_movie_graph import ActorMovieGraph
from src.scraper.graphs.vertices.actor import Actor
from src.scraper.graphs.vertices.movie import Movie

"""
Tests the functionality of the ActorMovieGraph class
"""
class ActorMovieGraphTest(unittest.TestCase):
    # create a graph to test all operations on
    def setUp(self):
        self.graph = ActorMovieGraph()
        self.graph.from_json('/Users/jearbear154/Desktop/School/F17*/242/Assignment2.1/src/tests/test.json')
        self.actor1 = Actor("actor1", 1, 1)
        self.movie1 = Movie("movie1", 1, 1, "http://movie1")

    def test_get_grossing(self):
        self.assertEqual(3, self.graph.get_movies_with({"name": "movie3", "year": 3})[0].grossing)

    def test_from_json(self):
        self.assertEqual(5, len(self.graph.get_actors_with({})))
        self.assertEqual(4, len(self.graph.get_movies_with({})))
        for i in range(1,5):
            assert self.graph.is_vertex(Actor("actor" + str(i), i, i))
            assert self.graph.is_vertex(Movie("movie" + str(i), i, i, "http://movie" + str(i)))
        assert self.graph.is_edge(self.actor1, self.movie1)
        assert not self.graph.is_edge(Actor("actor3", 3, 3), Movie("movie4", 4, 4, "http://movie4"))

    def test_connections(self):
        self.assertEqual(3, self.graph.connections(self.graph.get_actors_with({"name": "actor1"})[0]))

    def test_hub_actors(self):
        self.assertEqual(self.actor1, self.graph.hub_actors(1)[0])

    def test_top_grossing_age(self):
        self.assertEqual(3, self.graph.top_grossing_age())

    def test_age_to_grossing(self):
        self.assertEqual({1: 1, 2: 2, 3: 1003, 4: 4}, self.graph.age_to_grossing())

    def test_get_actors_with(self):
        self.assertEqual("actor2", self.graph.get_actors_with({"total_gross": 2})[0].name)
        self.assertEqual("actor2", self.graph.get_actors_with({"age": 2})[0].name)
        self.assertEqual("actor2", self.graph.get_actors_with({"name": "actor2"})[0].name)
        self.assertNotEqual("actor2", self.graph.get_actors_with({"total_gross": 3})[0].name)

    def test_get_movies_with(self):
        self.assertEqual("movie3", self.graph.get_movies_with({"grossing": 3})[0].name)
        self.assertEqual("movie3", self.graph.get_movies_with({"year": 3})[0].name)
        self.assertEqual("movie3", self.graph.get_movies_with({"url": "http://movie3"})[0].name)
        self.assertEqual("movie3", self.graph.get_movies_with({"name": "movie3"})[0].name)
        self.assertNotEqual("movie3", self.graph.get_movies_with({"year": 4})[0].name)


if __name__ == '__main__':
    unittest.main()
