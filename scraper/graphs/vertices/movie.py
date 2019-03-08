
"""
Represents a movie vertex. Contains the name, gross income, year, and url belonging to the movie
"""
class Movie():
    def __init__(self, name, grossing, year, url):
        self.name = name
        self.grossing = grossing
        self.year = year
        self.url = url

    """
    :return: a dict representation of the movie
    """
    def to_dict(self):
        return {"json_class": "Movie", "name": self.name, "year": self.year, "grossing": self.grossing,
                            "url": self.url}

    """
    :param dct: a dct that specifies attributes of the movie to be overwritten
    :return: a new movie with the same member values as the current movie except those specified to be changed by dct
    """
    def from_dict(self, dct):
        name = dct['name'] if dct.get('name') else self.name
        year = int(dct['year']) if dct.get('year') else self.year
        grossing = int(dct['grossing']) if dct.get('grossing') else self.grossing
        url = dct['url'] if dct.get('url') else self.url
        return Movie(name, grossing, year, url)

    def __hash__(self):
        return hash((self.name, self.grossing, self.year, self.url))

    def __eq__(self, other):
        return self.url == other.url  # a movie is uniquely identified by it's url
