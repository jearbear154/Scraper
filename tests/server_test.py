import unittest
import os
from src.scraper.server import app, am_graph
from src.scraper.graphs.vertices.actor import Actor
from src.scraper.graphs.vertices.movie import Movie
import tempfile
import flask.json

# Cite: I got the setUp and tearDown code from the Flask documentation:
# 'http://flask.pocoo.org/docs/0.10/testing/#the-testing-skeleton'
"""
Tests the functionality of the server
"""
class ServerTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

    def test_index(self):
        start = self.app.get('/')
        dct = flask.json.loads(start.data)
        assert "actor1" in dct[0]

    def test_get_actor(self):
        start = self.app.get('/actors/actor1')
        dct = flask.json.loads(start.data)
        assert dct["actor1"]["age"] == 1
        start = self.app.get('/actors/actor7')
        assert start.data == b'No such actor exists'

    def test_get_movie(self):
        start = self.app.get('/movies/movie1')
        dct = flask.json.loads(start.data)
        assert dct["movie1"]["year"] == 1
        start = self.app.get('/movies/movie7')
        assert start.data == b'No such movie exists'

    def test_get_actors(self):
        start = self.app.get('/actors/?name=actor2')
        dct = flask.json.loads(start.data)
        assert dct["actor2"]["age"] == 2
        start = self.app.get('/actors/?name=actor7')
        assert start.data == b'No such actors exist'

    def test_get_movies(self):
        start = self.app.get('/movies/?name=movie2')
        dct = flask.json.loads(start.data)
        assert dct["movie2"]["grossing"] == 2
        start = self.app.get('/movies/?name=movie7')
        assert start.data == b'No such movies exist'

    def test_make_actor(self):
        self.app.post('/actors', data=flask.json.dumps({"name": "actor6", "age": 6, "total_gross": 6}),
                      content_type="application/json")
        assert am_graph.is_vertex(Actor("actor6", 6, 6))

    def test_make_movie(self):
        self.app.post('/movies', data=flask.json.dumps({"name": "movie5", "year": 5}), content_type="application/json")
        assert am_graph.is_vertex(Movie("movie5", None, 5, None))

    def test_update_actor(self):
        self.app.put('/actors/actor2', data=flask.json.dumps({"age": 26}), content_type="application/json")
        assert am_graph.get_actors_with({"name": "actor2"})[0].age == 26
        start = self.app.get('/actors/actor7')
        assert start.data == b'No such actor exists'

    def test_update_movie(self):
        self.app.put('/movies/movie2', data=flask.json.dumps({"year": 1980}), content_type="application/json")
        assert am_graph.get_movies_with({"name": "movie2"})[0].year == 1980
        start = self.app.get('/movies/movie7')
        assert start.data == b'No such movie exists'

    def test_delete_actor(self):
        self.app.delete('/actors/actor4')
        assert am_graph.get_actors_with({"name": "actor4"}) == []
        start = self.app.get('/actors/actor7')
        assert start.data == b'No such actor exists'

    def test_delete_movie(self):
        self.app.delete('/movies/movie3')
        assert am_graph.get_movies_with({"name": "movie3"}) == []
        start = self.app.get('/movies/movie7')
        assert start.data == b'No such movie exists'

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
