import unittest

from src.scraper.graphs.vertices.actor import Actor

"""
Classes to test the functionality of the Actor vertex
"""
class ActorTest(unittest.TestCase):
    def setUp(self):
        self.actor1 = Actor("Test1", 24, 45)
        self.actor2 = Actor("Test2", 32, 55)

    def test_init(self):
        self.assertEqual("Test1", self.actor1.name)
        self.assertEqual(24, self.actor1.age)
        self.assertEqual(45, self.actor1.total_gross)

    def test_eq(self):
        self.assertEqual(Actor("Test1", 24, 45), self.actor1)
        self.assertNotEqual(self.actor1, self.actor2)

    def test_to_dict(self):
        self.assertEqual({"json_class": "Actor", "name": "Test1", "age": 24, "total_gross": 45}, self.actor1.to_dict())

    def test_from_dict(self):
        actor = Actor("h", 3, 4)
        actor = actor.from_dict({"name": "Test1", "age": 24, "total_gross": 45})
        self.assertEqual(self.actor1, actor)


if __name__ == '__main__':
    unittest.main()
