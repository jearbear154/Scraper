import json

from src.scraper.graphs.graph import Graph
from src.scraper.graphs.vertices.actor import Actor
from src.scraper.graphs.vertices.movie import Movie

"""
A graph holding the actors and vertices with all the desired analysis functionality
"""
class ActorMovieGraph(Graph):
    """
    :param n: the number of hub actors desired
    :return: a sorted list containing the n actors with the most connections
    """
    def hub_actors(self, n):
        return sorted(self.get_actors_with({}), key=lambda actor: self.connections(actor))[(-1)*n:]

    """
    :param actor: an actor vertex
    :return: the number of connections of the actor
    """
    def connections(self, actor):
        neighbors = set()
        for movie in self.get_neighbors(actor):
            neighbors = neighbors | self.get_neighbors(movie)
        return len(neighbors)-1  # don't include the actor itself

    """
    :return: the age for which actors of this age have in total the most grossing income
    """
    def top_grossing_age(self):
        ages = self.age_to_grossing()
        return [x for x in ages.keys() if ages[x] == sorted(ages.values())[-1]][0]

    """
    :return: a dict mapping ages to the sum of total_gross of each actor with that age
    """
    def age_to_grossing(self):
        ages = dict()
        for actor in self.get_actors_with({}):
            if actor.age not in ages.keys():
                ages[actor.age] = 0
            ages[actor.age] += actor.total_gross
        return ages

    """
    :param attr: a dict that specifies attribute, value pairs that the actor must satisfy
    :return: A list of the actors with the desired attributes
    """
    def get_actors_with(self, attr):
        def has_attributes(actor):
            if not isinstance(actor, Actor):
                return False
            satisfies = (not attr.get('name') or actor.name == attr['name'])
            satisfies = satisfies and (not attr.get('age') or actor.age == int(attr['age']))
            satisfies = satisfies and (not attr.get('total_gross') or actor.total_gross == int(attr['total_gross']))
            return satisfies
        return self.get_all_with(has_attributes)

    """
    :param attr: a dict that specifies attribute, value pairs that the movie must satisfy
    :return: A list of the movies with the desired attributes
    """
    def get_movies_with(self, attr):
        def has_attributes(movie):
            if not isinstance(movie, Movie):
                return False
            satisfies = (not attr.get('name') or movie.name == attr['name'])
            satisfies = satisfies and (not attr.get('grossing') or movie.grossing == int(attr['grossing']))
            satisfies = satisfies and (not attr.get('year') or movie.year == int(attr['year']))
            satisfies = satisfies and (not attr.get('url') or movie.url == attr['url'])
            return satisfies
        return self.get_all_with(has_attributes)

    """
    Constructs the current graph from the json file specified
    :param file: a string specifying the file path
    """
    def from_json(self, file):
        f = open(file, 'r')
        movie_actor_list = json.load(f)
        f.close()

        for actor in movie_actor_list[0].values():
            self.add_vertex(Actor(actor["name"], actor["age"], actor["total_gross"]))

        for movie in movie_actor_list[1].values():
            self.add_vertex(Movie(movie["name"], movie["box_office"], movie["year"], movie["wiki_page"]))

        for actor in movie_actor_list[0].values():  # make actor->movie edges
            for movie in actor["movies"]:
                u = self.get_actors_with({"name": actor['name']})
                v = self.get_movies_with({"name": movie})
                if u != [] and v != []:
                    self.add_edge(u[0], v[0], 0)

        for movie in movie_actor_list[1].values():  # make movie->actor edges
            for actor in movie["actors"]:
                u = self.get_movies_with({"name": movie['name']})
                v = self.get_actors_with({"name": actor})
                if u != [] and v != []:
                    self.add_edge(u[0], v[0], 0)

