import hashlib
import urllib


class Graph(object):
    def __init__(self, name, token, priority=0):
        self.name = name
        self.token = token
        self.priority = priority
        self.parameters = {}

    def __key(self):
        return self.name, self.token, self.priority

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def md5(self):
        return hashlib.md5(self.name + ':' + self.token).hexdigest()

    def set_parameters(self, parameters):
        self.parameters = parameters

    def render_parameters(self):
        return urllib.urlencode(self.parameters)

    @classmethod
    def from_hash(cls, g):
        graph = cls(g['name'], g['token'])
        graph.set_parameters(g['parameters'])
