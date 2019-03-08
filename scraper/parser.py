from src.scraper.graphs.vertices.movie import Movie

"""
Parser --- class that parses data given by the server and updates the graph, then returns a dict for the HTTP response
"""
class Parser:
    """
    Sets up the parser to work with the specified ActorMovieGraph
    :param am_graph: an ActorMovieGraph
    """
    def __init__(self, am_graph):
        self.am_graph = am_graph

    """
    Updates the actor with name, actor_name, in the graph with the specified attribute, value pairs
    :param actor_name: the name of the actor to be updated
    :param attributes: a dict that specifies which attributes of the actor should be changed and what into
    :return: A dict with the updated actor that is easily jsonified in the server
    """
    def parse_actor(self, actor_name, attributes):
        actors = self.am_graph.get_actors_with({"name": actor_name})
        if actors != []:
            if attributes.get('movies'):
                for movie_name in attributes['movies']:
                    movie = self.am_graph.get_movies_with({"name": movie_name})[0]
                    self.am_graph.add_edge(actors[0], movie, 0)
            updated_actor = actors[0].from_dict(attributes)
            self.am_graph.update_vertex(actors[0], updated_actor)
            return self.get_adjacent_names(updated_actor)
        else:
            return {}

    """
    Updates the movie with name, movie_name, in the graph with the specified attribute, value pairs
    :param movie_name: the name of the movie to be updated
    :param attributes: a dict that specifies which attributes of the movie should be changed and what into
    :return: A dict with the updated movie that is easily jsonified in the server
    """
    def parse_movie(self, movie_name, attributes):
        movies = self.am_graph.get_movies_with({"name": movie_name})
        if movies != []:
            if attributes.get('actors'):
                for actor_name in attributes['actors']:
                    actor = self.am_graph.get_actors_with({"name": actor_name})[0]
                    self.am_graph.add_edge(movies[0], actor, 0)
            updated_movie = movies[0].from_dict(attributes)
            self.am_graph.update_vertex(movies[0], updated_movie)
            return self.get_adjacent_names(updated_movie)
        else:
            return {}

    # I assume for simplicity that and has higher precedence then or
    """
    :param attributes: a multidict that has an entry for the desired attributes that must be anded together, and the
        attributes to be ored together will be in the value string associated to a key. i.e. is the multidict given by
        request.args.to_dict()
    :return: A dict with all the actors satisfying the desired attributes boolean expression
    """
    def parse_actors(self, attributes):
        acceptable = set(self.am_graph.get_actors_with({}))
        for attribute, value in attributes.items():
            or_values = value.split('|')
            or_values[0] = attribute + '=' + or_values[0]  # pair the first arg back with its value
            movies_found = set()
            for assignment in or_values:
                attr = assignment.split('=')
                movies_found = movies_found | set(self.am_graph.get_actors_with({attr[0]: attr[1]}))
            acceptable = acceptable & movies_found
        return {movie.name: movie.to_dict() for movie in acceptable}

    # I assume for simplicity that and has higher precedence then or
    """
    :param attributes: a multidict that has an entry for the desired attributes that must be anded together, and the
        attributes to be ored together will be in the value string associated to a key. i.e. is the multidict given by
        request.args.to_dict()
    :return: A dict with all the movies satisfying the desired attributes boolean expression
    """
    def parse_movies(self, attributes):
        acceptable = set(self.am_graph.get_movies_with({}))
        for attribute, value in attributes.items():
            or_values = value.split('|')
            or_values[0] = attribute + '=' + or_values[0]  # pair the first arg back with its value
            actors_found = set()
            for assignment in or_values:
                attr = assignment.split('=')
                actors_found = actors_found | set(self.am_graph.get_movies_with({attr[0]: attr[1]}))
            acceptable = acceptable & actors_found
        return {actor.name: actor.to_dict() for actor in acceptable}

    """
    :return: a dict with all the actors in the graph
    """
    def actors_to_dict(self):
        return {actor.name: actor.to_dict() for actor in self.am_graph.get_actors_with({})}

    """
    :return: a dict with all the movies in the graph
    """
    def movies_to_dict(self):
        return {movie.name: movie.to_dict() for movie in self.am_graph.get_movies_with({})}

    """
    :param vertex: an Actor or Movie vertex in the graph
    :return: a dict that has the info of the vertex and the list of all its neighbors included
    """
    def get_adjacent_names(self, vertex):
        neighbor_names = [neighbor.name for neighbor in self.am_graph.get_neighbors(vertex)]
        vertex_dict = vertex.to_dict()
        vertex_dict['actors' if isinstance(vertex, Movie) else 'movies'] = neighbor_names
        return {vertex.name: vertex_dict}
