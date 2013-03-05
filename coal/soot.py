import hashlib
import urllib

class Soot(object):
    def __init__(self, graph_name, local_identifier):
        self.name = graph_name
        self.identifier  = local_identifier
        self.parameters = {}

    def md5(self):
        return hashlib.md5(self.name+':'+self.identifier).hexdigest()

    def set_parameters(self, parameters):
        self.parameters = parameters

    def render_parameters(self):
        return urllib.urlencode(self.parameters)
