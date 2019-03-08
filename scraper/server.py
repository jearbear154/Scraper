from flask import Flask, jsonify, request, make_response

from src.scraper.graphs.actor_movie_graph import ActorMovieGraph
from src.scraper.graphs.vertices.actor import Actor
from src.scraper.graphs.vertices.movie import Movie
from src.scraper.parser import Parser

app = Flask(__name__)
am_graph = ActorMovieGraph()
# use file: test.json for unit testing otherwise data.json
am_graph.from_json('/Users/jearbear154/Desktop/School/F17*/242/Assignment2.1/src/tests/test.json')
parser = Parser(am_graph)
print(am_graph.connections(am_graph.hub_actors(1)[0]))

# ----------------------------------------------------GET--------------------------------------------------------------
"""
Starts the server in the home directory with a list of all movies and actors
"""
@app.route('/', methods=['GET'])
def index():
    return jsonify([parser.actors_to_dict(), parser.movies_to_dict()])

"""
:return: a jsonified dict of all the actors that satisfy the attributes boolean expression
"""
@app.route('/actors/', methods=['GET'])
def get_actors():
    actors = parser.parse_actors(request.args.to_dict())
    if actors == {}:
        return make_response('No such actors exist', 400)
    return jsonify(actors)

"""
:return: a jsonified dict of all the movies that satisfy the attributes boolean expression
"""
@app.route('/movies/', methods=['GET'])
def get_movies():
    movies = parser.parse_movies(request.args.to_dict())
    if movies == {}:
        return make_response('No such movies exist', 400)
    return jsonify(movies)

"""
:param actor_name: the name of the actor
:return: a jsonified dict with the attributes of the actor including all the movies it is in
"""
@app.route('/actors/<actor_name>', methods=['GET'])
def get_actor(actor_name):
    actors = am_graph.get_actors_with({"name": actor_name})
    if actors == []:
        return make_response('No such actor exists', 400)
    return jsonify(parser.get_adjacent_names(actors[0]))

"""
:param movie_name: the name of the movie
:return: a jsonified dict with the attributes of the movie including all the actors in it
"""
@app.route('/movies/<movie_name>', methods=['GET'])
def get_movie(movie_name):
    movies = am_graph.get_movies_with({"name": movie_name})
    if movies == []:
        return make_response('No such movie exists', 400)
    return jsonify(parser.get_adjacent_names(movies[0]))

# ----------------------------------------------------PUT--------------------------------------------------------------
"""
Updates the actor in the graph specified by name, actor_name, with the attributes and values specified in the 
request.json dict
:param actor_name: the name of the actor to be updated
:return: a jsonified dict containing the metadata of the updated actor
"""
@app.route('/actors/<actor_name>', methods=['PUT'])
def update_actor(actor_name):
    actor = parser.parse_actor(actor_name, request.json)
    if actor == {}:
        return make_response('No such actor exists', 400)
    return jsonify(actor)

"""
Updates the movie in the graph specified by name, movie_name, with the attributes and values specified in the 
request.json dict
:param movie_name: the name of the movie to be updated
:return: a jsonified dict containing the metadata of the updated movie
"""
@app.route('/movies/<movie_name>', methods=['PUT'])
def update_movie(movie_name):
    movie = parser.parse_movie(movie_name, request.json)
    if movie == {}:
        return make_response('No such movie exists', 400)
    return jsonify(movie)

# ----------------------------------------------------POST--------------------------------------------------------------
"""
Creates a new actor vertex with the attribute, values specified in the dict, request.json
:return: a jsonified dict containing the metadata of the new actor
"""
@app.route('/actors', methods=['POST'])
def make_actor():
    actor = Actor(request.json.get('name'), request.json.get('age'), request.json.get('total_gross'))
    am_graph.add_vertex(actor)
    return make_response(jsonify(parser.actors_to_dict()), 201)

"""
Creates a new movie vertex with the attribute, values specified in the dict, request.json
:return: a jsonified dict containing the metadata of the new movie
"""
@app.route('/movies', methods=['POST'])
def make_movie():
    movie = Movie(request.json.get('name'), request.json.get('grossing'),
                  request.json.get('year'), request.json.get('url'))
    am_graph.add_vertex(movie)
    return make_response(jsonify(parser.movies_to_dict()), 201)

# ---------------------------------------------------DELETE-------------------------------------------------------------
"""
:param actor_name: the name of the actor to be deleted from the graph
:return: a jsonified dict containing the metadata of the next actor with same name if there is one
"""
@app.route('/actors/<actor_name>', methods=['DELETE'])
def delete_actor(actor_name):
    actors = am_graph.get_actors_with({"name": actor_name})
    if actors == []:
        return make_response('No such actor exists', 400)
    am_graph.delete_vertex(actors[0])
    actors.__delitem__(0)
    return jsonify({actors[0].name: actors[0].to_dict()} if actors != [] else {})

"""
:param movie_name: the name of the movie to be deleted from the graph
:return: a jsonified dict containing the metadata of the next movie with same name if there is one
"""
@app.route('/movies/<movie_name>', methods=['DELETE'])
def delete_movie(movie_name):
    movies = am_graph.get_movies_with({"name": movie_name})
    if movies== []:
        return make_response('No such movie exists', 400)
    am_graph.delete_vertex(movies[0])
    movies.__delitem__(0)
    return jsonify({movies[0].name: movies[0].to_dict()} if movies != [] else {})


if __name__ == '__main__':
    app.run(debug=True)