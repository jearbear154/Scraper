import unittest
from src.scraper.graphs.actor_movie_graph import ActorMovieGraph
from src.scraper.parser import Parser

"""
Tests the functionality of the Parser class
"""
class ParserTest(unittest.TestCase):
    def setUp(self):
        self.am_graph = ActorMovieGraph()
        self.am_graph.from_json('/Users/jearbear154/Desktop/School/F17*/242/Assignment2.1/src/tests/test.json')
        self.parser = Parser(self.am_graph)
        self.actor1 = self.am_graph.get_actors_with({"name": "actor1"})[0]
        self.movie1 = self.am_graph.get_movies_with({"name": "movie1"})[0]

    def test_parse_actor(self):
        self.assertEqual({}, self.parser.parse_actor("actor6", {}))
        self.parser.parse_actor(self.actor1.name, {"total_gross": 7, "movies": ["movie2"]})
        self.assertEqual(7, self.am_graph.get_actors_with({"name": "actor1"})[0].total_gross)

    def test_parse_movie(self):
        self.assertEqual({}, self.parser.parse_movie("movie6",{}))
        self.parser.parse_movie(self.movie1.name, {"year": 85, "actors": ["actor2"]})
        assert self.am_graph.is_edge(self.am_graph.get_movies_with({"name": "movie1"})[0],
                                     self.am_graph.get_actors_with({"name": "actor2"})[0])
        self.assertEqual(85, self.am_graph.get_movies_with({"name": "movie1"})[0].year)

    def test_parse_actors(self):
        self.assertEqual({"actor3", "actor5"}, set(self.parser.parse_actors({"name": "actor3|name=actor5"}).keys()))
        self.assertEqual({"actor3", "actor4"}, set(self.parser.parse_actors({"name": "actor3|age=4"}).keys()))
        self.assertEqual({}, self.parser.parse_actors({"name": "actor1", "age": "16"}))

    def test_parse_movies(self):
        self.assertEqual({"movie3", "movie4"}, set(self.parser.parse_movies({"name": "movie3|name=movie4"}).keys()))
        self.assertEqual({"movie3", "movie4"}, set(self.parser.parse_movies({"name": "movie3|grossing=4"}).keys()))
        self.assertEqual({}, self.parser.parse_movies({"name": "movie1", "year": "16"}))


if __name__ == '__main__':
    unittest.main()
