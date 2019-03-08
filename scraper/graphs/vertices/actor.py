
"""
Represents an actor vertex. Contains the name, age, and url belonging to the actor
"""
class Actor():
    def __init__(self, name, age, total_gross):
        self.name = name
        self.age = age
        self.total_gross = total_gross

    """
    :return: a dict representation of the actor
    """
    def to_dict(self):
        return {"json_class": "Actor", "name": self.name, "age": self.age, "total_gross": self.total_gross}

    """
    :param dct: a dct that specifies attributes of the actor to be overwritten
    :return: a new actor with the same member values as the current actor except those specified to be changed by dct
    """
    def from_dict(self, dct):
        name = dct['name'] if dct.get('name') else self.name
        age = int(dct['age']) if dct.get('age') else self.age
        total_gross = int(dct['total_gross']) if dct.get('total_gross') else self.total_gross
        return Actor(name, age, total_gross)

    def __hash__(self):
        return hash((self.name, self.age, self.total_gross))

    def __eq__(self, other):
        return (self.name, self.age, self.total_gross) == (other.name, other.age, other.total_gross)
