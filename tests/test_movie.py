import unittest
from src.scraper.graphs.vertices.movie import Movie

"""
Tests the functionality of the Movie vertex
"""
class MovieTest(unittest.TestCase):
    def setUp(self):
        self.movie1 = Movie("Test1", 240, 1980, 'http://test1')
        self.movie2 = Movie("Test2", 320, 1872, 'http://test2')

    def test_init(self):
        self.assertEqual("Test1", self.movie1.name)
        self.assertEqual(240, self.movie1.grossing)
        self.assertEqual(1980, self.movie1.year)
        self.assertEqual('http://test1', self.movie1.url)

    def test_eq(self):
        self.assertEqual(Movie("", 21, 0, 'http://test1'), self.movie1)
        self.assertNotEqual(self.movie1, self.movie2)

    def test_to_dict(self):
        self.assertEqual({"json_class": "Movie", "name": "Test1", "year": 1980, "grossing": 240,
                            "url": 'http://test1'}, self.movie1.to_dict())

    def test_from_dict(self):
        movie = Movie("hi", 5, 8, "hi")
        movie = movie.from_dict({"url": 'http://test1'})
        self.assertEqual(self.movie1, movie)


if __name__ == '__main__':
    unittest.main()
